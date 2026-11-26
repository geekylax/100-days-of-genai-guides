## Evaluation (the chapter people skip)

You can't improve what you only "feel".

- **General benchmarks** (MMLU and friends) tell you the base model didn't break. They say little about your task.
- **Task-specific evals**: your own questions with known good answers. The ones that matter.
- **LLM-as-a-judge**: a strong model scores answers against a rubric (accuracy, style, relevance). Cheap, fast, good enough if you spot-check it.
- **RAG evals** score two things separately: did retrieval find the right chunks, and did the answer stay faithful to them. Tools: [Ragas](https://docs.ragas.io/) and ARES.

My rule from this chapter: write the eval script before you change anything. My starter has one (`evals.py`). Good further reading: [Hamel Husain on evals](https://hamel.dev/blog/posts/evals/).
