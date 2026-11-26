## Stage 3 — RAG, past the beginner version

Beginners stop at "top-k by similarity and hope". The book's RAG inference pipeline adds three things before retrieval and one after:

- **Query expansion**: ask an LLM to rewrite the question a few ways, search with all of them, merge.
- **Self-querying**: pull structured filters out of the question ("posts by Maxime about RAG" → author = Maxime).
- **Filtered vector search**: search only where the metadata matches. This is why you stored metadata in stage 1.
- **Re-ranking**: retrieve wide (say 50), then a cross-encoder reads every (question, chunk) pair and keeps the best 5. Embedding search compares two vectors that never "saw" each other. A cross-encoder reads them together, so it's slower and much sharper.

**The single biggest upgrade for the least effort is re-ranking.** My starter does exactly this. Run `python ask.py "your question" --compare` and feel the jump.
