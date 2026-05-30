# Common AI Resources

[![CI](https://github.com/jlmonteiro/common-ai-resources/actions/workflows/ci.yml/badge.svg)](https://github.com/jlmonteiro/common-ai-resources/actions/workflows/ci.yml)
[![Docs](https://github.com/jlmonteiro/common-ai-resources/actions/workflows/post-merge.yml/badge.svg)](https://jlmonteiro.github.io/common-ai-resources/)
[![Release](https://img.shields.io/github/v/release/jlmonteiro/common-ai-resources)](https://github.com/jlmonteiro/common-ai-resources/releases/latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Shared AI resources with multi-tool adapters for Kiro CLI, Claude Code, and Gemini CLI.

📖 **Full documentation:** https://jlmonteiro.github.io/common-ai-resources/

## Architecture

Define resources once in a canonical format, generate tool-specific configurations via adapters.

```
common-ai-resources/
├── resources/
│   ├── agents/          # Canonical agent definitions (YAML)
│   ├── prompts/         # Shared prompt templates
│   ├── skills/          # Workflow definitions (tool-agnostic)
│   ├── knowledge-bases/ # Documentation (universal markdown)
│   └── scripts/         # Utility scripts
├── src/common_ai/       # Python CLI + adapters
│   ├── cli.py           # CLI entry point
│   └── adapters/        # Per-tool generators
│       ├── kiro.py      # → agent.json, SKILL.md
│       ├── claude_code.py # → CLAUDE.md, .claude/
│       └── gemini.py    # → GEMINI.md, .gemini/
├── tests/
├── docs/                # MkDocs documentation
└── pyproject.toml
```

## Usage

```bash
# Install in development mode
pip install -e ".[dev,docs]"

# Generate tool-specific configs
common-ai generate --target kiro
common-ai generate --target claude-code --agent java-developer

# Install to target tool's location
common-ai install --target kiro

# Serve documentation
mkdocs serve
```

## Build

```bash
# Install dev dependencies
pip install -e ".[dev,docs]"

# Build MCP knowledge base Docker image
inv build

# Run MCP server
inv run

# Run MCP server with live-mounted knowledge bases (development)
inv run-dev

# Lint code
inv lint

# Run tests
inv test

# Serve documentation
inv docs
```

## MCP Server

The knowledge base MCP server provides semantic search over all resources via STDIO.

Add to your AI tool's MCP config:

```json
{
  "mcpServers": {
    "common-knowledge-base-mcp": {
      "command": "docker",
      "args": ["run", "-i", "ghcr.io/jlmonteiro/common-knowledge-base-mcp"]
    }
  }
}
```
