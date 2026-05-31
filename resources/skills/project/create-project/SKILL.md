---
name: "create-project"
description: "Scaffold a new project with proper structure, build system, dotfiles, and tooling. Heavily interactive — asks the user about every decision. Use when user says 'create project', 'new project', 'scaffold project', 'init project', or 'start a new project'."
---

# Create Project

## Prerequisites

Search the following knowledge bases for conventions:
- **git** — dotfiles, branching, pre-commit hooks
- **gradle** — project structure, version catalog (if multi-module)
- **docker** — Dockerfile standards (if containers needed)
- **helm** — chart conventions (if K8s deployment needed)

## Step 1: Gather Project Identity

Ask the user:

1. "What is the project name?" (kebab-case)
2. "Brief description — what does this project do?"
3. "Who is the author/team?"
4. "License? (Apache 2.0, MIT, proprietary, none)"

## Step 2: Determine Tech Stack

Ask one at a time — do not assume:

1. "What language(s)? (Java, Python, Go, TypeScript, multi-language)"
2. "What framework? (Spring Boot, FastAPI, Express, none)"
3. "Single module or multi-module project?"
   - If multi-module or multi-language: "Gradle will be used as the build system (supports polyglot projects). OK?"

## Step 3: Build System

Based on answers:

**Single-language Python:**
- `pyproject.toml` with hatchling

**Single-language Java/Kotlin:**
- Gradle with Kotlin DSL, version catalog

**Multi-module / multi-language:**
- Gradle with Kotlin DSL
- `settings.gradle.kts` with module includes
- `gradle/libs.versions.toml` for version catalog
- Gradle wrapper

Ask: "What modules do you need? (e.g., api, worker, deployment)"

## Step 4: Infrastructure Decisions

Ask each explicitly:

1. "Do you need Docker containers?" (Yes/No)
   - If yes: create Dockerfile following docker KB standards
2. "Do you need Kubernetes deployment?" (Yes/No)
   - If yes: "Helm chart or plain manifests?" → create following helm/k8s KB
3. "Do you need a CI/CD pipeline?" (Yes/No)
   - If yes: "GitHub Actions or GitLab CI?" → create workflow files
4. "Do you need a database?" (Yes/No)
   - If yes: "Which? (PostgreSQL, MySQL, MongoDB)" → add to docker-compose, add migration tool

## Step 5: Documentation

Ask:

1. "How do you want to document the project?"
   - MkDocs Material (full documentation site)
   - Plain markdown in `docs/` folder
   - README only

2. "Do you want a changelog?" (Yes/No) → create CHANGELOG.md

## Step 6: Quality Tooling

Ask:

1. "Do you want pre-commit hooks?" (Yes/No)
   - If yes: create `.pre-commit-config.yaml` following git/pre-commit-hooks KB
2. "Do you want linting configured?" (Yes/No)
   - If yes: configure based on language (ruff for Python, checkstyle for Java)
3. "Do you want test coverage reporting?" (Yes/No)

## Step 7: Create Project Structure

Based on all answers, scaffold:

### Always created:
- `README.md` — project name, description, badges, getting started
- `.gitignore` — language-appropriate patterns
- `.gitattributes` — line endings, binary files
- `.editorconfig` — formatting rules
- `project-context.md` — tech stack, conventions, commands
- `CHANGELOG.md` (if requested)
- `LICENSE` (if requested)

### Language-specific:
- Build files (`pyproject.toml`, `build.gradle.kts`, `package.json`)
- Source directory structure
- Test directory structure

### Infrastructure (if requested):
- `Dockerfile` / `docker-compose.yml`
- Helm chart / K8s manifests
- CI/CD workflow files

### Tooling (if requested):
- `.pre-commit-config.yaml`
- Linter configuration
- Coverage configuration

## Step 8: Initialize Git

```bash
git init
git add -A
git commit -m "feat: initial project scaffold"
```

## Step 9: Present Summary

```
✓ Project created: {name}

Structure:
  {tree output}

Build: {build system}
Language: {language}
Framework: {framework}
Infrastructure: {docker, helm, CI}
Documentation: {type}
Tooling: {pre-commit, linter, coverage}

Next steps:
- Review project-context.md
- Run 'create requirements' to start specifying features
- Push to remote: git remote add origin <url> && git push -u origin main
```
