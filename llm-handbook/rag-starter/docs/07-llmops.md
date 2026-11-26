## Stage 5 — LLMOps: keep it alive

DevOps → MLOps → LLMOps. The LLM-specific additions:

- **Log every prompt and answer** (they use [Opik](https://github.com/comet-ml/opik)). Your logs are tomorrow's eval set.
- **Evals in CI**: every change to prompts, chunking or model runs the eval suite before it ships.
- **Watch for drift**: the questions users ask change. Re-check retrieval quality on new questions.
- **Guardrails**: check inputs and outputs (PII, off-topic, unsafe).
- **Alert on cost and latency**, not just errors.
- **Human feedback**: thumbs up/down becomes new preference data for the next DPO round.

Boring = in production.
