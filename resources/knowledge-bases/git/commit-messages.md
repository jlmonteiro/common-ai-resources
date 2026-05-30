# Commit Messages

## Conventional Commits

This project follows [Conventional Commits](https://www.conventionalcommits.org/) (v1.0.0).

## Format

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

The scope is optional — use it when it adds clarity about which part of the project was affected (e.g., `mcp`, `sdd`, `cli`, `docs`).

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

### Version Impact

Only `feat`, `fix`, and `perf` affect the user-facing artifact — they change what the user gets. The rest are internal changes that don't warrant a new version on their own.

Non-release types accumulate on `main` and ship with the next version bump:

```
v0.1.0
  ├── docs: update MCP setup guide        ← no release
  ├── chore: upgrade ruff to 0.12         ← no release
  ├── refactor: simplify chunking logic   ← no release
  ├── feat: add Kubernetes knowledge base ← triggers v0.2.0
```

All internal changes get included in the `v0.2.0` release notes, but they didn't individually justify a new version.

## Rules

- Subject line: imperative mood, lowercase, no period, max 72 chars
- Body: explain what and why, not how (wrap at 72 chars)
- Footer: reference issues, breaking changes
- Breaking changes: add `!` after type or `BREAKING CHANGE:` in footer

## Examples

**Simple:**

```
feat: add semantic search to MCP server
```

**With scope:**

```
fix(mcp): handle empty knowledge-bases directory
```

**With body:**

```
refactor(sdd): move ADRs from requirements to design

ADRs are technical decisions that belong in design documents.
Requirements should focus on what the system must do, not how.
```

**Breaking change:**

```
feat(cli)!: rename generate command to build

BREAKING CHANGE: The `generate` command is now `build`.
Update any scripts that reference `common-ai generate`.
```

**With issue reference:**

```
fix(mcp): prevent crash on malformed markdown

Closes #42
```

## Anti-Patterns

- ❌ `fix stuff` — no type, vague subject
- ❌ `Fixed the bug in the MCP server.` — past tense, period, too long
- ❌ `feat: Add new feature and fix bug and update docs` — multiple concerns
- ❌ `WIP` — never commit work-in-progress to shared branches
