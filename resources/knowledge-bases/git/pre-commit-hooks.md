# Pre-Commit Hooks

## Project Configuration

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
        args: [feat, fix, docs, refactor, test, chore, perf, style, ci, build, revert, release]
```

## Automated vs AI-Assisted Checks

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

## Rules

- Never skip hooks (`--no-verify`) unless you have a specific reason
- Keep hooks fast — move slow checks (full test suite) to CI
- Run `pre-commit autoupdate` periodically for security fixes
