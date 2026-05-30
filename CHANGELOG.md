# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## 0.0.1 - 2026-05-30

### Added
- Initial project scaffold with Python CLI and multi-tool adapter architecture
- MCP knowledge base server with semantic search (fastembed + langchain-text-splitters)
- SDD knowledge base (methodology, requirements, design best practices)
- AI skills knowledge base (skills development guidelines, agent steering)
- Release management knowledge base with versioning guidelines
- Changelog management skill (`update-changelog`)
- MkDocs Material documentation with Mermaid diagrams, dark/light toggle, tabs, grid cards
- Python CLI with generate/install adapter commands
- Invoke tasks for build, run, lint, test, docs, version, release
- Docker image: ghcr.io/jlmonteiro/common-knowledge-base-mcp
- Project context with documentation and coding guidelines
- GitHub Actions release workflow (creates release on tag push)
- CHANGELOG.md following Keep a Changelog format
- Version sync across pyproject.toml, Python package, MCP server, Docker tag, and git tag

### Changed
- ADRs moved from requirements to design documents
- Estimates changed from days to hours in SDD templates
- Chunk strategy: heading-aware splitting (500 chars, 100 overlap) via langchain-text-splitters
- Image name standardized to ghcr.io/jlmonteiro/common-knowledge-base-mcp
