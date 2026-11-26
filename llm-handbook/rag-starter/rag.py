"""The whole RAG starter in one small file: clean -> chunk -> embed -> retrieve -> re-rank -> answer.

Used by ingest.py, ask.py, evals.py and serve.py. Read it top to bottom; it is meant to be read.
"""
import json
import os
import re
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
INDEX = HERE / "index"
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")            # small, fast, good
RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

_embedder = None
_reranker = None


def embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def reranker():
    global _reranker
    if _reranker is None:
        from sentence_transformers import CrossEncoder
        _reranker = CrossEncoder(RERANK_MODEL)
    return _reranker


# ---------- step 1: clean + chunk -------------------------------------------------------------

def clean(text: str) -> str:
    """Boring, and where most of your quality comes from."""
    text = re.sub(r"<[^>]+>", " ", text)                 # stray HTML tags
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)    # markdown images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # markdown links -> their text
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk(text: str, size: int = 180, overlap: int = 40) -> list[str]:
    """Split on paragraphs, then pack paragraphs into ~`size`-word chunks with a little overlap,
    so an idea that spans two paragraphs is not cut in half."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], []
    for p in paras:
        words = p.split()
        if cur and len(cur) + len(words) > size:
            chunks.append(" ".join(cur))
            cur = cur[-overlap:]
        cur.extend(words)
        while len(cur) > size * 1.5:                       # one very long paragraph
            chunks.append(" ".join(cur[:size]))
            cur = cur[size - overlap:]
    if cur:
        chunks.append(" ".join(cur))
    return chunks


def load_docs(folder: Path) -> list[dict]:
    docs = []
    for f in sorted(folder.rglob("*")):
        if f.suffix.lower() in {".md", ".txt", ".html", ".htm"} and f.is_file():
            docs.append({"source": str(f.relative_to(folder)), "text": clean(f.read_text(errors="ignore"))})
    return docs


def build_index(folder: Path) -> int:
    docs = load_docs(folder)
    if not docs:
        raise SystemExit(f"No .md/.txt/.html files in {folder}")
    rows = [{"source": d["source"], "text": c} for d in docs for c in chunk(d["text"])]
    vecs = embedder().encode([r["text"] for r in rows], normalize_embeddings=True, show_progress_bar=True)
    INDEX.mkdir(exist_ok=True)
    np.save(INDEX / "vectors.npy", vecs.astype(np.float32))
    with open(INDEX / "chunks.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"{len(docs)} docs -> {len(rows)} chunks -> {INDEX}")
    return len(rows)


# ---------- step 2 + 3: retrieve, then re-rank ------------------------------------------------

_cache = None


def load_index():
    global _cache
    if _cache is None:
        if not (INDEX / "vectors.npy").exists():
            raise SystemExit("No index yet. Run: python ingest.py")
        rows = [json.loads(l) for l in open(INDEX / "chunks.jsonl")]
        _cache = (np.load(INDEX / "vectors.npy"), rows)
    return _cache


def retrieve(question: str, k: int = 5) -> list[dict]:
    """Naive RAG: top-k by cosine similarity. Where every beginner stops."""
    vecs, rows = load_index()
    # bge models want this prefix on the query (not on the documents)
    q = embedder().encode(["Represent this sentence for searching relevant passages: " + question], normalize_embeddings=True)[0]
    scores = vecs @ q
    top = np.argsort(-scores)[:k]
    return [{**rows[i], "score": float(scores[i])} for i in top]


def retrieve_rerank(question: str, wide: int = 50, keep: int = 5) -> list[dict]:
    """Pull wide (50), then let a cross-encoder read each (question, chunk) pair and keep the best 5."""
    cands = retrieve(question, k=wide)
    scores = reranker().predict([(question, c["text"]) for c in cands])
    order = np.argsort(-scores)[:keep]
    return [{**cands[i], "score": float(scores[i])} for i in order]


# ---------- answer (optional: needs any OpenAI-compatible endpoint) ---------------------------

def answer(question: str, hits: list[dict]) -> str:
    """Ask an LLM to answer from the chunks only, citing [1], [2]...
    Works with Groq (free key), OpenAI, or a local Ollama: set LLM_BASE_URL, LLM_API_KEY, LLM_MODEL."""
    import urllib.request
    base = os.getenv("LLM_BASE_URL")
    if not base:
        return "(no LLM set: showing the retrieved chunks only. See README, step 2.)"
    context = "\n\n".join(f"[{i + 1}] ({h['source']}) {h['text']}" for i, h in enumerate(hits))
    body = {
        "model": os.getenv("LLM_MODEL", "llama-3.1-8b-instant"),
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "Answer only from the context. Cite sources like [1]. If the context does not contain the answer, say you don't know."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    }
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.getenv("LLM_API_KEY", "none")},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["choices"][0]["message"]["content"]
