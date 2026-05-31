# Project Context

## Overview

This is a Python-based repository for managing shared AI resources (agents, prompts, skills, knowledge bases) with multi-tool adapters for Kiro CLI, Claude Code, and Gemini CLI.

## Tech Stack

- **Language**: Python 3.11+
- **Build**: pyproject.toml (hatchling), invoke for tasks
- **Documentation**: MkDocs Material
- **Containerization**: Docker (knowledge-base-mcp.dockerfile)
- **Linting**: ruff
- **Testing**: pytest

## Project Structure

- `src/` layout for Python packages
- `resources/` for all AI resources (agents, prompts, skills, knowledge bases)
- `docs/` for MkDocs user documentation
- `tests/` for pytest test files

## Code Style

- All Python code is enforced by ruff (line length 120)
- Follow existing patterns in `src/common_ai/`
- Pin all dependency versions exactly in pyproject.toml
- Run `inv lint` before committing Python changes

## Git Conventions

- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`
- Do not commit secrets, credentials, or API keys
- Keep commits focused — one logical change per commit

## Knowledge Bases

- Markdown files under `resources/knowledge-bases/`
- Keep documents under 200 lines per file
- Use `##` headings as primary chunk boundaries
- Write self-contained sections that make sense in isolation
- Use descriptive headings — they become part of the search context

## Agents and Skills

- Canonical agent definitions use YAML format (`resources/agents/`)
- Skills are defined as Markdown files (`resources/skills/`)
- Both are tool-agnostic — adapters generate tool-specific output

## Documentation

Documentation lives in `docs/` and is built with MkDocs Material.

### Writing Style

- Write for the user, not the developer — explain "how to use", not "how it works internally"
- Use second person ("you") and active voice
- Keep sentences short — one idea per sentence
- Lead with the most important information (inverted pyramid)
- Include practical examples for every concept

### Page Structure

- Start with a one-sentence description of what the page covers
- Use `##` for main sections, `###` for subsections — avoid `####`+
- End with a "Next Steps" or related links section when applicable
- Keep pages focused — one topic per page, split if over 200 lines

### MkDocs Material Features

Use these features to improve readability:

**Admonitions** — for callouts, warnings, tips:

    !!! tip "Performance"
        Use connection pooling for database access.

    !!! warning
        This will delete all data.

    !!! note
        Available since v0.2.0.

**Tabs** — for multi-tool/multi-language examples:

    === "Kiro CLI"
        ```json
        {"name": "my-agent"}
        ```

    === "Claude Code"
        ```markdown
        # CLAUDE.md
        You are my-agent...
        ```

    === "Gemini CLI"
        ```markdown
        # GEMINI.md
        You are my-agent...
        ```

**Code annotations** — for inline explanations:

    ```python
    model = TextEmbedding("BAAI/bge-small-en-v1.5")  # (1)!
    ```

    1. Lightweight ONNX model, ~50MB

**Grid cards** — for feature overviews and navigation:

    <div class="grid cards" markdown>

    - :material-robot: **Agents** — AI persona definitions
    - :material-lightning-bolt: **Skills** — Multi-step workflows
    - :material-book-open: **Knowledge Bases** — RAG documentation
    - :material-console: **MCP Server** — Semantic search API

    </div>

**Icons** — use Material Design icons for visual markers:

    :material-check-circle: Completed
    :material-alert: Warning
    :material-information: Info
    :octicons-rocket-16: New feature

**Mermaid diagrams** — for architecture and flows:

    ```mermaid
    graph LR
        A --> B --> C
    ```

### Formatting Rules

- Tables for structured comparisons (features, options, parameters)
- Bullet lists for sequences or enumerations (max 7 items)
- Code blocks with language annotation for all code/config
- Bold for UI elements and key terms on first use
- Backticks for file names, commands, and inline code

### Admonition Usage Guide

| Type | Use for |
|------|---------|
| `note` | Additional context, background info |
| `tip` | Best practices, recommendations |
| `warning` | Potential pitfalls, breaking changes |
| `danger` | Destructive actions, security risks |
| `example` | Concrete usage examples |
| `info` | Version info, compatibility notes |

## Docker

- Image name: `ghcr.io/jlmonteiro/common-knowledge-base-mcp`
- Dockerfile: `knowledge-base-mcp.dockerfile`
- Keep image size minimal — prefer lightweight dependencies

## Commands

- `inv build` — Build the MCP Docker image
- `inv run` — Run MCP server (STDIO)
- `inv run-dev` — Run MCP server with live-mounted KBs
- `inv lint` — Run ruff linter
- `inv test` — Run pytest
- `inv docs` — Serve MkDocs locally
- `common-ai install --tool <kiro|claude|gemini> --name <agent> --target <dir>` — Install resources to target tool
