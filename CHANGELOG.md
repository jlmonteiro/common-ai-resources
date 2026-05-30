# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.1]  - 2026-05-30

### Fixed
- GitHub Release not created after merge (GITHUB_TOKEN tag pushes don't trigger other workflows)
- Merged release creation into post-merge workflow, removed standalone release.yml

## [0.1.0] - 2026-05-30

### Added
- Initial project scaffold with Python CLI and multi-tool adapter architecture
- MCP knowledge base server with semantic search (fastembed + langchain-text-splitters)
- SDD knowledge base (methodology, requirements, design best practices)
- AI knowledge bases (skills development guidelines, agent steering)
- Git knowledge bases (commit messages, branching, PRs, tagging, pre-commit hooks, best practices)
- Helm knowledge base (chart conventions, NOTES.txt, probes, ConfigMaps/Secrets, environment injection)
- Docker knowledge base (Dockerfile standards, image management conventions)
- Gradle knowledge base (conventions, version management)
- Database knowledge base (naming, migrations, schema change conventions)
- Document review skill (interactive item-by-item review)
- Release management knowledge base with versioning guidelines
- Skills: commit, push, create-pr, create-branch, update-changelog
- MkDocs Material documentation with Mermaid diagrams, dark/light toggle, tabs, grid cards
- Python CLI with generate/install adapter commands
- Invoke tasks for build, run, lint, test, docs, version, release
- Docker image: ghcr.io/jlmonteiro/common-knowledge-base-mcp
- Project context with documentation and coding guidelines
- GitHub Actions: CI (lint, test, build on PR), post-merge (docs, tag, Docker publish)
- GitHub Actions release workflow (creates release on tag push)
- CHANGELOG.md following Keep a Changelog format
- Version sync across pyproject.toml, Python package, MCP server, Docker tag, and git tag
- Pre-commit hooks configuration (.pre-commit-config.yaml)

### Changed
- ADRs moved from requirements to design documents
- Estimates changed from days to hours in SDD templates
- Chunk strategy: heading-aware splitting (500 chars, 100 overlap) via langchain-text-splitters
- Image name standardized to ghcr.io/jlmonteiro/common-knowledge-base-mcp
- KB docs link to source files on GitHub (open in new tab)
- Gradle icon updated to Simple Icons `:simple-gradle:`
- README: add badges (CI, Docs, Release, License) and documentation link
- Apache 2.0 license added
