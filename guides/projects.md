# 7 AI Projects That Get You Hired

> @geekylax_ai · 100 Days of GenAI

A shipped project beats 10 tutorials. Recruiters skim resumes in seconds, but a working repo with a live link forces them to stop and click — so build these seven, each one proof you can turn an LLM into something real.

Each project below is a buildable spec: **what to build**, the **stack**, **why it impresses recruiters**, a rough **difficulty**, and a **Learn it** list of verified references. Links are labeled 📘 Docs · 💻 Code · 🎥 Video · 📄 Paper · 🔗 Link.

---

## 1. Chat With Your Docs (RAG)

**What to build:** A Q&A app where a user drops in PDFs/Markdown and asks questions. You chunk the docs, embed them, store vectors, retrieve the top matches for each question, and feed them to an LLM with citations back to the source.

**Stack:** LlamaIndex *or* LangChain for the pipeline · a vector DB (Chroma to start, Pinecone/Weaviate/pgvector at scale) · any chat model · Streamlit or Next.js for the UI.

**Why it impresses recruiters:** RAG is the single most-requested GenAI skill on the market — almost every "AI feature" shipped in 2024–2026 is RAG under the hood. Showing you understand chunking, embeddings, retrieval quality, and citations proves you can build the thing companies actually pay for. Add source citations and you signal you care about hallucination, which is what separates a demo from production.

**Difficulty:** 🟢 Beginner–Intermediate · ~1 weekend

**Learn it**
- 📘 [LangChain — Build a RAG app](https://docs.langchain.com/oss/python/langchain/rag) — end-to-end tutorial that indexes real docs and answers over them.
- 📘 [LlamaIndex — Introduction to RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/) — the five RAG stages (load, index, store, query, evaluate) explained cleanly.
- 📘 [Chroma — Getting Started](https://docs.trychroma.com/docs/overview/getting-started) — spin up a local vector store in a few lines.
- 💻 [weaviate/Verba](https://github.com/weaviate/Verba) — a full open-source RAG chatbot to read for architecture ideas (note: archived/read-only, but the structure is gold).

![Verba RAG chatbot demo](https://raw.githubusercontent.com/weaviate/Verba/2.0.0/img/verba.gif)

---

## 2. An Agent That Does a Real Task

**What to build:** An agent that takes a goal, picks tools, and loops until it's done — e.g. "research the top 3 competitors for X and write a summary" using web-search + a scraper + a file-writer tool. The key is real tool-calling and a control loop, not a single prompt.

**Stack:** smolagents (code-first, minimal) *or* LangGraph (stateful, graph-based control) · function/tool definitions · a model that supports tool calls · optional sandbox (Docker/E2B/Modal) for safe code execution.

**Why it impresses recruiters:** "Agents" is the 2025–2026 hype cycle, and most candidates can only talk about them. A working agent that actually calls tools and recovers from failures shows you understand the orchestration layer — state, tool schemas, loops, and guardrails — which is exactly the hard part teams are hiring for.

**Difficulty:** 🟡 Intermediate · ~3–5 days

**Learn it**
- 📘 [smolagents — Docs](https://huggingface.co/docs/smolagents/index) — build an agent in a few lines; `CodeAgent` writes its actions as Python.
- 💻 [huggingface/smolagents](https://github.com/huggingface/smolagents) — the full library source; small enough to read end-to-end.
- 📘 [LangGraph — Overview](https://docs.langchain.com/oss/python/langgraph/overview) — stateful graphs with persistence, streaming, and human-in-the-loop for serious agents.

---

## 3. Fine-Tune a Small Model (LoRA / QLoRA)

**What to build:** Take a ~3B open model and LoRA/QLoRA fine-tune it on a focused dataset (your own tone, a classification task, a domain Q&A format). Ship the adapter weights, a before/after eval, and a short writeup of what changed.

**Stack:** Hugging Face PEFT (LoRA/QLoRA) *or* Unsloth (faster, lower VRAM) · a small base model (Llama 3.2 3B, Qwen 2.5 3B, Gemma) · a free Colab/Kaggle T4 GPU · a clean instruction dataset.

**Why it impresses recruiters:** Everyone can call an API — very few can *train*. Showing you understand LoRA, quantization, VRAM trade-offs, and overfitting proves depth most applicants don't have. Even one well-documented fine-tune with a measured improvement signals you can own the model layer, not just prompt it.

**Difficulty:** 🟡 Intermediate · ~3–5 days

**Learn it**
- 📘 [Hugging Face PEFT — Docs](https://huggingface.co/docs/peft/index) — the reference library for LoRA and other parameter-efficient methods.
- 💻 [unslothai/unsloth](https://github.com/unslothai/unsloth) — 2x faster fine-tuning with LoRA/QLoRA; widely used free Colab notebooks.
- 📘 [Unsloth — Docs](https://unsloth.ai/docs) — fine-tuning guide covering LoRA, QLoRA, and full fine-tuning.

---

## 4. An Eval Harness (Auto-Score LLM Outputs)

**What to build:** A test suite that runs your prompts/app against a dataset of cases and auto-scores the outputs — exact-match, LLM-as-a-judge, RAG faithfulness/relevancy — then fails CI when quality drops. Turn "it feels better" into a number.

**Stack:** promptfoo (CLI/CI-first) *or* DeepEval (Pytest-style) for general LLM evals · Ragas for RAG-specific metrics (faithfulness, answer relevancy, context precision) · wire it into GitHub Actions.

**Why it impresses recruiters:** Evals are where senior engineers separate from juniors. Anyone can build a demo; proving it works with a reproducible scorecard shows engineering maturity and that you think about regressions, red-teaming, and reliability — the stuff that keeps AI features from breaking in production.

**Difficulty:** 🟡 Intermediate · ~2–4 days

**Learn it**
- 📘 [promptfoo — Docs (Intro)](https://www.promptfoo.dev/docs/intro/) — declarative evals + red-teaming you can drop into CI/CD.
- 💻 [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) — the open-source CLI/library for evaluating and red-teaming LLM apps.
- 💻 [confident-ai/deepeval](https://github.com/confident-ai/deepeval) — "the LLM evaluation framework," Pytest-like with G-Eval and judge metrics.
- 📘 [DeepEval — Docs](https://deepeval.com/) — metrics for agents, RAG, chat, and safety, plus quickstart.
- 📘 [Ragas — Docs](https://docs.ragas.io/en/stable/) · 💻 [vibrantlabsai/ragas](https://github.com/vibrantlabsai/ragas) — the standard toolkit for RAG metrics.

---

## 5. Multimodal App (Image → Structured JSON)

**What to build:** Point a vision model at an image and get clean, typed JSON back — e.g. a receipt photo → `{merchant, date, line_items[], total}` → one row in an expense sheet. The trick is enforcing a schema so the output is machine-usable, not prose.

**Stack:** A vision-capable model (GPT-4o/4.1-class, or a local VLM like Qwen2-VL via Ollama/smolagents) · structured outputs / JSON-schema enforcement · a tiny frontend or a Google Sheet write.

**Why it impresses recruiters:** Multimodal + structured output is an instantly demo-able business win — invoices, receipts, IDs, forms. It shows you can connect a model to a real workflow and guarantee the output shape downstream systems need, which is exactly how AI gets deployed inside companies.

**Difficulty:** 🟢 Beginner–Intermediate · ~2–3 days

**Learn it**
- 📘 [OpenAI — Images and vision](https://developers.openai.com/api/docs/guides/images-vision) — how to pass images (URL, base64, file ID) to a model.
- 📘 [OpenAI — Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) — constrain responses to a JSON Schema so the output is always valid.
- 📘 [smolagents — Docs](https://huggingface.co/docs/smolagents/index) — model-agnostic path if you want a local/open vision model instead of an API.

---

## 6. Deploy a Model as an API

**What to build:** Serve an open model behind an OpenAI-compatible HTTP endpoint, then put a minimal chat frontend in front of it — deployed to a URL anyone can hit. This is the gap between "runs on my laptop" and "it's live."

**Stack:** vLLM for high-throughput serving (or Modal for serverless GPU, or Ollama for the simplest local path) · an OpenAI-compatible API layer · a small Next.js/Streamlit frontend · a GPU host.

**Why it impresses recruiters:** Deployment is where most portfolio projects die. A live, shareable endpoint proves you understand serving, throughput, GPUs, and productionization — the operational skills that make you hireable as an *engineer*, not just a notebook tinkerer. A working URL on your resume is worth more than any screenshot.

**Difficulty:** 🔴 Intermediate–Advanced · ~3–5 days

**Learn it**
- 📘 [vLLM — Docs](https://docs.vllm.ai/en/latest/) — fast, memory-efficient serving with an OpenAI-compatible API server built in.
- 💻 [vllm-project/vllm](https://github.com/vllm-project/vllm) — the high-throughput inference & serving engine itself.
- 📘 [Modal — Run OpenAI-compatible LLM inference with vLLM](https://modal.com/docs/examples/vllm_inference) — serverless GPU deploy you can copy almost verbatim.
- 💻 [ollama/ollama](https://github.com/ollama/ollama) — the simplest way to run and expose open models locally via a REST API.

---

## 7. Automate Your Own Boring Task, End-to-End

**What to build:** Pick one tedious thing *you* actually do weekly — triaging emails, summarizing a Slack channel, turning meeting notes into tickets, sorting receipts — and automate it fully: trigger → LLM step(s) → action (write to Notion/Sheets/email). Record a 30-second before/after.

**Stack:** n8n (visual, 1500+ integrations) *or* a code-first agent (smolagents/LangGraph) · a trigger (cron, webhook, inbox) · your real tools (Gmail, Sheets, Notion, Slack) · deploy so it runs unattended.

**Why it impresses recruiters:** This is the most memorable project because it's *yours* — a genuine problem solved end-to-end, not a toy from a tutorial. It shows product sense, glue-code skill, and the instinct to ship something useful, which is exactly the "builder who gets things done" signal hiring managers chase. Great story in an interview: "here's a thing I built that I still use every day."

**Difficulty:** 🟢 Beginner–Intermediate · ~2–4 days

**Learn it**
- 💻 [n8n-io/n8n](https://github.com/n8n-io/n8n) — fair-code workflow automation with native AI nodes and 1500+ integrations.
- 📘 [smolagents — Docs](https://huggingface.co/docs/smolagents/index) — go code-first if your task needs custom tools and real reasoning loops.
- 📘 [LangGraph — Overview](https://docs.langchain.com/oss/python/langgraph/overview) — for scheduled, stateful automations that recover from failures.

---

## Ship It: GitHub + a Live Link

A project only counts if a recruiter can find it. For each build:

1. **Put it on GitHub** — clean README (what it does, screenshot/GIF, how to run), pinned on your profile.
2. **Give it a live link** — deploy the demo (Streamlit Community Cloud, Vercel, Hugging Face Spaces, Modal) and put the URL at the top of the README *and* your resume.
3. **Write 3 lines on what you learned** — the trade-off you hit, the metric you moved, the thing you'd do differently. That's the senior signal.

**Do one, do it well, ship it loud.** One finished, deployed, documented project beats seven half-built notebooks — and beats ten tutorials you only watched.

> @geekylax_ai · 100 Days of GenAI
