"""MCP server that exposes knowledge bases via semantic search."""

import os
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from mcp.server.fastmcp import FastMCP

from common_ai import __version__

KB_PATH = Path(os.environ.get("KB_PATH", "/data"))
MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

mcp = FastMCP("common-knowledge-base-mcp", version=__version__)

_model = None
_chunks = []
_embeddings = None

_md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
)
_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " "],
)


def _get_model():
    global _model
    if _model is None:
        _model = TextEmbedding(MODEL_NAME)
    return _model


def _chunk_file(path: Path) -> list[dict]:
    """Split a markdown file into chunks using heading-aware + recursive splitting."""
    text = path.read_text(encoding="utf-8")
    source = str(path.relative_to(KB_PATH))
    scope = path.relative_to(KB_PATH).parts[0] if len(path.relative_to(KB_PATH).parts) > 1 else "general"

    md_docs = _md_splitter.split_text(text)
    chunks = []

    for doc in md_docs:
        headers = " > ".join(doc.metadata.values()) if doc.metadata else ""
        content = f"{headers}\n\n{doc.page_content}" if headers else doc.page_content

        if len(content) <= CHUNK_SIZE:
            chunks.append({"text": content, "source": source, "scope": scope})
        else:
            sub_chunks = _text_splitter.split_text(content)
            for sub in sub_chunks:
                chunks.append({"text": sub, "source": source, "scope": scope})

    return chunks


def _build_index():
    global _chunks, _embeddings
    if _chunks:
        return

    for md_file in KB_PATH.rglob("*.md"):
        _chunks.extend(_chunk_file(md_file))

    if not _chunks:
        return

    model = _get_model()
    texts = [c["text"] for c in _chunks]
    _embeddings = np.array(list(model.embed(texts)))


@mcp.tool()
def search_knowledge(query: str, scopes: list[str] | None = None, limit: int = 5) -> str:
    """Search software engineering knowledge bases covering coding standards,
    architecture patterns, DevOps conventions, and best practices.

    Use list_scopes first to discover available topics (e.g., java, docker, git, helm, sdd).
    Filter with scopes to get relevant results for the current project's tech stack.

    Args:
        query: The search query.
        scopes: Optional list of scopes to filter results. Use list_scopes to see available options.
        limit: Maximum number of results to return (default 5).
    """
    _build_index()

    if not _chunks:
        return "No knowledge base documents found."

    if scopes:
        available = set(c["scope"] for c in _chunks)
        invalid = set(scopes) - available
        if invalid:
            return f"Invalid scope(s): {', '.join(sorted(invalid))}. Available: {', '.join(sorted(available))}"

    model = _get_model()
    query_embedding = np.array(list(model.embed([query])))
    scores = np.dot(_embeddings, query_embedding.T).flatten()

    if scopes:
        scope_set = set(scopes)
        for i, chunk in enumerate(_chunks):
            if chunk["scope"] not in scope_set:
                scores[i] = -1

    top_indices = np.argsort(scores)[::-1][:limit]

    results = []
    for i in top_indices:
        if scores[i] < 0.1:
            break
        results.append(f"**[{_chunks[i]['source']}]** (score: {scores[i]:.3f})\n\n{_chunks[i]['text']}")

    return "\n\n---\n\n".join(results) if results else "No relevant results found."


@mcp.tool()
def list_scopes() -> str:
    """List available knowledge base scopes (e.g., java, docker, git, helm, sdd).

    Call this first to discover what topics are available, then pass relevant
    scopes to search_knowledge to filter results for your project's tech stack.
    """
    _build_index()

    scopes = sorted(set(c["scope"] for c in _chunks))
    return "\n".join(f"- {s}" for s in scopes) if scopes else "No scopes found."


@mcp.tool()
def list_knowledge_bases() -> str:
    """List all knowledge base topics with their directory names.

    Each topic contains markdown documents covering conventions, standards,
    and best practices for that area of software engineering.
    """
    topics = set()
    for md_file in KB_PATH.rglob("*.md"):
        rel = md_file.relative_to(KB_PATH)
        if len(rel.parts) > 1:
            topics.add(rel.parts[0])
        else:
            topics.add(rel.stem)
    return "\n".join(f"- {t}" for t in sorted(topics)) if topics else "No knowledge bases found."


if __name__ == "__main__":
    mcp.run(transport="stdio")
