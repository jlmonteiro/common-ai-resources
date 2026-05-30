# Pre-Commit Hooks

## Overview

[pre-commit](https://pre-commit.com/) is a git hooks manager that runs automated checks on every commit. It blocks bad commits before they reach the repository — no manual effort after initial setup.

## How It Works

```
git commit
    │
    ▼
pre-commit runs hooks against staged files
    │
    ├── All pass → commit proceeds
    └── Any fail → commit blocked, fix and retry
```

Hooks are defined in `.pre-commit-config.yaml` at the project root. The file is version-controlled so all contributors get the same checks.

## Configuration Format

```yaml
repos:
  - repo: <github-url-of-hook-collection>
    rev: <version-tag>
    hooks:
      - id: <hook-name>
        args: [optional, arguments]
        stages: [commit-msg]  # optional: which git stage
```

## Common Hooks

### Security

| Hook | Purpose |
|------|---------|
| `detect-private-key` | Blocks commits containing private keys |
| `detect-secrets` (Yelp) | Scans for API keys, tokens, passwords |
| `check-added-large-files` | Prevents accidentally committing large binaries |

### Code Quality

| Hook | Purpose |
|------|---------|
| `ruff-check` | Python linting (fast, replaces flake8/isort) |
| `trailing-whitespace` | Removes trailing whitespace |
| `end-of-file-fixer` | Ensures files end with a newline |
| `check-yaml` | Validates YAML syntax |
| `check-json` | Validates JSON syntax |

### Git Workflow

| Hook | Purpose |
|------|---------|
| `no-commit-to-branch` | Blocks direct commits to `main` |
| `conventional-pre-commit` | Validates commit message format |
| `check-merge-conflict` | Catches unresolved merge conflict markers |

## Setup

One-time per developer:

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

After this, hooks run automatically on every `git commit`.

## Useful Commands

```bash
pre-commit run --all-files    # Run all hooks on entire repo
pre-commit autoupdate         # Update hook versions
pre-commit run <hook-id>      # Run a specific hook
git commit --no-verify        # Skip hooks (emergency only)
```

## Automated vs AI-Assisted Checks

Pre-commit handles fast, deterministic checks. The AI commit skill handles checks requiring judgment.

| Check | Pre-commit (automated) | AI Skill (judgment) |
|-------|----------------------|---------------------|
| Secrets detection | ✅ | — |
| Lint/formatting | ✅ | — |
| Commit message format | ✅ | — |
| Branch protection | ✅ | — |
| Changelog updated | — | ✅ |
| Version consistency | — | ✅ |
| Scope matches changes | — | ✅ |
| Rebase needed | — | ✅ |

## Best Practices

- Commit `.pre-commit-config.yaml` to the repository
- Pin hook versions with `rev:` for reproducibility
- Run `pre-commit autoupdate` periodically to get security fixes
- Never skip hooks (`--no-verify`) unless you have a specific reason
- Keep hooks fast — move slow checks (full test suite) to CI

## Implementation Examples

### Minimal (Security + Formatting)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

### Standard (+ Lint + Branch Protection)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: no-commit-to-branch
        args: ["--branch", "main"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.12
    hooks:
      - id: ruff-check
```

### Full (+ Commit Message Validation)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: no-commit-to-branch
        args: ["--branch", "main"]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.12
    hooks:
      - id: ruff-check

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v4.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
        args: [feat, fix, docs, refactor, test, chore, perf, style, ci, build, revert]
```

### Custom Local Hook

For project-specific checks not available as a published hook:

```yaml
repos:
  - repo: local
    hooks:
      - id: check-changelog
        name: Check changelog has unreleased entries
        entry: grep -q "## \[Unreleased\]" CHANGELOG.md
        language: system
        pass_filenames: false
        always_run: true
```
