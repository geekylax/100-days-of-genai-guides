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
