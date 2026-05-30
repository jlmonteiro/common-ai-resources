# Common AI Resources

Shared AI resources with multi-tool adapters for Kiro CLI, Claude Code, and Gemini CLI.

## Concept

Define your AI resources (agents, prompts, skills, knowledge bases) once in a
canonical, tool-agnostic format. Use adapters to generate configurations for
each specific AI assistant.

## Supported Tools

| Tool | Output Format |
|------|---------------|
| Kiro CLI | `agent.json`, `SKILL.md`, knowledge base configs |
| Claude Code | `CLAUDE.md`, `.claude/` directory |
| Gemini CLI | `GEMINI.md`, `.gemini/` configuration |

## Quick Start

```bash
pip install -e ".[dev,docs]"
common-ai generate --target kiro
common-ai install --target kiro
```
