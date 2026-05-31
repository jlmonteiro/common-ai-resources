---
name: "create-dockerfile"
description: "Generate a Dockerfile following standards. Multi-stage, non-root, health check, labels. Use when user says 'create dockerfile', 'add docker', 'dockerize', 'containerize', or 'create docker image'."
---

# Create Dockerfile

## Prerequisites

Search the following knowledge bases:
- **docker** — Dockerfile standards, image management, multi-stage, security
- Project's language scope — base image selection, build commands

## Step 1: Detect Project

Identify from project files:
- Language and build system
- Entry point (main class, module, binary)
- Dependencies that need build tools vs runtime only
- Port exposed

If unclear, ask:

> "What is the application entry point and which port does it listen on?"

## Step 2: Select Base Images

Based on language:

| Language | Build stage | Runtime stage |
|----------|------------|---------------|
| Java | `gradle:8-jdk21` | `eclipse-temurin:21-jre-alpine` |
| Python | `python:3.11` | `python:3.11-slim` |
| Go | `golang:1.22` | `gcr.io/distroless/static` |
| Node | `node:20` | `node:20-slim` |

Present choice:

> "I'll use `python:3.11` for build and `python:3.11-slim` for runtime. OK?"

## Step 3: Generate Dockerfile

Apply all standards from docker KB:

```dockerfile
# Build stage
FROM {build-image} AS build
WORKDIR /app
COPY {dependency-files} .
RUN {install-dependencies}
COPY {source} .
RUN {build-command}

# Runtime stage
FROM {runtime-image}

LABEL org.opencontainers.image.title="{name}"
LABEL org.opencontainers.image.version="{version}"
LABEL org.opencontainers.image.source="{repo-url}"

RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app
COPY --from=build --chown=appuser:appgroup {artifact} .

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD {health-check-command}

USER appuser
ENTRYPOINT {exec-form-entrypoint}
```

Includes:
- Multi-stage build (separate build from runtime)
- OCI labels
- Non-root user
- Health check
- Exec form entrypoint (graceful shutdown)

## Step 4: Generate .dockerignore

```
.git/
.venv/
__pycache__/
node_modules/
build/
*.md
.env
tests/
docs/
```

## Step 5: Verify

```bash
docker build -t {image-name}:local .
docker run --rm {image-name}:local --version  # or health check
```

## Step 6: Present Summary

```
✓ Dockerfile created

Files:
  - Dockerfile (multi-stage, {build-size} → {runtime-size})
  - .dockerignore

Image: {runtime-image} base
Security: non-root, health check, exec form
Labels: OCI standard

Next steps:
  - Build: docker build -t {name}:local .
  - Add to CI pipeline
  - Create Helm chart: run 'create-helm-chart'
```
