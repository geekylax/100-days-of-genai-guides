# The LLM Engineer's Handbook — my full notes

The book: **The LLM Engineer's Handbook** by Paul Iusztin & Maxime Labonne (Packt). These are my notes, in my words, for people who want the ideas before they buy the book. If one section clicks, buy it. The code is free on GitHub.

- Book: [Amazon](https://www.amazon.com/LLM-Engineers-Handbook-engineering-production/dp/1836200072/) · [Packt](https://www.packtpub.com/en-us/product/llm-engineers-handbook-9781836200062)
- The book's full code (MIT): [PacktPublishing/LLM-Engineers-Handbook](https://github.com/PacktPublishing/LLM-Engineers-Handbook)
- My starter repo to build stage 1 today: [rag-starter](https://github.com/geekylax/100-days-of-genai-guides/tree/main/llm-handbook/rag-starter)

---

## The one idea that holds the book together

The whole book builds one project end to end: an **LLM Twin**, an assistant that writes like you because it learned from your own posts, articles and code. The project is just the excuse. The real lesson is how a production LLM system is shaped.

They split everything into three pipelines, the **FTI architecture**:

| Pipeline | Job | Runs when |
|---|---|---|
| **Feature** | raw data → clean, chunked, embedded features | new data arrives |
| **Training** | features → a fine-tuned model in a registry | you decide to retrain |
| **Inference** | question + features + model → answer | a user asks |

The three only talk through two shared places: a **feature store** (for them, the Qdrant vector DB) and a **model registry**. That's why one can change without breaking the others. If you remember one diagram from the book, make it this one.

Their stack, for reference: ZenML (orchestration), MongoDB (raw data warehouse), Qdrant (vectors), Comet ML (experiment tracking), Opik (prompt monitoring), Hugging Face (models), AWS SageMaker (training + serving). You don't need any of it to start. My starter repo uses none of it on purpose.

---

## Stage 1 — Data: it was always a data problem

The book's first real lesson: your data pipeline sets the ceiling. The model only fills the space under it.

**Collect → Clean → Chunk → Embed → Store.**

- **Collect.** They write crawlers (one per source: articles, posts, code repos) and dump everything raw into a data warehouse first. Keep the raw copy. You will want to re-clean it later.
- **Clean.** Strip HTML, emojis you don't need, links, boilerplate, duplicate text. Boring, and where most quality comes from.
- **Chunk.** Different content wants different chunk sizes. A long article and a tweet should not be cut the same way. Overlap chunks slightly so an idea is never cut in half.
- **Embed.** Turn each chunk into a vector with an embedding model. Pick one model and keep it. Mixing models in one index breaks search.
- **Store.** Vectors + the original text + metadata (source, author, date) go into the vector DB. The metadata matters later, for filtering.

**Batch vs streaming.** Start with batch (re-index on a schedule). Streaming (change-data-capture: every new row in the warehouse triggers re-embedding) only when freshness really matters.

**My takeaway:** clean beats clever. A smaller model on clean, well-chunked data beats a bigger one on sludge.

---

## Stage 2 — Fine-tuning: last, not first

Three words to know:

- **SFT** (supervised fine-tuning): show the model good question → answer pairs until it copies the style and format.
- **LoRA / QLoRA**: instead of updating all the weights, train small adapter matrices. QLoRA does it on a 4-bit quantized model, so a 7–8B model fits on one GPU. Papers: [LoRA](https://arxiv.org/abs/2106.09685), [QLoRA](https://arxiv.org/abs/2305.14314).
- **DPO** (direct preference optimization): give pairs of answers, one *chosen* and one *rejected*, and the model learns which kind to prefer. Simpler than full RLHF, no separate reward model. Paper: [DPO](https://arxiv.org/abs/2305.18290).

**Building the dataset is most of the work.** The book generates an instruction dataset from the raw articles with an LLM (turn a paragraph into a question + answer), then filters hard: dedupe (exact and near-duplicate), remove junk, check that answers are accurate, diverse and not too easy. For DPO, it makes preference pairs the same way.

**Training.** They fine-tune a Llama 3.1 8B base with [Unsloth](https://github.com/unslothai/unsloth) (fast LoRA/QLoRA) and Hugging Face [TRL](https://huggingface.co/docs/trl/sft_trainer) ([DPO trainer](https://huggingface.co/docs/trl/dpo_trainer)). The knobs that matter: learning rate, epochs, batch size, max sequence length, LoRA rank, and the chat template (wrong template = silent garbage).

**When to fine-tune at all:**

- New **knowledge**? That's RAG, not fine-tuning.
- New **behaviour**, tone or output format? That's fine-tuning.
- Neither? Just write a better prompt. That one rule answers most "should I fine-tune?" questions.

---

## Evaluation (the chapter people skip)

You can't improve what you only "feel".

- **General benchmarks** (MMLU and friends) tell you the base model didn't break. They say little about your task.
- **Task-specific evals**: your own questions with known good answers. The ones that matter.
- **LLM-as-a-judge**: a strong model scores answers against a rubric (accuracy, style, relevance). Cheap, fast, good enough if you spot-check it.
- **RAG evals** score two things separately: did retrieval find the right chunks, and did the answer stay faithful to them. Tools: [Ragas](https://docs.ragas.io/) and ARES.

My rule from this chapter: write the eval script before you change anything. My starter has one (`evals.py`). Good further reading: [Hamel Husain on evals](https://hamel.dev/blog/posts/evals/).

---

## Stage 3 — RAG, past the beginner version

Beginners stop at "top-k by similarity and hope". The book's RAG inference pipeline adds three things before retrieval and one after:

- **Query expansion**: ask an LLM to rewrite the question a few ways, search with all of them, merge.
- **Self-querying**: pull structured filters out of the question ("posts by Maxime about RAG" → author = Maxime).
- **Filtered vector search**: search only where the metadata matches. This is why you stored metadata in stage 1.
- **Re-ranking**: retrieve wide (say 50), then a cross-encoder reads every (question, chunk) pair and keeps the best 5. Embedding search compares two vectors that never "saw" each other. A cross-encoder reads them together, so it's slower and much sharper.

**The single biggest upgrade for the least effort is re-ranking.** My starter does exactly this. Run `python ask.py "your question" --compare` and feel the jump.

---

## Stage 4 — Inference: make it fast and cheap

The demo is the easy part. The book spends real time on what makes serving affordable:

- **KV cache**: don't recompute attention for tokens you've already processed.
- **Continuous batching**: new requests join the batch as soon as a slot frees up, instead of waiting for the whole batch to finish.
- **Speculative decoding**: a small model drafts tokens, the big model checks several at once.
- **Better attention kernels**: FlashAttention, and PagedAttention ([paper](https://arxiv.org/abs/2309.06180)), which manages the KV cache like OS memory pages. It's the core of [vLLM](https://docs.vllm.ai/).
- **Model parallelism**: data, pipeline and tensor parallel, for when one GPU isn't enough.
- **Quantization**: run weights in lower precision (FP16 → 8-bit → 4-bit). Formats you'll see: GGUF (llama.cpp), GPTQ, EXL2, bitsandbytes NF4. Less memory, faster, small quality cost. Always eval after.

**Deployment choices** come down to: real-time API, async (queue + worker) or offline batch, and monolith vs separate microservices for the LLM and the business logic. They deploy the LLM as a SageMaker endpoint and put a FastAPI service in front that does the RAG part.

---

## Stage 5 — LLMOps: keep it alive

DevOps → MLOps → LLMOps. The LLM-specific additions:

- **Log every prompt and answer** (they use [Opik](https://github.com/comet-ml/opik)). Your logs are tomorrow's eval set.
- **Evals in CI**: every change to prompts, chunking or model runs the eval suite before it ships.
- **Watch for drift**: the questions users ask change. Re-check retrieval quality on new questions.
- **Guardrails**: check inputs and outputs (PII, off-topic, unsafe).
- **Alert on cost and latency**, not just errors.
- **Human feedback**: thumbs up/down becomes new preference data for the next DPO round.

Boring = in production.

---

## If I started over today: learn it in this order

1. **Clean + chunk your own 50 docs.** Notes, PDFs as text, your blog, your team's docs.
2. **Build naive RAG over them.** Top-5 by similarity.
3. **Add re-ranking.** Retrieve 50, keep 5. Feel the jump.
4. **Wrap it in an evals script.** 20–30 real questions, hit@5 before and after every change.
5. **Deploy it where a real person can use it.** Log every question.
6. **Only now fine-tune**, if the logs show you still need a new behaviour or format.

Steps 1–5 are exactly what the [rag-starter](https://github.com/geekylax/100-days-of-genai-guides/tree/main/llm-handbook/rag-starter) does, in about 200 lines you can read in one sitting. It comes loaded with these notes as sample docs, so it runs before you add your own.

---

## Go deeper (free)

- The book's code: [PacktPublishing/LLM-Engineers-Handbook](https://github.com/PacktPublishing/LLM-Engineers-Handbook)
- Maxime Labonne's free [LLM Course](https://github.com/mlabonne/llm-course) and [blog](https://maximelabonne.substack.com/)
- [Unsloth](https://github.com/unslothai/unsloth) for your first LoRA run
- [vLLM docs](https://docs.vllm.ai/) for serving
- [Qdrant docs](https://qdrant.tech/documentation/) for vector search
- [Sentence Transformers: cross-encoders](https://sbert.net/docs/cross_encoder/usage/usage.html) for re-ranking

*Notes by @geekylax_ai · 100 Days of GenAI. Read the book, it's worth it.*
