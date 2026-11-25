# Master AI Engineering — 250 Concepts (Part 1: Topics 1–13)

> @geekylax_ai · 100 Days of GenAI · Part 1 of 2

This is a flagship, build-first reference for the modern AI Engineer: the person who ships reliable products *on top of* foundation models rather than training them from scratch. Part 1 walks the full input-to-retrieval stack — from what an LLM actually is, through prompting and context engineering, into models, platforms, embeddings, vector databases, and Retrieval-Augmented Generation (RAG) — and every link below has been verified to load.

**How to read a "Learn it" list:** 📄 Paper · 🎥 Video · 💻 Code · 📘 Docs · 🔗 Link. Each entry says *why* it's worth your time. Seminal papers are linked at their exact arXiv `/abs/` URLs.

---

## 1. Introduction — What an AI Engineer Is

### What it is
An **AI Engineer** builds applications on top of pre-trained foundation models (LLMs, embedding models, multimodal models) by orchestrating prompts, context, tools, retrieval, and evaluation into reliable systems. The role exists because capability moved from *training* models to *composing* them: a general-purpose model you call over an API now does what used to require a bespoke trained model, so the hard, differentiated work shifts to the product layer — data pipelines, retrieval, guardrails, evals, latency/cost control, and UX.

Contrast with the **ML Engineer**: the ML Engineer owns the model itself — curating datasets, choosing architectures, training/fine-tuning, and optimizing loss on a held-out set. Their unit of work is a trained artifact and a metric (accuracy, F1, AUC). The AI Engineer's unit of work is a *system* whose central component is a frozen model they usually did not train. ML Engineers ask "how do I make the model better?"; AI Engineers ask "how do I make the *product* reliable given this model?" The two overlap on evaluation and MLOps but diverge sharply on where the leverage lives.

**Build vs. buy** is the role's defining decision. "Buy" = call a hosted frontier API (OpenAI, Anthropic, Google) — fastest to value, best quality, but per-token cost, data-residency, and vendor-lock considerations. "Build" = self-host open-weight models (Llama, Qwen, Mistral) — more control, fixed infra cost, privacy, but you own latency, scaling, and ops. Most mature systems are hybrids: a strong hosted model for hard reasoning, a cheap/local model for high-volume classification and extraction, routed per request.

### Why it matters
This is the single highest-leverage engineering role of the current cycle: the scarce skill is not training models but *productizing* them under real constraints (cost, latency, safety, accuracy). Getting the build-vs-buy and model-routing decisions right is often the difference between a demo and a margin-positive product.

### Key sub-concepts
- AI Engineer vs. ML Engineer vs. Data Scientist (unit of work, leverage point)
- Foundation models as a platform; the "application layer"
- Build vs. buy; hosted API vs. open-weight self-hosting; hybrid routing
- Total cost of ownership: per-token cost vs. GPU/infra cost
- Evaluation-driven development (evals as the new unit tests)
- Capabilities vs. reliability gap; the "last mile" of productization

### Learn it
- 🔗 [What We Learned Building AI Products (a16z / Andreessen Horowitz: "Emerging Architectures for LLM Applications")](https://a16z.com/emerging-architectures-for-llm-applications/) — the canonical reference architecture for the LLM app stack; orients the whole role.
- 📘 [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — the clearest statement of "start simple, add complexity only when it measurably helps," core to the build-vs-buy mindset.
- 🎥 [Andrej Karpathy — [1hr Talk] Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) — a product-and-systems framing of what these models are and how to think about building on them.
- 🔗 [OpenAI API Reference — Overview](https://developers.openai.com/api/reference/overview) — the "buy" path, concretely: what you actually call and pay for.

---

## 2. LLM Fundamentals — Tokens, Context, Training vs. Inference, Transformers

### What it is
A **Large Language Model (LLM)** is a neural network — almost always a **Transformer** — trained to predict the next **token** given the preceding tokens. A token is a sub-word unit (roughly ¾ of a word in English); text is split into tokens before the model ever sees it, and the model's entire input/output budget is counted in tokens, not characters or words.

Two distinct phases:
- **Training** is the compute-heavy, one-time (per model version) process of adjusting billions of parameters by gradient descent over trillions of tokens, so the network minimizes next-token prediction error. Modern pipelines add **post-training**: supervised fine-tuning (SFT) on instruction data, then preference optimization (RLHF/DPO) to make the model helpful and aligned.
- **Inference** is running the trained model forward to generate text. It is autoregressive: the model emits one token, appends it to the input, and repeats. Inference cost and latency scale with both input length (the prompt) and output length (tokens generated).

The **context window** is the maximum number of tokens the model can attend to at once (input + output). It is a hard architectural limit — exceed it and earlier tokens are truncated or dropped. Context windows have grown from ~2K tokens (early GPT-3 era) to 100K–1M+ in frontier models, which reshapes what's possible (whole codebases, long documents) but does not make context *free*: attention cost and "lost-in-the-middle" degradation still bite.

The **Transformer** is the architecture underneath. Its key innovation is **self-attention**: every token computes a weighted combination of every other token in the sequence, letting the model build context-dependent representations in parallel (unlike the sequential RNNs it replaced). Stacked attention + feed-forward layers, with residual connections and layer normalization, make up the network.

### Why it matters
Tokens are the unit of cost, latency, and context limits — every pricing, performance, and capacity decision is really a token-budget decision. Understanding the training/inference split tells you what you *can* change (prompts, context, fine-tuning) vs. what's baked in (the model's knowledge and reasoning priors).

### Key sub-concepts
- Tokens and tokenization; token ≈ ¾ word; input vs. output tokens
- Context window (max tokens); truncation; context as a shared budget
- Parameters, weights, pre-training vs. post-training (SFT, RLHF/DPO)
- Autoregressive / next-token prediction; the decoder-only architecture
- Transformers: self-attention, feed-forward layers, residuals, layer norm
- Scaling laws (more params + data + compute → predictably lower loss)

### Learn it
- 📄 [Attention Is All You Need — Vaswani et al., 2017](https://arxiv.org/abs/1706.03762) — the paper that introduced the Transformer; the foundation of essentially every LLM.
- 📄 [Language Models are Few-Shot Learners (GPT-3) — Brown et al., 2020](https://arxiv.org/abs/2005.14165) — showed scale alone unlocks in-context learning; defined the modern LLM.
- 🎥 [3Blue1Brown — Transformers, the tech behind LLMs (Deep Learning Chapter 5)](https://www.youtube.com/watch?v=wjZofJX0v4M) — the best visual intuition for what a Transformer computes, end to end.
- 📘 [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) — the classic diagram-driven walkthrough of the architecture.

![Transformer encoder sublayer with residual connections and layer normalization, from The Illustrated Transformer](https://jalammar.github.io/images/t/transformer_resideual_layer_norm_3.png)

---

## 3. How LLMs Work — Tokenization, Attention, Sampling, KV Cache, Speculative Decoding

### What it is
This is the mechanical, inference-time view of the model.

**Tokenization** converts text ↔ integers. The dominant scheme is **Byte-Pair Encoding (BPE)**: starting from bytes, the most frequent adjacent pairs are merged repeatedly to build a vocabulary of ~50K–200K tokens. This is why models miscount letters, struggle with arithmetic on long numbers, and behave oddly on rare languages or whitespace — those quirks are tokenization artifacts, not reasoning failures.

**Attention** is the computation at the heart of each layer. For each token, the model produces a **Query (Q)**, **Key (K)**, and **Value (V)** vector. The attention weight from token *i* to token *j* is the (scaled, softmax-normalized) dot product of *i*'s query with *j*'s key; the output for *i* is the weighted sum of all *V* vectors. **Multi-head attention** runs several such projections in parallel to capture different relationships. In decoder-only LLMs attention is **causal** (masked): a token may only attend to earlier tokens.

**Sampling** turns the model's output — a probability distribution over the vocabulary (logits → softmax) — into an actual next token:
- **Temperature** scales the logits before softmax. Low temperature (→0) sharpens the distribution toward the single most likely token (deterministic, focused); high temperature flattens it (diverse, creative, riskier).
- **Top-k** restricts sampling to the *k* most likely tokens.
- **Top-p (nucleus)** restricts sampling to the smallest set of tokens whose cumulative probability ≥ *p*, adapting the candidate set to the model's confidence.

**KV cache**: because generation is autoregressive and attention re-reads all prior tokens, naively recomputing every token's K and V each step is quadratic waste. The **KV cache** stores the K and V vectors of already-processed tokens so each new step only computes K/V for the one new token. It is the main reason generation is fast — and the main consumer of GPU memory during inference (cache size grows with context length × layers × heads).

**Speculative decoding** accelerates generation: a small, cheap **draft model** proposes several tokens ahead; the large **target model** verifies them all in a single parallel forward pass and accepts the longest correct prefix. Because the big model runs once per *several* accepted tokens instead of once per token, you get 2–3× speedups with *identical* output distribution (it's exact, not approximate).

### Why it matters
These are the dials and bottlenecks you actually touch in production: tokenization explains failure modes, sampling parameters control determinism vs. creativity (and reproducibility of evals), and KV cache + speculative decoding are why latency and GPU memory behave the way they do.

### Key sub-concepts
- BPE tokenization; vocabulary; token artifacts (counting, arithmetic, spacing)
- Q/K/V, scaled dot-product attention, softmax, multi-head, causal masking
- Logits → distribution; greedy vs. sampling decoding
- Temperature, top-k, top-p (nucleus), repetition/frequency penalties
- KV cache; memory growth with context; prefill vs. decode phases
- Speculative decoding (draft + verify); other efficiency tricks

### Learn it
- 🎥 [Andrej Karpathy — Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE) — builds BPE tokenization from scratch and explains every tokenization quirk you'll hit.
- 🎥 [Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY) — implements attention and a full GPT line by line; the single best way to internalize the mechanics.
- 🎥 [3Blue1Brown — Attention in transformers, step-by-step (Deep Learning Chapter 6)](https://www.youtube.com/watch?v=eMlx5fFNoYc) — the clearest visual explanation of Q/K/V and multi-head attention.
- 📄 [Fast Inference from Transformers via Speculative Decoding — Leviathan et al., 2022](https://arxiv.org/abs/2211.17192) — the original speculative decoding paper; exact-output speedups.
- 🎥 [StatQuest — Transformer Neural Networks, ChatGPT's foundation, Clearly Explained!!!](https://www.youtube.com/watch?v=zxQyTK8quyY) — a gentle, step-by-step reinforcement of attention and the decoding loop.

---

## 4. Prompt Engineering — Zero/Few-Shot, Chain-of-Thought, ReAct, Function Calling, Structured Outputs

### What it is
**Prompt engineering** is the practice of shaping a model's input to reliably elicit the behavior you want from a *frozen* model — no weight changes. It works because LLMs are **in-context learners**: they adapt to instructions, examples, and formats supplied at inference time.

Core techniques, in rough order of sophistication:
- **Zero-shot**: instruction only, no examples. "Classify the sentiment of this review."
- **Few-shot**: a handful of input→output examples in the prompt. The model infers the pattern and format from the demonstrations — often a large quality jump over zero-shot for structured tasks.
- **Chain-of-Thought (CoT)**: prompting the model to produce intermediate reasoning steps ("think step by step") before the final answer. This dramatically improves performance on arithmetic, logic, and multi-step tasks, because it lets the model allocate "computation" across tokens. **Self-consistency** extends CoT by sampling multiple reasoning paths and taking a majority vote on the answer.
- **ReAct (Reason + Act)**: interleaves reasoning traces with *actions* (tool calls, searches) and *observations* (results fed back in). This is the conceptual backbone of agents — the model thinks, acts, observes, and repeats until the task is done.
- **Function / tool calling**: the model is given machine-readable schemas (JSON Schema) of available functions; instead of answering in prose, it emits a structured call (name + arguments) that your code executes, returning the result for the model to continue with. This is how LLMs touch the real world (APIs, databases, code).
- **Structured outputs**: constraining the model to emit valid JSON conforming to a schema (via constrained decoding / "JSON mode"), so downstream code can parse it reliably instead of regex-scraping prose.

### Why it matters
Prompting is the cheapest, fastest lever you have — no training, instant iteration — and it's often the difference between 60% and 95% task accuracy. Function calling and structured outputs are what turn a chatbot into a *system component* with reliable, parseable I/O.

### Key sub-concepts
- Zero-shot, few-shot, in-context learning; demonstration selection
- Chain-of-Thought; self-consistency; reasoning-model "thinking" budgets
- ReAct loop (reason → act → observe); agents as prompting patterns
- Function/tool calling; JSON Schema for arguments
- Structured outputs / JSON mode / constrained decoding
- System vs. user vs. assistant roles; prompt templates; role prompting

### Learn it
- 📄 [Chain-of-Thought Prompting Elicits Reasoning in LLMs — Wei et al., 2022](https://arxiv.org/abs/2201.11903) — introduced CoT; one of the most influential prompting results.
- 📄 [ReAct: Synergizing Reasoning and Acting in Language Models — Yao et al., 2022](https://arxiv.org/abs/2210.03629) — the reason+act pattern behind modern agents.
- 📄 [Self-Consistency Improves Chain of Thought Reasoning — Wang et al., 2022](https://arxiv.org/abs/2203.11171) — sample many reasoning paths, vote; a reliable accuracy boost.
- 📄 [Toolformer: Language Models Can Teach Themselves to Use Tools — Schick et al., 2023](https://arxiv.org/abs/2302.04761) — foundational framing of LLMs invoking tools/APIs.
- 📘 [Anthropic — Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — a practical, maintained catalog of techniques with interactive tutorials.

---

## 5. Context Engineering — Memory, Retrieval, Context Compression, Token Budgeting

### What it is
**Context engineering** is the discipline of deciding *what information occupies the model's context window at each step*, and in what form. If prompt engineering is about wording the instruction, context engineering is about assembling the *payload* — the system prompt, tools, retrieved documents, conversation history, and memory — so the right facts are present, the wrong ones are absent, and the whole thing fits the budget.

It matters because the context window is a scarce, shared, and non-uniform resource:
- **Scarce**: every token of retrieved document competes with conversation history and output space.
- **Non-uniform**: models attend unevenly across position — the "lost-in-the-middle" effect means facts buried in the center of a long context are recalled worse than those at the start or end. More context is not monotonically better.
- **Costly**: you pay per input token on every call, and latency grows with context length.

Core moves:
- **Memory**: persisting information across turns/sessions. *Short-term* memory is the running conversation (often summarized as it grows); *long-term* memory stores durable facts (user preferences, prior decisions) in an external store and retrieves them as needed.
- **Retrieval**: pulling only the relevant slices of a large corpus into context on demand (this is RAG, Topic 13) rather than stuffing everything in.
- **Context compression**: summarizing or distilling history and documents to preserve signal while cutting tokens — recursive summarization of old turns, extracting only the relevant sentences from a retrieved chunk, or using a cheaper model to pre-condense.
- **Token budgeting**: explicitly allocating the window — e.g., reserve N tokens for system + tools, M for retrieved context, K for history, and guarantee room for the output — and enforcing it with truncation/eviction policies.

### Why it matters
As context windows and agentic loops grow, *what you put in the window* becomes the dominant driver of quality, cost, and latency — more so than clever wording. Poor context engineering shows up as hallucination (missing facts), distraction (irrelevant facts), and blown budgets (truncated, incoherent behavior).

### Key sub-concepts
- The context window as a shared, finite budget; token budgeting/allocation
- Lost-in-the-middle; positional recall degradation; context rot
- Short-term vs. long-term memory; conversation summarization; memory stores
- Retrieval as just-in-time context (bridge to RAG)
- Context compression: summarization, extraction, distillation
- Eviction/truncation policies; relevance filtering; re-ranking what to include

### Learn it
- 🔗 [Anthropic — Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — a current, practitioner-grade treatment of budgeting and curating the window.
- 📄 [Lost in the Middle: How Language Models Use Long Contexts — Liu et al., 2023](https://arxiv.org/abs/2307.03172) — the empirical paper on positional recall; required reading before you trust long context.
- 📘 [LlamaIndex — Framework Documentation](https://developers.llamaindex.ai/python/framework/) — practical patterns for memory, retrieval, and context assembly.
- 📘 [LangChain — Overview](https://docs.langchain.com/oss/python/langchain/overview) — agent/memory/middleware primitives for managing what enters the context.

---

## 6. Model Selection — Latency, Cost, Quality, Context, Reasoning Tradeoffs, Benchmarks

### What it is
**Model selection** is choosing *which* model to call for a given task, treating models as a portfolio rather than a single default. The axes you trade off:
- **Quality**: raw capability on your task (reasoning, instruction-following, coding, multilingual). Not a single number — a model that tops a chat leaderboard may be mediocre at structured extraction.
- **Cost**: priced per input and output token, often asymmetrically (output usually costs more). A 10–50× cost spread exists between frontier and small models.
- **Latency**: time-to-first-token (TTFT, dominated by prefill) and tokens-per-second (throughput, the decode phase). Interactive UX lives or dies on TTFT.
- **Context window**: how much you can feed in; larger windows cost more and can degrade recall.
- **Reasoning**: "reasoning" models spend extra inference-time compute on hidden chain-of-thought before answering — much stronger on hard logic/math/agentic tasks, but slower and pricier. Not worth it for simple extraction or classification.

The practical pattern is **routing**: send easy, high-volume requests to a small/cheap/fast model, and hard requests to a frontier/reasoning model — sometimes with an LLM or classifier deciding per request. The corollary is **task-specific evaluation**: public benchmarks are a starting filter, but you must build your own eval set on *your* data because benchmark rankings rarely transfer cleanly to a specific production task (and benchmark contamination is real).

**Benchmarks** to know as filters (not gospel): MMLU (knowledge), GPQA (hard science reasoning), HumanEval/SWE-bench (coding), MATH/AIME (math), and crowd-ranked arenas (LMArena/Chatbot Arena) for human preference.

### Why it matters
Model choice is usually the biggest single lever on both cost and quality in a shipped system; naive "always use the best model" can cost 20× more than a routed design at similar quality. Benchmark literacy prevents you from over-trusting a leaderboard that doesn't reflect your workload.

### Key sub-concepts
- Quality vs. cost vs. latency vs. context vs. reasoning tradeoff space
- Time-to-first-token (prefill) vs. throughput (decode); streaming UX
- Reasoning models and inference-time compute; when they're worth it
- Model routing / cascades; small-model-first designs
- Benchmarks: MMLU, GPQA, SWE-bench, MATH, LMArena; contamination
- Task-specific evals; why leaderboards don't transfer; eval-driven selection

### Learn it
- 🔗 [LMArena (Chatbot Arena) Leaderboard](https://arena.ai/leaderboard) — crowd-sourced human-preference rankings; the best single sanity check on relative chat quality.
- 🔗 [Artificial Analysis — Model Comparison](https://artificialanalysis.ai/) — side-by-side quality, price, and speed across providers; built for exactly this tradeoff.
- 📄 [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL — 2025](https://arxiv.org/abs/2501.12948) — the open reasoning model that made inference-time compute mainstream; read to understand the reasoning axis.
- 📘 [OpenAI API Reference — Overview](https://developers.openai.com/api/reference/overview) — concrete model IDs, pricing surface, and parameters to reason about.

---

## 7. AI Models — OpenAI, Anthropic Claude, Google Gemini, Mistral, Llama, DeepSeek, Qwen

### What it is
The **model landscape** splits into two camps you blend in practice:

**Proprietary / hosted (API-only, frontier quality):**
- **OpenAI (GPT family)** — broad general capability, strong tooling/ecosystem, reasoning models; the default "buy" option for many.
- **Anthropic (Claude family)** — strong on long-context, coding, instruction-following, and safety-sensitive work; emphasis on steerability.
- **Google (Gemini family)** — very large context windows, native multimodality, tight Google Cloud integration.

**Open-weight (downloadable weights, self-hostable):**
- **Meta Llama** — the open-weight series that catalyzed the local-LLM ecosystem; broad fine-tune/tooling support.
- **Mistral** — efficient European models (dense and Mixture-of-Experts); strong quality-per-parameter.
- **DeepSeek** — Chinese lab notable for cost-efficient training and strong open reasoning models (V3, R1) at frontier-adjacent quality.
- **Qwen (Alibaba)** — a prolific, strong multilingual open-weight family spanning many sizes and modalities; a common fine-tuning base.

The key distinction is **weights access**: proprietary models are capabilities you rent; open-weight models are artifacts you own (and must serve). "Open-weight" ≠ fully "open-source" — weights are released, but training data and full recipes often aren't. Licenses vary (permissive Apache-2.0 vs. community licenses with usage restrictions), so license review is part of selection.

### Why it matters
Your build-vs-buy strategy is expressed through this roster: frontier hosted models for the hardest reasoning, open-weight models for privacy, cost control at scale, and customization. Knowing each family's strengths lets you route and hedge against any single vendor.

### Key sub-concepts
- Proprietary/hosted vs. open-weight; "open-weight" ≠ "open-source"
- Model families: GPT, Claude, Gemini, Llama, Mistral, DeepSeek, Qwen
- Dense vs. Mixture-of-Experts (MoE) architectures; model sizes
- Licensing (Apache-2.0 vs. community/custom licenses); commercial use
- Multimodality; context-window differences; reasoning variants
- Vendor diversification / fallback strategy

### Learn it
- 📄 [Llama 2: Open Foundation and Fine-Tuned Chat Models — Touvron et al., 2023](https://arxiv.org/abs/2307.09288) — the open-weight release (and detailed technical report) that reshaped the ecosystem.
- 📄 [The Llama 3 Herd of Models — Meta AI, 2024](https://arxiv.org/abs/2407.21783) — an unusually transparent, encyclopedic report on building a frontier open model.
- 📄 [Mistral 7B — Jiang et al., 2023](https://arxiv.org/abs/2310.06825) — a landmark in quality-per-parameter and efficient attention.
- 📄 [DeepSeek-V3 Technical Report — 2024](https://arxiv.org/abs/2412.19437) — cost-efficient MoE training at scale; a frontier-adjacent open model.
- 📄 [Qwen2.5 Technical Report — Alibaba, 2024](https://arxiv.org/abs/2412.15115) — one of the strongest open multilingual families and fine-tuning bases.
- 📘 [Anthropic — Messages API Reference](https://platform.claude.com/docs/en/api/messages) — how you actually call a frontier hosted model, parameter by parameter.

---

## 8. Platforms & Ecosystem — Hugging Face, Ollama, LM Studio, OpenRouter, Groq, Together

### What it is
Between raw model weights and your application sits an **ecosystem** of platforms that host, serve, and route models.

- **Hugging Face** — the "GitHub of ML": the Hub hosts models, datasets, and demo Spaces, plus the `transformers` library that is the de facto standard for loading and running models. It's where open-weight models live and how most of them are distributed.
- **Ollama** — the simplest way to run open-weight models *locally* with one command; wraps `llama.cpp`, exposes a local REST API (port 11434), and handles model download/quantization. Ideal for dev, privacy, and offline.
- **LM Studio** — a desktop GUI app for discovering, downloading, and chatting with local models (MLX/`llama.cpp` runtimes), with a local OpenAI-compatible server. The non-CLI counterpart to Ollama.
- **OpenRouter** — a single API that routes to *hundreds* of models across providers behind one OpenAI-compatible endpoint, with automatic fallbacks and unified billing. Great for experimentation and vendor-agnostic apps.
- **Groq** — an inference provider built on custom LPU hardware delivering extremely high tokens-per-second; an OpenAI-compatible endpoint when latency is the priority.
- **Together AI** — a cloud platform to run, fine-tune, and serve open-weight models (serverless per-token or dedicated endpoints); a common "build" host for open models without owning GPUs.

The recurring pattern: most of these expose an **OpenAI-compatible API**, so you can swap providers by changing a base URL and key — which is itself a key architectural insight (code to the interface, not the vendor).

### Why it matters
These platforms decide how fast you can prototype, how cheaply you can serve, and how locked-in you are. OpenAI-compatible endpoints make the whole stack swappable, and local runners (Ollama/LM Studio) collapse the cost and privacy barrier to building with open models.

### Key sub-concepts
- Model hubs/registries (Hugging Face Hub); `transformers`; Spaces
- Local inference: Ollama, LM Studio; `llama.cpp`; quantization (GGUF)
- Inference providers / aggregators: OpenRouter, Groq, Together
- OpenAI-compatible API as a portability layer
- Serverless (per-token) vs. dedicated endpoints (per-GPU-hour)
- Latency-optimized hardware (Groq LPU) vs. general GPU serving

### Learn it
- 📘 [Hugging Face — Transformers Documentation](https://huggingface.co/docs/transformers/index) — the standard library and Hub; the center of the open ecosystem.
- 💻 [Ollama (GitHub)](https://github.com/ollama/ollama) — run open models locally in one command; local REST API.
- 📘 [OpenRouter — Quickstart](https://openrouter.ai/docs/quickstart) — one endpoint, hundreds of models, automatic fallbacks.
- 📘 [Groq — Docs Overview](https://console.groq.com/docs/overview) — OpenAI-compatible, latency-optimized inference.
- 📘 [Together AI — Introduction](https://docs.together.ai/docs/introduction) — serve and fine-tune open-weight models without owning GPUs.
- 🔗 [LM Studio](https://lmstudio.ai/) — desktop GUI for local models with an OpenAI-compatible server.

---

## 9. APIs & SDKs — OpenAI/Claude/Gemini APIs, LangChain, LlamaIndex, AI Gateways

### What it is
This is the integration layer: how your code talks to models and composes them.

**Provider APIs/SDKs** are the primitives. Each frontier lab ships an HTTP API and official SDKs: you send messages (system/user/assistant roles), the model streams back tokens, and you can attach tools (function schemas) and request structured outputs. The three to know — OpenAI, Anthropic (Claude), Google (Gemini) — differ in surface details but share the same shape, and most of the ecosystem speaks the **OpenAI-compatible** dialect.

**Orchestration frameworks** sit above the raw API to help build multi-step applications:
- **LangChain** — a broad framework of composable primitives (models, tools, memory, agents) for building agentic and chained LLM apps; pairs with LangGraph (stateful graphs) and LangSmith (tracing/evals).
- **LlamaIndex** — data-centric framework specialized for RAG and agents over *your* data: connectors, indexes, retrievers, and query engines.

You don't always need a framework — for simple apps, calling the provider SDK directly is cleaner. Frameworks earn their keep on complex agents, swappable providers, and built-in RAG/eval plumbing.

**AI gateways** are infrastructure that sits in front of model calls: a single proxy that handles API-key management, routing/fallbacks across providers, rate limiting, caching, cost tracking, and observability. OpenRouter is a hosted gateway; self-hosted options (e.g., proxies exposing an OpenAI-compatible endpoint) centralize governance so application code stays simple.

### Why it matters
This layer determines your development velocity, portability, and operability. Coding to an OpenAI-compatible interface plus a gateway means you can swap models, add caching, and get observability without touching app logic — the difference between a brittle prototype and a maintainable system.

### Key sub-concepts
- Provider APIs/SDKs; messages, roles, streaming, tool calling, structured output
- OpenAI-compatible API as a lingua franca
- Orchestration frameworks: LangChain (+ LangGraph, LangSmith), LlamaIndex
- When *not* to use a framework (direct SDK calls)
- AI gateways: routing, fallbacks, caching, rate limits, cost/observability
- Retries, timeouts, idempotency, streaming back-pressure

### Learn it
- 📘 [OpenAI — API Reference (Overview)](https://developers.openai.com/api/reference/overview) — the reference surface most of the ecosystem imitates.
- 📘 [Anthropic — Messages API Reference](https://platform.claude.com/docs/en/api/messages) — Claude's request/response shape, tools, streaming, and caching.
- 📘 [Google — Gemini API / AI Studio Docs](https://aistudio.google.com/docs) — the third major provider API and SDKs.
- 📘 [LangChain — Overview](https://docs.langchain.com/oss/python/langchain/overview) — agent/tool/memory primitives for orchestration.
- 📘 [LlamaIndex — Framework Docs](https://developers.llamaindex.ai/python/framework/) — the data/RAG-centric framework.

---

## 10. Embeddings — What They Are, Semantic Search, Similarity, Clustering

### What it is
An **embedding** is a dense vector of floating-point numbers (typically 256–4096 dimensions) that represents the *meaning* of a piece of text (or image, audio, code) as a point in a high-dimensional space. A good embedding model places semantically similar inputs close together and dissimilar inputs far apart — "king" near "queen," a question near its answer — regardless of exact wording.

This matters because it converts the fuzzy notion of "similar meaning" into a precise, computable **distance**:
- **Cosine similarity** — the cosine of the angle between two vectors; the standard measure for text embeddings (magnitude-invariant). Ranges from −1 to 1; higher = more similar.
- **Dot product** and **Euclidean (L2) distance** are the other common measures; for normalized vectors cosine and dot product rank identically.

With embeddings you get three workhorse capabilities:
- **Semantic search**: embed the query and the documents, return the documents whose vectors are nearest the query vector — matching on *meaning*, not keywords. This is the retrieval engine behind RAG.
- **Similarity / de-duplication / recommendation**: compare items directly by vector distance (find near-duplicates, "more like this").
- **Clustering**: group items by proximity in embedding space (topic discovery, deduplication at scale, labeling) using k-means or density methods on the vectors.

A crucial property is that embeddings are **learned**, contextual representations — modern text embedding models are Transformers fine-tuned (often contrastively) so that the single pooled vector captures sentence/passage meaning, unlike older bag-of-words vectors.

### Why it matters
Embeddings are the bridge from unstructured text to math — they power semantic search, RAG, clustering, classification, deduplication, and recommendation, all with the same primitive. Nearly every retrieval system you build starts by choosing an embedding model and a distance metric.

### Key sub-concepts
- Dense vectors; dimensionality; the semantic vector space
- Cosine similarity vs. dot product vs. Euclidean (L2); normalization
- Semantic (dense) search vs. keyword (lexical) search
- Clustering (k-means, density-based) on embeddings
- Classification and deduplication via nearest neighbors
- Contrastive learning; pooling a sequence into one vector

### Learn it
- 📄 [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks — Reimers & Gurevych, 2019](https://arxiv.org/abs/1908.10084) — the paper that made high-quality sentence embeddings practical; foundational for semantic search.
- 📘 [OpenAI — Vector Embeddings Guide](https://developers.openai.com/api/docs/guides/embeddings) — a clear, practical intro to embeddings, similarity, search, and clustering with worked examples.
- 🎥 [StatQuest — Word Embedding and Word2Vec, Clearly Explained!!!](https://www.youtube.com/watch?v=viZrOnJclY0) — the best gentle intuition for what an embedding *is* before the sentence-level view.
- 📘 [Sentence Transformers (SBERT) Documentation](https://sbert.net/) — the standard library for computing and using text embeddings.

---

## 11. Embedding Models — OpenAI/Gemini/Cohere Embeddings, Sentence Transformers, BGE

### What it is
An **embedding model** is the specific model that turns text into vectors; choosing one is a distinct decision from choosing your generation LLM. The landscape mirrors Topic 7:

**Hosted / API embeddings:**
- **OpenAI** (`text-embedding-3` family) — strong general-purpose embeddings with adjustable dimensions.
- **Google Gemini** embeddings — competitive hosted embeddings integrated with the Gemini stack.
- **Cohere** (Embed family) — embeddings designed for retrieval, with multilingual and compression-friendly variants.

**Open-weight / self-hosted embeddings:**
- **Sentence Transformers (SBERT)** — the library and a large catalog of open embedding models (e.g., `all-MiniLM`, `all-mpnet`); the default for local embedding.
- **BGE (BAAI General Embedding)** — a top open family; **BGE-M3** supports dense, sparse (lexical), *and* multi-vector (ColBERT-style) retrieval in one model, 100+ languages, up to 8192-token inputs.

Selection axes that matter specifically for embeddings:
- **Quality on your domain** — judged via the **MTEB** benchmark (and your own retrieval eval), not vibes.
- **Dimensionality** — more dims can mean better quality but higher storage/compute; some models support **Matryoshka Representation Learning**, letting you truncate the vector to a shorter prefix with graceful quality loss.
- **Max input length** — chunking depends on it.
- **Multilingual** coverage, and **cost/latency** (hosted per-token vs. local GPU).
- **Symmetric vs. asymmetric** search (query and document encoded the same way, or with different prompts/prefixes).

A hard rule: **query and documents must be embedded with the same model** (and the index rebuilt if you change models), because vectors from different models are not comparable.

### Why it matters
The embedding model sets the ceiling on retrieval quality — a weak embedder means your RAG system retrieves the wrong chunks no matter how good the LLM is. Dimensionality and max-length choices directly drive your vector-DB storage cost and chunking strategy.

### Key sub-concepts
- Hosted (OpenAI/Gemini/Cohere) vs. open-weight (SBERT, BGE) embedders
- MTEB benchmark for comparing models; task-specific retrieval evals
- Dimensionality; Matryoshka Representation Learning (truncatable dims)
- Max sequence length; multilingual coverage; cost/latency
- Symmetric vs. asymmetric (query/document) encoding; instruction prefixes
- Dense vs. sparse vs. multi-vector (ColBERT) embeddings; model-index coupling

### Learn it
- 📄 [MTEB: Massive Text Embedding Benchmark — Muennighoff et al., 2022](https://arxiv.org/abs/2210.07316) — the standard benchmark; how to compare embedding models rigorously.
- 🔗 [MTEB Leaderboard (Hugging Face Space)](https://huggingface.co/spaces/mteb/leaderboard) — the live ranking you consult before picking an embedder.
- 📄 [C-Pack / BGE: Packed Resources for General Embeddings — Xiao et al., 2023](https://arxiv.org/abs/2309.07597) — the paper behind the BGE family of open embedders.
- 💻 [BGE-M3 (Hugging Face model card)](https://huggingface.co/BAAI/bge-m3) — dense + sparse + multi-vector, 100+ languages, 8192-token inputs.
- 📄 [Matryoshka Representation Learning — Kusupati et al., 2022](https://arxiv.org/abs/2205.13147) — why you can truncate embeddings to save storage with minimal loss.
- 📘 [Sentence Transformers — Pretrained Models](https://sbert.net/) — the open embedding library and model catalog.

---

## 12. Vector Databases — Pinecone, Weaviate, Qdrant, Chroma, pgvector, FAISS, HNSW

### What it is
A **vector database** stores embeddings and answers **nearest-neighbor** queries: "given this query vector, return the *k* most similar stored vectors," fast, at scale, with metadata filtering.

The core problem is that *exact* nearest-neighbor search over millions of high-dimensional vectors is too slow (it's effectively linear scan). So vector DBs use **Approximate Nearest Neighbor (ANN)** indexes that trade a tiny bit of recall for enormous speedups. The dominant ANN algorithm is **HNSW (Hierarchical Navigable Small World)**: a multi-layer proximity graph where upper layers are sparse "express lanes" for coarse navigation and lower layers are dense for fine search. A query greedily walks the graph from the top layer down, converging on the nearest neighbors in logarithmic-ish time. Other index families include IVF (inverted file / clustering) and PQ (product quantization) for compression.

The product landscape:
- **FAISS** (Meta) — the foundational *library* (not a server) for similarity search and clustering; GPU-capable; the engine many systems embed.
- **hnswlib** — a lightweight header-only HNSW implementation; the reference for the algorithm.
- **pgvector** — a PostgreSQL extension adding vector types and HNSW/IVFFlat indexes; lets you keep vectors *next to* your relational data with JOINs and ACID — often the pragmatic first choice.
- **Chroma** — developer-friendly, embeddable open-source vector store; great for prototyping and local RAG.
- **Qdrant** — open-source, Rust-based vector DB with strong filtering and payloads; self-host or cloud.
- **Weaviate** — open-source vector DB with hybrid search, modules, and built-in model integrations.
- **Pinecone** — fully managed, serverless vector database; you offload all the ops.

Beyond the index, production concerns are **metadata filtering** (combine vector similarity with structured predicates), **hybrid search** support, **persistence/scaling**, and **recall vs. latency** tuning (HNSW's `ef`/`M` parameters).

### Why it matters
The vector DB is the retrieval backbone of RAG and semantic search; its index choice and tuning set your latency, recall, and cost at scale. Knowing when a Postgres extension (pgvector) suffices vs. when you need a dedicated/managed system (Pinecone, Qdrant, Weaviate) is a core architecture call.

### Key sub-concepts
- Exact vs. Approximate Nearest Neighbor (ANN); recall/latency tradeoff
- HNSW (proximity graph); IVF (clustering); PQ (quantization/compression)
- Library (FAISS, hnswlib) vs. database (Pinecone, Qdrant, Weaviate, Chroma)
- pgvector: vectors inside PostgreSQL; JOINs, ACID, filtering
- Metadata filtering; namespaces/collections; hybrid search support
- Distance metrics (cosine/dot/L2); index parameters (`M`, `ef`); scaling/persistence

### Learn it
- 📄 [Efficient and Robust ANN Search using HNSW Graphs — Malkov & Yashunin, 2016](https://arxiv.org/abs/1603.09320) — the HNSW paper; the algorithm nearly every vector DB uses.
- 📄 [Billion-scale Similarity Search with GPUs (FAISS) — Johnson, Douze & Jégou, 2017](https://arxiv.org/abs/1702.08734) — the foundational similarity-search library and its methods.
- 💻 [pgvector (GitHub)](https://github.com/pgvector/pgvector) — vector search inside Postgres; the pragmatic default for many teams.
- 📘 [Qdrant — Documentation](https://qdrant.tech/documentation/) — a production open-source vector DB with rich filtering.
- 📘 [Weaviate — Documentation](https://docs.weaviate.io/weaviate) — vector DB with built-in hybrid search and model integrations.
- 💻 [hnswlib (GitHub)](https://github.com/nmslib/hnswlib) — the reference HNSW implementation to read and learn from.

---

## 13. Retrieval (RAG) — Chunking, Retrieval, Reranking, Hybrid Search, Evaluation

### What it is
**Retrieval-Augmented Generation (RAG)** grounds an LLM in an external knowledge base: instead of relying only on parametric memory, the system *retrieves* relevant documents at query time and puts them in the context, so the model answers from provided evidence. This reduces hallucination, enables up-to-date and proprietary knowledge, and gives citeable sources — without retraining.

The pipeline, stage by stage:
1. **Ingestion & chunking** — split source documents into retrievable units. Chunk size is a real tradeoff: too small loses context, too large dilutes relevance and wastes tokens. Strategies include fixed-size with overlap, recursive/structural splitting (by headings/paragraphs), and semantic chunking. Each chunk is embedded (Topics 10–11) and stored in a vector DB (Topic 12) with metadata.
2. **Retrieval** — embed the query, fetch the top-*k* nearest chunks. This is **dense retrieval** (semantic). Its lexical counterpart is **sparse retrieval** (BM25/keyword), which excels at exact terms, names, and codes that dense retrieval can miss.
3. **Hybrid search** — combine dense + sparse scores (often via Reciprocal Rank Fusion) to get the best of both: semantic recall *and* exact-match precision.
4. **Reranking** — take the top candidates from retrieval and re-score each (query, chunk) pair with a **cross-encoder reranker** that reads query and document *together* (far more accurate than the independent bi-encoder embeddings used for first-stage retrieval, but too slow to run over the whole corpus). This two-stage "retrieve cheap, rerank precise" design is the single biggest quality lever in production RAG.
5. **Generation** — assemble the reranked chunks into the prompt (context engineering, Topic 5) and have the LLM answer, ideally with citations.

**Evaluation** is what separates a demo from a product. You measure retrieval quality (recall@k, precision, hit rate, MRR/NDCG) and generation quality (faithfulness/groundedness — is the answer supported by retrieved context? — and answer relevance). Frameworks like RAGAS and LLM-as-judge pipelines operationalize this. The canonical failure taxonomy: you either retrieved the wrong context, or retrieved the right context and the model ignored/contradicted it — and evals tell you which.

### Why it matters
RAG is the default architecture for grounding LLMs in private, large, or fresh knowledge, and it's the most common production LLM pattern after chat. Each stage — chunking, hybrid retrieval, reranking, and especially evaluation — is a distinct, measurable lever; teams that skip reranking and evals ship RAG systems that quietly hallucinate.

### Key sub-concepts
- Chunking strategies: fixed+overlap, recursive/structural, semantic; metadata
- Dense (embedding) vs. sparse (BM25/keyword) retrieval; top-*k*
- Hybrid search; Reciprocal Rank Fusion (RRF)
- Reranking with cross-encoders; bi-encoder vs. cross-encoder; two-stage retrieval
- Query transformation (rewriting, HyDE, multi-query); recursive/agentic retrieval
- Evaluation: recall@k, MRR/NDCG, faithfulness, answer relevance; RAGAS, LLM-as-judge

### Learn it
- 📄 [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — Lewis et al., 2020](https://arxiv.org/abs/2005.11401) — the paper that named and defined RAG.
- 📄 [Dense Passage Retrieval for Open-Domain QA — Karpukhin et al., 2020](https://arxiv.org/abs/2004.04906) — the foundation of dense (embedding-based) retrieval.
- 💻 [BGE Reranker v2-m3 (Hugging Face model card)](https://huggingface.co/BAAI/bge-reranker-v2-m3) — a strong open cross-encoder reranker; the second-stage quality lever.
- 📘 [LlamaIndex — Framework Documentation](https://developers.llamaindex.ai/python/framework/) — the most complete practical toolkit for building and tuning RAG pipelines.
- 📘 [Anthropic — Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — how to prompt the generation step to stay grounded in retrieved context.

---

> **Continue to Part 2 (Topics 14–25)** — fine-tuning, agents, evaluation & observability, guardrails & safety, multimodal, deployment & inference optimization, and production operations.

> @geekylax_ai · 100 Days of GenAI · Part 1 of 2 · *All links verified at time of writing.*
