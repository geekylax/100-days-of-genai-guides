## If I started over today: learn it in this order

1. **Clean + chunk your own 50 docs.** Notes, PDFs as text, your blog, your team's docs.
2. **Build naive RAG over them.** Top-5 by similarity.
3. **Add re-ranking.** Retrieve 50, keep 5. Feel the jump.
4. **Wrap it in an evals script.** 20–30 real questions, hit@5 before and after every change.
5. **Deploy it where a real person can use it.** Log every question.
6. **Only now fine-tune**, if the logs show you still need a new behaviour or format.

Steps 1–5 are exactly what the [rag-starter](https://github.com/geekylax/100-days-of-genai-guides/tree/main/llm-handbook/rag-starter) does, in about 200 lines you can read in one sitting. It comes loaded with these notes as sample docs, so it runs before you add your own.
