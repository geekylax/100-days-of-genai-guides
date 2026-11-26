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
