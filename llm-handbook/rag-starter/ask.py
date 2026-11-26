"""Steps 2 + 3: ask a question, naive vs re-ranked.

    python ask.py "why fine-tune last?"            # re-ranked (retrieve 50, keep 5)
    python ask.py "why fine-tune last?" --naive    # plain top-5
    python ask.py "why fine-tune last?" --compare  # both, side by side. Feel the jump.
"""
import sys

from rag import answer, retrieve, retrieve_rerank

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    raise SystemExit(__doc__)
q = " ".join(args)


def show(title, hits):
    print(f"\n== {title}")
    for i, h in enumerate(hits, 1):
        print(f"[{i}] {h['score']:.3f}  {h['source']}  ·  {h['text'][:110]}...")


if "--compare" in sys.argv:
    show("naive top-5", retrieve(q, 5))
    show("retrieve 50 -> re-rank -> keep 5", retrieve_rerank(q))
else:
    hits = retrieve(q, 5) if "--naive" in sys.argv else retrieve_rerank(q)
    show("naive top-5" if "--naive" in sys.argv else "re-ranked top-5", hits)
    print("\n== answer\n" + answer(q, hits))
