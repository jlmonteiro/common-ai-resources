# Release Management

## Versioning

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0) — breaking changes to CLI, MCP tools, or canonical formats
- **MINOR** (0.x.0) — new features, new knowledge bases, new adapters
- **PATCH** (0.0.x) — bug fixes, documentation updates, minor improvements

## Version Source of Truth

The version is defined in `pyproject.toml` under `[project]`:

```toml
version = "0.1.0"
```

All other version references are derived from this single source:

- Python package (`__version__`)
- MCP server (reported in initialize response)
- Docker image tag (`ghcr.io/jlmonteiro/common-knowledge-base-mcp:0.1.0`)
- Git tag (`v0.1.0`)

## Changelog

### Format

The changelog follows [Keep a Changelog](https://keepachangelog.com/) format in `CHANGELOG.md`.

### Categories

| Category | Use for |
|----------|---------|
| **Added** | New features, new knowledge bases, new tools |
| **Changed** | Modifications to existing functionality |
| **Deprecated** | Features that will be removed in future versions |
| **Removed** | Features removed in this release |
| **Fixed** | Bug fixes |
| **Security** | Vulnerability fixes |

### Rules

- Always add entries under `[Unreleased]` during development
- One entry per logical change — not per commit
- Write from the user's perspective: what changed for them
- Use imperative mood: "Add", "Fix", "Change" — not "Added", "Fixed"
- Include issue/PR references when applicable

### Example Entry

```markdown
## [Unreleased]

### Added
- Kubernetes knowledge base with cluster connection guidelines
- `inv push` task for publishing Docker image to GHCR

### Fixed
- MCP server crash when knowledge-bases directory is empty
```

## Release Process

### Commands

```bash
inv version              # Show current version
inv release              # Bump patch (0.1.0 → 0.1.1), commit, tag
inv release --part=minor # Bump minor (0.1.0 → 0.2.0), commit, tag
inv release --part=major # Bump major (0.1.0 → 1.0.0), commit, tag
```

### What `inv release` Does

1. Bumps version in `pyproject.toml`
2. Commits the change with message `release: vX.Y.Z`
3. Creates git tag `vX.Y.Z`

### What Happens on Push

When the tag is pushed to GitHub:

1. GitHub Actions workflow triggers on `v*` tags
2. Extracts the changelog section for this version
3. Creates a GitHub Release with the changelog as body

### Pre-Release Checklist

Before running `inv release`:

- [ ] All changes are committed
- [ ] `inv lint` passes
- [ ] `inv test` passes
- [ ] `inv build` succeeds
- [ ] `CHANGELOG.md` has entries under `[Unreleased]`
- [ ] Move `[Unreleased]` entries to `[X.Y.Z] - YYYY-MM-DD` section

### Post-Release

After pushing the tag:

- [ ] Verify GitHub Release was created
- [ ] Build and push Docker image with new version tag
- [ ] Update documentation if needed
