# Agents

Canonical agent definitions in YAML format. These are tool-agnostic — the CLI
adapters transform them into tool-specific configurations (Kiro JSON, CLAUDE.md, GEMINI.md).

## Structure

```yaml
# agents/java-developer.yaml
name: java-developer
description: Internal Java development assistant
role: |
  You are a Senior Java Developer...
tools:
  - shell
  - file-read
  - file-write
knowledge_bases:
  - gradle-guidelines
  - repository-auth
skills:
  - commit-push
  - start-story
```
