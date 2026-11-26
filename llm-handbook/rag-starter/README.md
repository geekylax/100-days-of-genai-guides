# rag-starter · build stage 1 today

A RAG starter you can read in one sitting (~200 lines), from my notes on **The LLM Engineer's Handbook** (Iusztin & Labonne). It follows the order I'd learn it in if I started over:

1. Clean + chunk your own 50 docs → `ingest.py`
2. Naive RAG over them → `ask.py --naive`
3. Add re-ranking (retrieve 50, keep 5) → `ask.py`
4. Wrap it in an evals script → `evals.py`
5. Deploy it where a real person can use it, log every question → `serve.py`
6. Only then fine-tune, if the logs show you still need to

My full notes: [notes.md](../notes.md). The book's own (much bigger) code: [PacktPublishing/LLM-Engineers-Handbook](https://github.com/PacktPublishing/LLM-Engineers-Handbook).

## Run it (5 minutes)

```bash
git clone https://github.com/geekylax/100-days-of-genai-guides.git
cd 100-days-of-genai-guides/llm-handbook/rag-starter
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python ingest.py                                       # step 1: indexes ./docs (my handbook notes)
python ask.py "should I fine-tune or use RAG?" --compare   # steps 2 + 3: naive vs re-ranked
python evals.py                                        # step 4: hit@5 and MRR, naive vs re-ranked
```

The first run downloads two small models (~100 MB): [bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) for embeddings and [ms-marco-MiniLM-L-6-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2) for re-ranking. Runs on a laptop CPU, no GPU and no API key needed.

On the sample docs I got: naive hit@5 95% / MRR 0.73 → re-ranked hit@5 100% / MRR 0.97 (20 questions). Your numbers will differ. That's the point: measure yours.

## Now use YOUR docs

1. Put up to ~50 `.md` / `.txt` / `.html` files in a folder (export your notes, blog posts, team docs; PDFs → convert to text first).
2. `python ingest.py path/to/your_folder`
3. Rewrite `evals.jsonl`: 20–30 questions a real person would ask, each with the file that should answer it.
4. `python evals.py`. Change one thing (chunk size in `rag.py`, `wide`/`keep`, the embedding model), run it again. Keep what wins.

## Get real answers, not just chunks (optional)

`ask.py` shows the retrieved chunks. To get a written answer with citations, point it at any OpenAI-compatible LLM:

```bash
# Groq (free key at console.groq.com)
export LLM_BASE_URL=https://api.groq.com/openai/v1 LLM_API_KEY=your_key LLM_MODEL=llama-3.1-8b-instant
# or local Ollama (ollama.com), after `ollama pull llama3.1`
export LLM_BASE_URL=http://localhost:11434/v1 LLM_MODEL=llama3.1
```

## Step 5: serve it

```bash
uvicorn serve:app --port 8000
curl "http://localhost:8000/ask?q=why+fine-tune+last"
```

Every question is logged to `logs.jsonl` with its sources, answer and latency. Read it weekly. Bad answers become new rows in `evals.jsonl`. That's LLMOps at its smallest.

## Files

| File | What it does |
|---|---|
| `rag.py` | everything: clean, chunk, embed, retrieve, re-rank, answer |
| `ingest.py` | step 1, builds `index/` |
| `ask.py` | steps 2–3, `--naive` / `--compare` |
| `evals.py` + `evals.jsonl` | step 4 |
| `serve.py` | step 5, FastAPI + question log |
| `docs/` | sample docs (my handbook notes); replace with yours |

Made for [@geekylax_ai](https://www.instagram.com/geekylax_ai/) · 100 Days of GenAI. MIT, use it for anything.
