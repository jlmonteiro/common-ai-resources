# :material-lightning-bolt: Skills

Skills are structured instruction sets that guide AI assistants through multi-step workflows. Unlike knowledge bases (which provide reference information), skills define **how** to execute a task — step by step, with decision points, validations, and user interactions.

Skills follow a "Discovery vs Activation" pattern: the AI assistant knows a skill exists (by reading its name and description), but only loads the full instructions when your prompt matches the skill's intent. This saves context window space and keeps responses focused on the task at hand.

All skills in this repository are tool-agnostic — they work with any AI assistant that supports the SKILL.md standard (Kiro CLI, Claude Code, Cursor, and others). They reference knowledge bases for conventions and standards rather than duplicating content, ensuring consistency across all workflows.

## Git Workflow

| Skill | Purpose |
|-------|---------|
| [Create Branch](git/create-branch.md) | Start a new branch with proper naming and version bump |
| [Commit](git/commit.md) | Commit with pre-commit checks, changelog, and validation |
| [Push](git/push.md) | Push with pre-merge checks (lint, tests, rebase, Docker) |
| [Create PR](git/create-pr.md) | Create a pull request with proper title and description |

## Specification-Driven Development

| Skill | Purpose |
|-------|---------|
| [Create Requirements](sdd/create-requirements.md) | Gather and document requirements with EARS syntax |
| [Create Design](sdd/create-design.md) | Create design documents with ADRs and test scenarios |
| [Create Tasks](sdd/create-tasks.md) | Break down into user stories with hour estimates |
| [Review Specification](sdd/review-specification.md) | Audit specs for gaps and quality |
| [List Specifications](sdd/list-specifications.md) | Show current specification status |

## Development

| Skill | Purpose |
|-------|---------|
| [Code Review](development/code-review.md) | Comprehensive review with 11 areas, stack-adaptive |
| [Create API Endpoint](development/create-api-endpoint.md) | API First — OAS before code, TDD |
| [Create Test](development/create-test.md) | Generate tests with BDD structure and scenario proposals |
| [Performance Review](development/performance-review.md) | Find bottlenecks, N+1 queries, caching gaps |
| [Review Skill](development/review-skill.md) | Validate and simulate a skill step by step |

## Infrastructure

| Skill | Purpose |
|-------|---------|
| [Create Dockerfile](infrastructure/create-dockerfile.md) | Multi-stage, non-root, health check, OCI labels |
| [Create Helm Chart](infrastructure/create-helm-chart.md) | Full chart with security, probes, network policies |

## Security

| Skill | Purpose |
|-------|---------|
| [Security Audit](security/audit.md) | Deep security review across 7 areas |

## Database

| Skill | Purpose |
|-------|---------|
| [Create Migration](database/create-migration.md) | Expand-contract pattern, rollback, tested |

## Debugging

| Skill | Purpose |
|-------|---------|
| [Diagnose](debugging/diagnose.md) | 6-phase bug troubleshooting methodology |

## Release

| Skill | Purpose |
|-------|---------|
| [Update Changelog](release/update-changelog.md) | Add entries following Keep a Changelog format |

## Documentation

| Skill | Purpose |
|-------|---------|
| [Review Document](document/review.md) | Interactive item-by-item document review |

## Project

| Skill | Purpose |
|-------|---------|
| [Create Project](project/create-project.md) | Interactive project scaffolding |
