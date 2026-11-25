# Zero → AI job in 2026 — the exact path

> @geekylax_ai · 100 Days of GenAI

You don't need a degree, a research background, or a PhD to get hired as an AI Engineer in 2026 — you need **shipped proof** that you can wire models into products that work. This is the exact 7-step path: what to learn at each stage, *why* hiring managers actually care about it, and the verified resources to learn it from — no fluff, no 40-course playlists you'll never finish.

**How to use this page:** Don't read it top to bottom and feel productive. Pick Step 1, do it, build the tiny thing, move on. The whole path is realistically **3–5 months of consistent evenings**. Steps 2–6 each end in something you can put on GitHub. That portfolio *is* your application.

---

## Step 1 — Python + Git fundamentals

**What to learn:** Core Python (variables, lists/dicts, functions, loops, classes, f-strings, virtual environments, `pip`, reading JSON, calling an API with `requests`). Then Git/GitHub (commit, branch, push, pull request, `.gitignore`, how to write a README). You do **not** need advanced data science, NumPy internals, or LeetCode grinding yet.

**Why it matters for getting hired:** Every AI Engineer job is a Python job. The language is how you glue models, tools, and data together — and Git is how teams prove you can work in a real codebase without breaking things. A clean GitHub profile with readable commits signals "safe to hire" before anyone reads your resume. Recruiters literally click your repos first.

**Learn it:**
- 📘 [Kaggle — Learn Python](https://www.kaggle.com/learn/python) — Free, hands-on, in-browser micro-course; fastest way to get the syntax into your fingers.
- 📘 [Automate the Boring Stuff with Python (free online)](https://automatetheboringstuff.com/) — Al Sweigart's classic; teaches practical Python by building small real tools, not toy exercises.
- 🎥 [freeCodeCamp — Python for Beginners (full course)](https://www.freecodecamp.org/news/python-programming-course/) — Beginner course by Beau Carnes with guided projects (rock-paper-scissors, blackjack) that force you to actually write code.
- 📘 [Pro Git book (free, Chacon & Straub)](https://git-scm.com/book/en/v2) — The definitive Git reference; read Chapters 1–3 and you'll understand 95% of day-to-day Git.

**✅ Done when:** you can clone a repo, make a branch, push a commit, and open a pull request without Googling every step — and you have a GitHub account with at least one README.

---

## Step 2 — Use AI first: LLM APIs + local models, then ship a tiny tool

**What to learn:** Call a hosted LLM from Python — chat completions, system vs. user messages, temperature, streaming, and reading token usage. Learn at least two providers so you're not locked in (e.g. OpenAI + Groq or Gemini). Then run a model **locally** with Ollama so you understand the offline/private path. Finish by shipping one tiny tool (a CLI summarizer, a "clean up my notes" script, a Slack-style reply drafter).

**Why it matters for getting hired:** This is the mindset shift that separates AI Engineers from traditional devs — *reach for the model first*. Being fluent across APIs shows you can pick the right tool for cost/latency/privacy, which is a real production decision. Running Ollama locally signals you understand data privacy and on-prem constraints that enterprises care about. The tiny tool is your first portfolio artifact.

**Learn it:**
- 🎥 [Andrej Karpathy — [1hr Talk] Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) — The best one-hour mental model of what an LLM *is*, how it's trained, and its limits. Watch before touching an API.
- 📘 [Groq — API Quickstart](https://console.groq.com/docs/quickstart) — Get a key and your first chat completion in minutes; Groq's free tier is extremely fast for prototyping.
- 📘 [Google Gemini API — Get started](https://aistudio.google.com/docs/get-started) — Free key, multimodal input, structured JSON output, and function calling in one SDK.
- 📘 [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — The pattern that turns a chat model into something that can *act*; you'll lean on this again in Step 4.
- 💻 [Ollama (ollama.com)](https://ollama.com/) · [Ollama on GitHub](https://github.com/ollama/ollama) — One command (`ollama run`) to run open models (Qwen, Gemma, DeepSeek, gpt-oss) locally with a built-in REST API.

**✅ Done when:** you have a small script in a public repo that takes input, calls an LLM, and returns something genuinely useful — and you've run at least one model fully offline with Ollama.

---

## Step 3 — RAG: retrieval-augmented generation over your own data (the "money skill")

**What to learn:** The full RAG loop — **chunk** your documents, **embed** them, store vectors (start with FAISS or a managed vector DB), **retrieve** the top-k relevant chunks for a query, and **stuff** them into the prompt so the model answers from *your* data with citations. Then learn the two upgrades that move you from toy to real: **reranking** and **contextual chunking**.

**Why it matters for getting hired:** RAG is the single most-requested AI Engineering skill in 2026 because it's how companies put their internal knowledge (docs, tickets, policies, codebases) behind an LLM without fine-tuning or leaking data to training. "Chat with our docs" is the most common first AI project at almost every company — if you can build it reliably *and* improve retrieval quality, you're immediately employable. This is where "I played with ChatGPT" becomes "I can ship an AI feature."

**Learn it:**
- 💻 [Hugging Face Cookbook — Advanced RAG](https://huggingface.co/learn/cookbook/en/advanced_rag) — End-to-end runnable notebook: chunking by tokens, FAISS index, reranking with ColBERT, and assembling the answer. The best single "build it" resource.
- 📘 [LangChain — RAG guide](https://docs.langchain.com/oss/python/langchain/rag) — Official walkthrough of indexing, retrieval, and synthesis; also flags the real-world risk of prompt injection from retrieved content.
- 🔗 [Anthropic — Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — Why naive chunking loses context, and how prepending context + BM25 + reranking cut retrieval failures dramatically. This is the "make RAG actually good" post.

**✅ Done when:** you've built a RAG app over a dataset *you* chose (your notes, a PDF manual, a codebase) that answers questions with correct citations — and you can explain why you picked your chunk size.

---

## Step 4 — Build one real agent: tools + function-calling

**What to learn:** How an agent loop works — the model decides to call a **tool** (a function you define with a JSON schema), your code runs it, you feed the result back, and the model continues until it has an answer. Build one agent that uses 2–3 real tools (e.g. web search + a calculator + your RAG retriever). Learn when an **agent** is warranted vs. a simpler scripted **workflow** — knowing the difference is a senior signal.

**Why it matters for getting hired:** Agents are the frontier of what companies are paying to build in 2026 (support bots that take actions, research assistants, coding agents). Function-calling is the core primitive underneath all of them. Demonstrating a *working, debuggable* agent — not a flaky demo — shows you can handle the hardest, highest-value part of the job. Bonus: building one teaches you *why* most agent demos fail, which makes you sound experienced in interviews.

**Learn it:**
- 📘 [Hugging Face — AI Agents Course (free)](https://huggingface.co/learn/agents-course/unit0/introduction) — Structured, free course covering agent fundamentals, tools, and frameworks (smolagents, LlamaIndex, LangGraph), with a certificate.
- 📘 [OpenAI — Function calling](https://platform.openai.com/docs/guides/function-calling) — The canonical reference for defining tools, handling tool calls, and parallel/strict calling.
- 📘 [Anthropic — Tool use (Claude) overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — Clear mental model of client vs. server tools and the full tool-use round trip with code.
- 🔗 [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — The essay every AI Engineer should read: workflows vs. agents, the five core patterns, and "use the simplest thing that works."

**✅ Done when:** you have an agent that reliably calls real tools to complete a multi-step task, and you can articulate when you'd use a plain workflow instead.

---

## Step 5 — Evals: prove your system works (your edge over vibe coders)

**What to learn:** How to measure whether your AI actually works — **error analysis** (read real outputs, label failure modes), building a small **eval set** of input→expected-behavior cases, writing **LLM-as-judge** graders, and tracking a pass/fail score as you change prompts, chunking, or models. Learn to trust data over "it looked fine when I tried it twice."

**Why it matters for getting hired:** This is the skill that separates you from the flood of "I built a GPT wrapper" applicants. Anyone can get a demo working once; **proving** it works — and systematically improving it — is what production teams desperately need and can't find. In interviews, "here's my eval harness and how I raised accuracy from 72% to 89%" is a hiring-manager magnet. It's the clearest signal that you think like an engineer, not a prompt tinkerer.

**Learn it:**
- 🔗 [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — The foundational read: why vibe checks fail, the three levels of evaluation, and the Rechat case study. Start here.
- 🔗 [Hamel Husain — A Field Guide to Rapidly Improving AI Products](https://hamel.dev/blog/posts/field-guide/) — The practical follow-up: error analysis, data viewers, synthetic test data, and keeping your judges honest.
- 💻 [OpenAI Evals (GitHub)](https://github.com/openai/evals) — A real open-source eval framework + registry; read the structure, then write one eval for *your* Step 3/4 project.

**✅ Done when:** one of your projects has an eval set and a score, you've made a change, and you can show the number moving. Put the eval results in the README.

---

## Step 6 — Ship 3 projects: GitHub repo + live deployed link

**What to learn:** How to take a project from "works on my laptop" to "anyone can click this link and use it." Learn one deploy path end-to-end — a Gradio/Streamlit app on Hugging Face Spaces, a serverless app on Modal, or a web app on Vercel. Each project needs: a clean **GitHub repo**, a README with a screenshot/GIF and a one-line "what & why," and a **live URL**.

**Why it matters for getting hired:** A deployed link is the difference between "I'm learning AI" and "I build AI products." It proves you handled the unglamorous 20% — environment, secrets, hosting, cost — that trips up most self-taught devs. Three solid projects (ideally one RAG, one agent, one with evals) *are* your portfolio, and a live demo you can paste into an application converts far better than any resume bullet. Hiring managers click the link; they rarely read line 7 of your CV.

**Learn it:**
- 📘 [Hugging Face Spaces — docs](https://huggingface.co/docs/hub/spaces) — Free hosting for ML demo apps (Gradio, Docker, static); the fastest way to get a public, clickable AI demo.
- 📘 [Modal — docs & guide](https://modal.com/docs/guide) — Define your container and GPU in Python, deploy serverless, pay per second; ideal for RAG/agent backends and model inference.
- 📘 [Vercel — Deploying](https://vercel.com/docs/deployments) — Push to Git → auto-deploy with a live URL; the standard for a polished front end on top of your AI backend.

**✅ Done when:** you have **three** repos, each with a README, a demo GIF, and a working live link. Pin them on your GitHub profile.

---

## Step 7 — Apply as an AI Engineer: portfolio > resume, no degree needed

**What to learn:** How to position yourself. The AI Engineer role is about *applying* models to ship products — not training them — so you qualify the moment you have shipped proof. Write a one-paragraph "here's what I build" intro, link your three live projects first, and apply broadly to roles titled *AI Engineer*, *LLM Engineer*, *Applied AI*, *Forward-Deployed Engineer*, and *GenAI Engineer*. Build in public: post each project on LinkedIn/X with the demo link.

**Why it matters for getting hired:** This is a brand-new discipline where **demonstrated ability beats credentials** — companies are hiring faster than universities can produce "qualified" candidates, so a portfolio of working AI products is the single strongest signal you can send. Leading with live links (not a skills list) lets a hiring manager verify you in 60 seconds. "No degree" is genuinely not a blocker here; shipped proof is the currency.

**Learn it:**
- 🔗 [swyx — The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer) — The essay that named the role: why "you want engineers, not researchers," and why it's forecast to be the highest-demand engineering job of the decade. Read it to understand what you're applying *for*.
- 🔗 [roadmap.sh — AI Engineer Roadmap](https://roadmap.sh/ai-engineer) — Clear picture of the role vs. ML Engineer/researcher, plus a "do you need a degree?" FAQ. Use it to sanity-check your gaps.
- 💻 [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces) — Doubles as your public portfolio: host your three demos here and link the Space URLs directly in applications.

**✅ Done when:** your GitHub pins, a short portfolio page/README, and 3 live demo links are ready — and you've sent your first 10 applications with the links on top.

---

## What to do this week

You don't need the whole path done to start building momentum. This week:

1. **Today:** Make a GitHub account (if you don't have one) and finish the first two Kaggle Python lessons.
2. **Day 2–3:** Get a free Groq *or* Gemini API key and write a 20-line script that calls the model and prints a streamed answer. Push it to a public repo.
3. **Day 4–5:** `ollama run` a local model and watch Karpathy's 1-hour intro.
4. **Weekend:** Turn your script into one tiny, genuinely-useful tool with a real README. That's your first portfolio piece — Step 3 (RAG) is where it gets serious.

Ship small, ship public, ship weekly. In 2026, the person with three working demos beats the person with three certificates. Go build.

> *100 Days of GenAI — follow [@geekylax_ai](https://instagram.com/geekylax_ai) for the daily build.*
