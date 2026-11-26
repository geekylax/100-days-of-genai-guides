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
