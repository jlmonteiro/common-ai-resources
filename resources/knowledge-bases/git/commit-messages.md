# Commit Message Conventions

## Format

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

Scope is optional — use when it adds clarity (e.g., `mcp`, `sdd`, `cli`, `docs`).

## Types

| Type | Purpose | Triggers Release? |
|------|---------|-------------------|
| `feat` | New feature | Yes (MINOR) |
| `fix` | Bug fix | Yes (PATCH) |
| `perf` | Performance improvement | Yes (PATCH) |
| `docs` | Documentation only | No |
| `refactor` | Code change that neither fixes nor adds | No |
| `test` | Adding or correcting tests | No |
| `chore` | Maintenance, tooling | No |
| `style` | Formatting, whitespace (no logic change) | No |
| `ci` | CI/CD configuration changes | No |
| `build` | Build system or dependencies | No |
| `revert` | Reverts a previous commit | No |

## Version Impact

Only `feat`, `fix`, and `perf` affect the user-facing artifact. Non-release types accumulate on `main` and ship with the next version bump:

```
v0.1.0
  ├── docs: update MCP setup guide        ← no release
  ├── chore: upgrade ruff to 0.12         ← no release
  ├── refactor: simplify chunking logic   ← no release
  ├── feat: add Kubernetes knowledge base ← triggers v0.2.0
```

## Rules

- Subject: imperative mood, lowercase, no period, max 72 chars
- Body: explain what and why, not how
- Breaking changes: add `!` after type or `BREAKING CHANGE:` in footer
