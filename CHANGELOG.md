# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-06-01

### Added
- UI knowledge base with Markdown-UI DSL schema reference and conventions
- `create-ui-mockup` skill for generating `.ui.md` wireframes
- `sync-ui-spec` skill for two-way binding between wireframes and code

## [1.0.1] - 2026-06-01

### Fixed
- Kiro adapter generates incomplete agent JSON missing tools, allowedTools, and toolsSettings
- Install next steps now remind users to review permissions and add agent description

## [1.0.0]

### Added
- CLI `install` command with adapters for Kiro, Claude Code, and Gemini CLI
- Kiro adapter: generates agent.json, prompt.md, copies skills and knowledge bases
- Claude adapter: generates .mcp.json, .claude/settings.json, .claude-skills/, CLAUDE.md
- Gemini adapter: generates .gemini/settings.json, .gemini/skills/, GEMINI.md
- Resource registry with `importlib.resources` for package distribution
- Rich terminal output with ANSI colors, emoji icons, and directory tree
- `--dry-run` flag to preview generated files without writing
- Scope restriction in Claude/Gemini prompts (MCP serves all, prompt limits)
- CLI documentation with architecture diagrams, per-tool pages, and install instructions
- 12 new BDD test scenarios for CLI (45 total tests, 97% coverage)

### Changed
- Resources bundled as package data for `pipx install` support

## [0.4.0] - 2026-05-31

### Added
- Diagnose skill (disciplined bug troubleshooting: reproduce → hypothesise → instrument → fix)
- SDD skills: create-requirements, create-design, create-tasks, review-specification, list-specifications
- Code review skill (11 review areas, sub-agent/sequential modes, stack-adaptive scopes)
- Review skill (validate and simulate skills step by step)
- Create project skill (interactive scaffolding with Gradle, Docker, Helm, CI/CD)
- Create API endpoint skill (API First, OAS before code, TDD)
- Create test skill (auto-detects test type, proposes scenarios, BDD structure)
- Security audit skill (7 audit areas, severity classification, TDD remediation)
- Create migration skill (expand-contract pattern, rollback, Testcontainers verification)
- Create Helm chart skill (full chart scaffold with security, probes, network policies)
- Create Dockerfile skill (multi-stage, non-root, health check, OCI labels)
- Performance review skill (N+1 detection, caching gaps, I/O optimization)

### Changed
- SDD templates: removed MkDocs-specific `{: #id }` anchors (use standard heading links)
- Skills documentation: 22 pages with rich examples, mermaid flows, admonitions, grid layouts

## [0.3.0] - 2026-05-31

### Added
- Security standards knowledge base (auth, authorization, secrets, input validation, data protection, headers)
- Observability standards knowledge base (RED/USE methods, tracing, health checks, alerting, dashboards)
- Resilience standards knowledge base (circuit breaker, retry, timeout, bulkhead, fallback, ordering)
- Kubernetes standards knowledge base (resource dimensioning, scaling, security, namespaces, resilience)
- Grid layouts with icons on all KB documentation pages

### Changed
- MCP tool descriptions improved for agent discoverability (server purpose, usage guidance)

## [0.2.0] - 2026-05-30

### Added
- Multi-platform Docker builds (linux/amd64 + linux/arm64)
- Java knowledge base (coding standards, Spring Boot conventions)
- Java observability, resilience, and caching knowledge bases
- MCP server: scope filtering for search (`list_scopes`, `scopes` parameter)
- BDD test suite with pytest-bdd (22 scenarios covering chunking, search, scopes)
- Test coverage and HTML reports (`inv test`)
- Testing knowledge base (language-agnostic: TDD, BDD, test pyramid, mocking rules, Testcontainers)
- REST API standards knowledge base (API First, URL design, status codes, resilience, RFC 7807, pagination, versioning, OAS)
- Logging standards knowledge base (structured JSON, levels, tracing, audit, security, cloud-friendly)
- Security standards knowledge base (auth, authorization, secrets, input validation, data protection, headers)
- Observability standards knowledge base (RED/USE methods, tracing, health checks, alerting, dashboards)
- Resilience standards knowledge base (circuit breaker, retry, timeout, bulkhead, fallback, ordering)

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
