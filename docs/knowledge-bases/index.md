# :material-book-open-page-variant: Knowledge Bases

Knowledge bases are markdown documents that provide context to AI assistants via semantic search. They are the foundation of the RAG (Retrieval-Augmented Generation) strategy used by the MCP server.

## :material-format-list-bulleted: Available Topics

| Topic | Description |
|-------|-------------|
| :material-file-document-outline: [SDD](sdd.md) | Spec-Driven Development methodology, templates, and best practices |

## :material-cog: How It Works

```mermaid
graph LR
    subgraph Input["📝 Markdown Files"]
        MD["knowledge-bases/**/*.md"]
    end

    subgraph Processing["⚙️ Indexing"]
        C["Chunking<br/><small>Split by headings</small>"]
        E["Embedding<br/><small>BAAI/bge-small-en-v1.5</small>"]
    end

    subgraph Output["🔍 Search"]
        Q["Query"] --> S["Semantic Similarity"]
        S --> R["Ranked Results"]
    end

    MD --> C --> E --> S

    style Input fill:#e8f5e9,stroke:#4caf50
    style Processing fill:#e3f2fd,stroke:#2196f3
    style Output fill:#fff3e0,stroke:#ff9800
```

## :material-plus-circle: Adding a Knowledge Base

1. Create a new folder under `resources/knowledge-bases/`
2. Add markdown files with your documentation
3. Rebuild the MCP Docker image: `inv build`

!!! info
    The MCP server automatically indexes all `*.md` files recursively. No configuration needed.

## :material-check-all: Best Practices

!!! tip "Writing for RAG"
    Each chunk should make sense **in isolation** — the AI tool sees only the chunk, not the full file.

- Split large topics into multiple files (~200 lines max per file)
- Use `#`, `##`, `###` headings to create natural chunk boundaries
- Write self-contained sections with descriptive headings
- Headings become part of the search context (e.g., `Design > Security > Zero Trust`)
- Keep sections under 500 characters when possible for optimal search precision
