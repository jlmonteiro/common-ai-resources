# Agents

Canonical agent definitions in YAML format. Each agent has a tool-agnostic definition
that adapters transform into tool-specific configurations.

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
