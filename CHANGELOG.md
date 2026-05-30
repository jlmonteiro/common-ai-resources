# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- MCP knowledge base server with semantic search (fastembed + langchain-text-splitters)
- SDD knowledge base (methodology, requirements, design best practices)
- MkDocs Material documentation with Mermaid diagrams
- Python CLI with generate/install adapter commands
- Invoke tasks for build, run, lint, test, docs
- Docker image: ghcr.io/jlmonteiro/common-knowledge-base-mcp
- Project context and documentation guidelines
- GitHub Actions release workflow

### Changed
- ADRs moved from requirements to design documents
- Estimates changed from days to hours in SDD templates
- Chunking strategy: heading-aware splitting (500 chars, 100 overlap)
