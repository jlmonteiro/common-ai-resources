# Common AI Resources

Shared AI resources with multi-tool adapters for Kiro CLI, Claude Code, and Gemini CLI.

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
