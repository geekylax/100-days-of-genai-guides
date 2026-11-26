"""Step 5: put it where a real person can use it. A small API with every question logged.

    uvicorn serve:app --port 8000
    curl "http://localhost:8000/ask?q=why+fine-tune+last"

Every request is appended to logs.jsonl (question, sources, answer, latency): that log is the start
of "keep it alive". Read it weekly; the bad answers become new rows in evals.jsonl.
"""
import json
import time
from pathlib import Path

from fastapi import FastAPI

from rag import answer, load_index, retrieve_rerank

app = FastAPI(title="rag-starter")
LOG = Path(__file__).parent / "logs.jsonl"
load_index()


@app.get("/ask")
def ask(q: str):
    t0 = time.time()
    hits = retrieve_rerank(q)
    out = answer(q, hits)
    row = {"q": q, "sources": [h["source"] for h in hits], "answer": out, "ms": round((time.time() - t0) * 1000)}
    with open(LOG, "a") as fh:
        fh.write(json.dumps(row) + "\n")
    return row
