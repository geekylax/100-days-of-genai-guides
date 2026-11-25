# Master AI Engineering — 250 Concepts (Part 2: Topics 14–25)

> @geekylax_ai · 100 Days of GenAI · Part 2 of 2

This is the second half of the field guide: the systems layer that turns a model into a product — agents, tools, fine-tuning, evaluation, safety, serving, and the MLOps discipline that keeps it all running. Every reference below was link-checked; where a seminal paper exists, you get the exact `/abs/` URL, and unverifiable links were dropped rather than guessed.

---

## 14. AI Agents

**What it is.** An *agent* is an LLM placed inside a control loop: at each step the model observes state, decides on an action (call a tool, write to memory, or finish), the environment executes that action, and the result is fed back as the next observation. The canonical formulation is **ReAct** — interleaving free-text *reasoning* traces with *acting* steps so the model can plan, call tools, and revise mid-task instead of emitting one shot of output. On top of the base loop you layer **planning** (decompose a goal into subgoals, sometimes with an explicit plan-then-execute split), **tool calling** (structured function invocation), **memory** (short-term scratchpad in context plus long-term retrieval from a store), **multi-agent** orchestration (specialist agents that hand off or debate), and **human-in-the-loop** checkpoints (approve, edit, or interrupt before a consequential action).

**Why it matters.** Agents are how you get an LLM to do multi-step work — research, code changes, operations — that no single prompt can accomplish, because the model gets to act, see consequences, and correct. The failure modes (compounding errors across steps, context rot, runaway tool loops, cost blow-ups) are also the hardest engineering problems in the field, which is why loop design, memory, and interruption points matter more than the base model choice.

**Key sub-concepts.** ReAct (reason + act) · plan-and-execute vs. reactive loops · tool/function calling · episodic & semantic memory, context management · self-reflection / self-critique (Reflexion) · multi-agent handoff, orchestrator–worker, debate · human-in-the-loop approval & interrupts · termination / step budgets.

**Learn it.**
- 📄 [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — the foundational agent loop; read this first to understand reason→act→observe.
- 📄 [Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903) — why intermediate reasoning traces unlock multi-step problem solving, the substrate ReAct builds on.
- 📄 [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — agents that reflect on failures in words and retry; the basis of self-critique loops.
- 📘 [LangGraph overview (LangChain)](https://docs.langchain.com/oss/python/langgraph/overview) — production patterns for state, persistence, memory, and human-in-the-loop in a real agent runtime.
- 📘 [Claude Agent SDK — Agent loop](https://code.claude.com/docs/en/agent-sdk/overview) — how a shipped harness runs plan→tool→observe with permissions, sessions, and subagents.

---

## 15. Agent Frameworks

**What it is.** Libraries that give you the agent loop, tool plumbing, state, and multi-agent orchestration so you don't rebuild them per project. They cluster into styles: **graph/state-machine** runtimes where you define nodes and edges explicitly (LangGraph); **role/crew** abstractions where you declare agents, tasks, and a process (CrewAI); **conversational multi-agent** frameworks where agents message each other (AutoGen); **data/RAG-first** agent toolkits (LlamaIndex); and **minimal, provider-native** SDKs that keep abstractions thin (OpenAI Agents SDK, Claude Agent SDK, Hugging Face `smolagents`, whose `CodeAgent` has the model write actions as Python).

**Why it matters.** The framework decides what's easy and what's impossible: how you resume a long run, where human approval hooks in, how you trace and debug, and whether you can swap models. Picking by loop model (graph vs. role vs. code-writing) rather than by hype is the single biggest architecture decision in an agent project. Note maturity signals too — AutoGen is now archived in favor of Microsoft Agent Framework.

**Key sub-concepts.** Explicit graph/state vs. implicit orchestration · roles, tasks, crews, flows · agents-as-tools & handoffs · code-writing agents (actions as Python) · guardrails/approvals as first-class nodes · tracing & observability hooks · model-agnostic vs. provider-native.

**Learn it.**
- 📘 [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) — low-level, durable graph runtime for long-running, stateful agents.
- 📘 [CrewAI](https://docs.crewai.com/) — role/crew and flows model for collaborative multi-agent systems.
- 📘 [Microsoft AutoGen](https://microsoft.github.io/autogen/stable/) — conversational multi-agent framework (now archived; see the maintenance notice).
- 📘 [LlamaIndex](https://developers.llamaindex.ai/python/framework/) — agents built over your data; strongest for RAG-centric workflows.
- 📘 [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — minimal primitives: agents, handoffs, guardrails, tracing.
- 📘 [smolagents (Hugging Face)](https://huggingface.co/docs/smolagents/index) — ~1k-line library; first-class `CodeAgent` that writes actions as code.

---

## 16. Tool Use & MCP

**What it is.** **Tool use** (function calling) is the mechanism by which an LLM, given a set of tools described by JSON schemas, emits a structured call naming a tool and its arguments; your application (or the provider) runs it and returns the result as a `tool_result` the model reads on the next turn. The **Model Context Protocol (MCP)** standardizes the *other* side of that boundary: an open, JSON-RPC 2.0 protocol (hosts ↔ clients ↔ servers) so any tool, data source, or prompt can be exposed once and consumed by any MCP-aware app — "USB-C for AI." On top sit **computer use** (the model drives a desktop via screenshots + mouse/keyboard) and **code execution** (the model writes and runs code in a sandbox to compute, transform data, or produce files).

**Why it matters.** Function calling is the single interface between a language model and everything deterministic — databases, APIs, calculators, your business logic. MCP turns a quadratic integration problem (M apps × N tools) into a linear one, which is why it spread across Claude, ChatGPT, and major IDEs within a year. Computer use and code execution extend reach to anything with a GUI or anything expressible as code.

**Key sub-concepts.** JSON-schema tool definitions · `tool_use`/`tool_result` round-trip · parallel tool calls, strict/structured outputs · client tools (run in your app) vs. server tools (run by provider) · MCP resources, prompts, tools; sampling, roots, elicitation · MCP transports & capability negotiation · computer use (screenshot→action) · sandboxed code execution.

**Learn it.**
- 📘 [Model Context Protocol — Introduction](https://modelcontextprotocol.io/) — what MCP is and why a standard connector layer matters.
- 📘 [MCP Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18) — authoritative protocol: hosts/clients/servers, features, and the security model.
- 📘 [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling) — defining tools, the multi-step flow, tool choice, parallel calls, strict mode.
- 📘 [Claude tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — client vs. server tools and the full tool_use→tool_result round trip, end to end.
- 💻 [Computer use tool (Claude)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) — screenshot-plus-input control of a desktop environment.
- 📄 [Toolformer: LMs Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761) — the research idea that models can learn *when* and *how* to call APIs.

---

## 17. Fine-Tuning

**What it is.** Adapting a pretrained model to a task, domain, or behavior. **SFT** (supervised fine-tuning) trains on curated input→output pairs. **PEFT** (parameter-efficient fine-tuning) updates only a small set of parameters: **LoRA** freezes the base weights and learns low-rank update matrices per layer, and **QLoRA** goes further by backpropagating LoRA adapters through a 4-bit (NF4) quantized frozen base, making single-GPU fine-tuning of large models feasible. **Preference tuning** aligns behavior to human choices: classic **RLHF** trains a reward model and optimizes with PPO (InstructGPT), while **DPO** skips the reward model and RL loop entirely, optimizing a simple classification-style loss directly on preference pairs. **Distillation** trains a small "student" to mimic a large "teacher," and **quantization** shrinks weights/activations to fewer bits for cheaper training and inference.

**Why it matters.** Full fine-tuning of a large model is cost-prohibitive; LoRA/QLoRA cut trainable parameters and memory by orders of magnitude while matching quality, which is what made custom models accessible outside big labs. DPO made alignment reproducible without the fragility of RL. Knowing *when to fine-tune vs. prompt vs. retrieve* — and which knob (SFT for format, preference tuning for behavior) — is core AI-engineering judgment.

**Key sub-concepts.** SFT & instruction tuning · LoRA rank/alpha, adapters · QLoRA 4-bit NF4, double quantization, paged optimizers · reward model + PPO (RLHF) · DPO & preference datasets · knowledge distillation (soft targets) · post-training quantization vs. QAT · data quality over quantity (LIMA).

**Learn it.**
- 📄 [LoRA: Low-Rank Adaptation of LLMs](https://arxiv.org/abs/2106.09685) — the low-rank-adapter method behind nearly all cheap fine-tuning.
- 📄 [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) — 4-bit NF4 + LoRA; fine-tune 65B-class models on one GPU.
- 📄 [Training LMs to Follow Instructions with Human Feedback (InstructGPT)](https://arxiv.org/abs/2203.02155) — the canonical RLHF recipe: SFT → reward model → PPO.
- 📄 [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290) — align to preferences without a reward model or RL; now a default.
- 📄 [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) — Hinton et al.'s original distillation; the basis for small, fast models.
- 📘 [Hugging Face PEFT docs](https://huggingface.co/docs/peft/index) — practical LoRA/QLoRA/adapters you can run today.

---

## 18. Evaluation

**What it is.** Measuring whether a model or an LLM system actually works, since accuracy alone doesn't capture usefulness, faithfulness, or safety. The toolkit: **benchmarks** (standardized task suites like HELM for broad, multi-metric comparison) and **human-preference leaderboards** (Chatbot Arena's pairwise Elo); **golden datasets** (curated input/expected pairs you regression-test against); **LLM-as-a-judge** (a strong model scores outputs against a rubric — scalable but needs calibration against humans and bias controls); **hallucination / faithfulness tests** (does the answer stay grounded in provided context?); and task-specific frameworks like **Ragas** that score RAG pipelines on faithfulness, answer relevancy, and context precision/recall.

**Why it matters.** You cannot improve what you can't measure, and LLM outputs are open-ended, so naive metrics mislead. A golden set plus LLM-judge turns "it feels better" into a number you can gate releases on; RAG-specific metrics tell you whether a bad answer came from retrieval or generation. Eval is the difference between shipping on vibes and shipping on evidence.

**Key sub-concepts.** Benchmarks & contamination · pairwise/Elo human preference · golden / reference datasets & regression suites · LLM-as-a-judge (pointwise vs. pairwise, position bias, calibration) · faithfulness / groundedness / hallucination rate · RAG metrics: context precision & recall, answer relevancy · offline vs. online eval.

**Learn it.**
- 📄 [Ragas: Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217) — reference-free metrics for faithfulness and context quality in RAG.
- 📘 [Ragas documentation](https://docs.ragas.io/en/stable/) — run experiments, built-in and custom metrics, framework integrations.
- 🔗 [Stanford HELM](https://crfm.stanford.edu/helm/) — holistic, multi-metric benchmarking across many models and scenarios.
- 📄 [Chatbot Arena: Evaluating LLMs by Human Preference](https://arxiv.org/abs/2403.04132) — the methodology behind pairwise/Elo leaderboards.
- 📘 [LangSmith evaluation & observability](https://docs.langchain.com/langsmith) — datasets, LLM-as-judge evaluators, and regression testing in practice.

---

## 19. Guardrails & Safety

**What it is.** The controls that keep an LLM system from producing or being manipulated into harmful behavior. **Prompt injection** is the defining threat: untrusted content (a web page, a document, a tool result) carries instructions the model follows as if they came from the user — and when an agent has tools plus private data plus external communication (the "lethal trifecta"), injection becomes data exfiltration. **Jailbreaks** are adversarial prompts that bypass alignment (including automated, transferable attacks like GCG). Defenses include **input/output classifiers** (e.g., Llama Guard), **content moderation**, **PII detection & redaction** before data reaches the model or logs, **programmable guardrails** that constrain dialogue and tool use, and **red teaming** — systematically probing for failures before attackers do. **Constitutional AI** bakes a set of principles into training so the model self-critiques.

**Why it matters.** There is no known complete fix for prompt injection, so defense is layered and probabilistic — which makes guardrails an architecture concern, not a feature you bolt on. For any agent touching private data or taking actions, the blast radius of a successful injection is the whole system; moderation, PII redaction, and red teaming are what make deployment responsible.

**Key sub-concepts.** Direct vs. indirect prompt injection · the lethal trifecta (private data + untrusted content + exfiltration channel) · jailbreaks & transferable adversarial suffixes (GCG) · input/output safety classifiers · PII detection/redaction · programmable rails (topic, dialog, tool) · red teaming & automated probing · Constitutional AI / RLAIF.

**Learn it.**
- 🔗 [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/) — the canonical risk taxonomy, LLM01 Prompt Injection through LLM10.
- 🔗 [Simon Willison — Prompt injection series](https://simonwillison.net/series/prompt-injection/) — the clearest running explanation of the threat and the "lethal trifecta."
- 📄 [Universal and Transferable Adversarial Attacks on Aligned LLMs (GCG)](https://arxiv.org/abs/2307.15043) — how automated jailbreak suffixes transfer across models.
- 📄 [Llama Guard: LLM-based Input-Output Safeguard](https://arxiv.org/abs/2312.06674) — a trainable classifier for moderating prompts and responses.
- 📘 [NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/index.html) — programmable rails for topics, jailbreak protection, and PII.
- 💻 [Microsoft Presidio](https://github.com/microsoft/presidio) — detect, redact, and anonymize PII in text and structured data.

---

## 20. Observability

**What it is.** Seeing inside an LLM system in production. The core primitive is the **trace**: a tree of spans covering one request — prompt, retrieval, each tool call, each model call, and nested agent steps — with inputs, outputs, and timing attached. Around traces you capture **metrics** (token counts, latency broken down by step, and cost per request/user/feature), build **dashboards** and **alerts**, and close **feedback loops** by logging user signals (thumbs, edits, corrections) and turning real traces into evaluation datasets. OpenTelemetry's GenAI semantic conventions standardize the attributes (model, token usage) so this telemetry is portable across tools.

**Why it matters.** LLM systems are non-deterministic and multi-step, so when a user reports a bad answer you need the exact trace to tell whether retrieval, a tool, or the model failed — logs of just the final output are useless. Token/latency/cost tracking is also how you keep spend sane: a single runaway agent loop can be 100× a normal request, and you only catch it if you're measuring per-step.

**Key sub-concepts.** Traces & spans (nested agent/tool/model calls) · token, latency, and cost attribution · dashboards & alerting · user-feedback capture → eval datasets · online evaluation on live traffic · OpenTelemetry GenAI semantic conventions · sampling & PII-safe logging.

**Learn it.**
- 📘 [OpenTelemetry for Generative AI](https://opentelemetry.io/blog/2024/otel-generative-ai/) — the vendor-neutral standard for GenAI traces, metrics, and token-usage attributes.
- 📘 [Langfuse docs](https://langfuse.com/docs) — open-source tracing, cost/latency analytics, dashboards, and evals.
- 📘 [LangSmith observability](https://docs.langchain.com/langsmith) — tracing, monitoring, automations, and feedback for LLM apps.

---

## 21. Deployment & Serving

**What it is.** Running models efficiently behind an API. The dominant pattern is a dedicated **inference server** that maximizes GPU utilization: **vLLM** introduced **PagedAttention** (manage the KV cache in non-contiguous "pages" like OS virtual memory) plus **continuous batching** (swap requests in and out of a running batch token-by-token), which together multiply throughput. **TGI** and **SGLang** are comparable high-throughput servers. Serving also means **streaming** tokens to the client (SSE) for low perceived latency, **autoscaling** replicas to demand, and **serverless GPU** platforms that spin capacity up per request so you don't pay for idle accelerators.

**Why it matters.** Naive one-request-per-forward-pass serving wastes most of a GPU; continuous batching and paged KV cache are the difference between serving 10 and 1000 concurrent users on the same hardware, i.e., an order-of-magnitude cost change. Streaming and autoscaling are what make a demo feel like a product and keep the bill tied to actual traffic.

**Key sub-concepts.** PagedAttention & KV-cache paging · continuous (in-flight) batching · tensor/pipeline parallelism · token streaming (SSE) · prefill vs. decode phases · autoscaling & cold starts · serverless GPU · throughput vs. latency (and per-token SLAs).

**Learn it.**
- 📘 [vLLM documentation](https://docs.vllm.ai/en/latest/) — the de facto open-source serving engine; quickstart to production tuning.
- 📄 [Efficient Memory Management for LLM Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — the paper behind vLLM's throughput gains; essential mental model.
- 📘 [Text Generation Inference (TGI)](https://huggingface.co/docs/text-generation-inference/index) — Hugging Face's production server (now maintenance mode; good for the concepts).
- 💻 [SGLang](https://github.com/sgl-project/sglang) — high-performance serving for LLMs and multimodal models, with structured-output support.

---

## 22. Optimization

**What it is.** Making inference faster and cheaper without retraining. **Quantization** stores weights/activations in fewer bits — **GPTQ** (accurate post-training 3–4 bit via second-order error correction) and **AWQ** (protect the salient weights activations touch) are the standard low-bit methods. **Speculative decoding** uses a small draft model to propose several tokens that the big model verifies in one pass, so you emit multiple tokens per expensive forward step; **Medusa** achieves the same with extra decoding heads instead of a separate draft model. **Flash Attention** restructures the attention computation to be IO-aware — tiling and avoiding materializing the full N×N matrix in slow memory — for exact attention that's far faster and lower-memory. **KV cache** reuse (and **prompt caching**, which persists the computed cache for a shared prefix across requests) cuts redundant prefill compute.

**Why it matters.** These are the techniques that turn a model you *can* run into one you can *afford* to run. 4-bit quantization roughly quarters memory; Flash Attention makes long contexts tractable; speculative decoding can 2–3× tokens/sec; prompt caching can slash cost and latency on repeated system prompts or long documents. They stack, and knowing which applies to your bottleneck (memory vs. latency vs. repeated-prefix cost) is the optimization skill.

**Key sub-concepts.** INT8/INT4 PTQ, GPTQ, AWQ (and the quality trade-off) · speculative/assisted decoding & draft models · Medusa heads · Flash Attention / IO-aware exact attention · KV cache management · prompt / prefix caching · batching interactions with the above.

**Learn it.**
- 📄 [FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135) — IO-aware attention; the reason long contexts are practical.
- 📄 [FlashAttention-2](https://arxiv.org/abs/2307.08691) — better parallelism and work partitioning; the version most stacks ship.
- 📄 [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) — draft-and-verify to emit multiple tokens per big-model step.
- 📄 [Medusa: Simple LLM Inference Acceleration with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) — speculative speedups without a separate draft model.
- 📄 [GPTQ: Accurate Post-Training Quantization](https://arxiv.org/abs/2210.17323) — 3–4 bit weights with minimal accuracy loss.
- 📄 [AWQ: Activation-aware Weight Quantization](https://arxiv.org/abs/2306.00978) — protect salient weights; strong low-bit quality and speed.

---

## 23. Multimodal AI

**What it is.** Models that work across text, images, audio, and video. **Vision-language models** bridge pixels and text — **CLIP** trained image and text encoders to share an embedding space via contrastive learning (the backbone of retrieval and generation), and **LLaVA**-style visual instruction tuning connects a vision encoder to an LLM so it can *reason about* images. **Text-to-image/video** generation is dominated by **latent diffusion** (denoise in a compressed latent space — the basis of Stable Diffusion) and diffusion-transformer video models (Sora). **Audio/speech**: **Whisper** does robust multilingual speech-to-text; **realtime speech-to-speech APIs** maintain conversation state and call tools with low latency. **OCR / document AI** turns scanned pages and PDFs into structured text — increasingly handled by the same vision-language models. **Segment Anything** provides promptable, general-purpose image segmentation.

**Why it matters.** Most real-world data isn't clean text — it's screenshots, scanned invoices, photos, call recordings. Multimodal models collapse once-separate pipelines (OCR, ASR, captioning, classification) into a single prompt, and they're what power voice agents, document extraction, and "take a photo and ask" products. The shared-embedding idea from CLIP also underlies cross-modal search and retrieval.

**Key sub-concepts.** Contrastive image-text pretraining (CLIP) · visual instruction tuning / VLMs (LLaVA) · latent diffusion & diffusion transformers · text-to-image and text-to-video · ASR (Whisper) & realtime speech-to-speech · OCR / document understanding · promptable segmentation (SAM) · cross-modal retrieval & embeddings.

**Learn it.**
- 📄 [CLIP: Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) — contrastive image-text pretraining; the shared-embedding backbone.
- 📄 [Visual Instruction Tuning (LLaVA)](https://arxiv.org/abs/2304.08485) — how a vision encoder is wired to an LLM for image reasoning.
- 📄 [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — the latent-diffusion method behind Stable Diffusion.
- 📄 [Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)](https://arxiv.org/abs/2212.04356) — the standard open ASR model and its training recipe.
- 📄 [Segment Anything](https://arxiv.org/abs/2304.02643) — a promptable, general segmentation foundation model.
- 📘 [OpenAI Realtime API](https://developers.openai.com/api/docs/guides/realtime) — low-latency speech-to-speech agents with state and tool calls.

---

## 24. Security

**What it is.** Protecting the system, its data, and its users across the LLM-specific attack surface. Beyond prompt injection (Topic 19), production security covers **API-key and secret management** (never in prompts, logs, or client code; rotate and scope), **data privacy** (what leaves your boundary, PII minimization, retention and training-opt-out), **access control** (authn/authz on tools and data — the model must not be able to reach anything the *user* can't), **sandboxing** (run model-written code and tool calls in isolated, least-privilege environments), **supply-chain** security (untrusted model weights, poisoned datasets, and — increasingly — malicious or over-privileged MCP servers and tool descriptions), and **compliance** (GDPR, SOC 2, sector rules). The MCP spec itself codifies consent, tool-safety, and sampling-control principles because tool descriptions and server responses are untrusted by default.

**Why it matters.** An LLM with tools is a confused-deputy risk: it will faithfully relay an injected instruction to a tool that has *your* credentials. Treating model inputs as untrusted, scoping every tool's permissions, sandboxing code execution, and vetting third-party servers/weights is what separates a prototype from something you can put in front of customer data without creating a breach path.

**Key sub-concepts.** Secret management & key rotation · least-privilege tool permissions (confused-deputy) · data minimization, retention, training opt-out · sandboxing & isolation for code/tool execution · supply-chain risk (weights, datasets, MCP servers, tool descriptions) · untrusted-by-default tool metadata · auditing & compliance (GDPR/SOC 2).

**Learn it.**
- 🔗 [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/) — the security checklist for LLM systems, from injection to unbounded consumption.
- 📘 [MCP security & trust principles (spec)](https://modelcontextprotocol.io/specification/2025-06-18) — why tool descriptions are untrusted and what consent/isolation to enforce.
- 🔗 [Simon Willison — the lethal trifecta & prompt-injection defenses](https://simonwillison.net/series/prompt-injection/) — the clearest framing of agent data-exfiltration risk.
- 💻 [garak — LLM vulnerability scanner](https://github.com/NVIDIA/garak) — automated probing for jailbreaks, leakage, and injection before you ship.
- 💻 [Microsoft Presidio](https://github.com/microsoft/presidio) — PII detection/redaction to keep sensitive data out of prompts and logs.

---

## 25. Production & MLOps

**What it is.** The engineering discipline that keeps an AI system reliable over time — the LLM-era extension of MLOps. **CI/CD for AI** means version-controlling prompts, configs, and datasets and gating deploys on *evaluation* (run your golden-set and LLM-judge suites in the pipeline, not just unit tests). A **model/prompt registry** stores versioned artifacts with aliases and lineage so you know exactly what's in production and can roll back. **Experiment tracking** records each run's parameters, data, and metrics for reproducibility. **Monitoring** watches live quality, cost, latency, and drift via tracing (Topic 20). **Retraining / refresh** loops feed production traces and feedback back into fine-tuning or into updated retrieval corpora and prompts.

**Why it matters.** Models and data drift, prompts rot as providers update models, and "it worked last week" is a real outage class. Treating prompts and eval sets as versioned artifacts — and gating every change on measured quality — is what makes AI systems maintainable by a team instead of fragile artifacts owned by whoever last touched them. The registry + eval-gated CI/CD loop is the backbone of shipping changes safely and often.

**Key sub-concepts.** Prompt/config/dataset versioning · eval-gated CI/CD (quality thresholds as release gates) · model & prompt registry (versions, aliases, lineage, rollback) · experiment tracking & reproducibility · drift & quality monitoring in production · feedback → dataset → retrain loop · canary / shadow deploys for model swaps.

**Learn it.**
- 📘 [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/) — centralized, versioned model store with aliases, tags, and lineage.
- 📘 [Langfuse](https://langfuse.com/docs) — production tracing, cost/quality monitoring, and prompt management.
- 📘 [LangSmith](https://docs.langchain.com/langsmith) — datasets, evaluators, and monitoring to gate and watch LLM deployments.
- 📘 [Ragas](https://docs.ragas.io/en/stable/) — turn evaluation into a repeatable experiment you can run in CI.

---

## Ship it

That's the systems half of AI engineering: an agent is a loop, tools are its hands, MCP is the standard socket, fine-tuning and optimization are how you make it yours and make it cheap, and evaluation, guardrails, observability, security, and MLOps are what keep it trustworthy in front of real users. Pick one topic, wire the smallest end-to-end version into something you actually run, measure it, and iterate — depth comes from shipping, not reading. — @geekylax_ai
