## Stage 4 — Inference: make it fast and cheap

The demo is the easy part. The book spends real time on what makes serving affordable:

- **KV cache**: don't recompute attention for tokens you've already processed.
- **Continuous batching**: new requests join the batch as soon as a slot frees up, instead of waiting for the whole batch to finish.
- **Speculative decoding**: a small model drafts tokens, the big model checks several at once.
- **Better attention kernels**: FlashAttention, and PagedAttention ([paper](https://arxiv.org/abs/2309.06180)), which manages the KV cache like OS memory pages. It's the core of [vLLM](https://docs.vllm.ai/).
- **Model parallelism**: data, pipeline and tensor parallel, for when one GPU isn't enough.
- **Quantization**: run weights in lower precision (FP16 → 8-bit → 4-bit). Formats you'll see: GGUF (llama.cpp), GPTQ, EXL2, bitsandbytes NF4. Less memory, faster, small quality cost. Always eval after.

**Deployment choices** come down to: real-time API, async (queue + worker) or offline batch, and monolith vs separate microservices for the LLM and the business logic. They deploy the LLM as a SageMaker endpoint and put a FastAPI service in front that does the RAG part.
