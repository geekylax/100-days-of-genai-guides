"""Step 4: a tiny evals script. Run it after every change, so "it feels better" becomes a number.

evals.jsonl has one question per line plus the doc that should answer it:
    {"q": "why fine-tune last?", "source": "02-fine-tuning.md"}

It reports hit@5 (is the right doc in the top 5?) and MRR (how high up it is) for naive vs re-ranked.
Write 20-30 questions about YOUR docs: questions real users would ask, not ones copied from the text.
"""
import json
import sys
from pathlib import Path

from rag import retrieve, retrieve_rerank

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "evals.jsonl"
cases = [json.loads(l) for l in open(path) if l.strip()]


def score(fn):
    hits, rr = 0, 0.0
    for c in cases:
        srcs = [h["source"] for h in fn(c["q"])]
        if c["source"] in srcs:
            hits += 1
            rr += 1 / (srcs.index(c["source"]) + 1)
    return hits / len(cases), rr / len(cases)


for name, fn in [("naive top-5", lambda q: retrieve(q, 5)), ("re-ranked", retrieve_rerank)]:
    h, m = score(fn)
    print(f"{name:12s}  hit@5 {h:.0%}   MRR {m:.2f}   ({len(cases)} questions)")
