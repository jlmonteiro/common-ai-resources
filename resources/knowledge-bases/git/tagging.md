# Tagging

## Format

Tags follow Semantic Versioning with a `v` prefix:

```
v<MAJOR>.<MINOR>.<PATCH>
```

**Examples:** `v0.1.0`, `v1.0.0`, `v2.3.1`

## When to Tag

- After merging all changes for a release into `main`
- After updating the changelog (`[Unreleased]` → `[X.Y.Z] - date`)
- After bumping the version in `pyproject.toml`

## Tag Types

| Tag | Purpose | Example |
|-----|---------|---------|
| Release | Marks a production release | `v1.2.0` |
| Pre-release | Marks a candidate for testing | `v1.2.0-rc.1` |

## Rules

- Tags are immutable — never delete or move a tag
- Tags trigger CI/CD (GitHub Actions release workflow)
- Only tag commits on `main`
- One tag per release — don't tag intermediate states

## Process

```bash
# Automated via invoke
inv release              # v0.1.0 → v0.1.1
inv release --part=minor # v0.1.0 → v0.2.0
inv release --part=major # v0.1.0 → v1.0.0

# Push tag to trigger release
git push origin main --tags
```

## Version Bumping Rules

| Change | Bump | Example |
|--------|------|---------|
| Breaking change to CLI, MCP tools, or formats | MAJOR | `v1.0.0` → `v2.0.0` |
| New feature, knowledge base, or adapter | MINOR | `v1.0.0` → `v1.1.0` |
| Bug fix, doc update, minor improvement | PATCH | `v1.0.0` → `v1.0.1` |

## Initial Development (0.x.x)

While the major version is `0`, the API is not considered stable:

- MINOR bumps may include breaking changes
- PATCH bumps are bug fixes only
- First stable release is `v1.0.0`
