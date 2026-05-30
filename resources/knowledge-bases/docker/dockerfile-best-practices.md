# Dockerfile Conventions

## Base Image Selection

- Use `python:3.11-slim` as the default base image
- Never use `latest` — always pin the version
- Only use Alpine if all dependencies are verified compatible (musl libc breaks C extensions)

## Required Practices

- Multi-stage builds for all production images (separate build from runtime)
- Run as non-root user in production
- Use `--no-cache-dir` for pip installs
- Pre-download large assets (models, data) at build time to avoid startup latency
- Always include a `HEALTHCHECK` instruction
- Use exec form for `ENTRYPOINT` (enables graceful shutdown via SIGTERM)

## Image Structure

```dockerfile
FROM python:3.11-slim

# OCI labels
LABEL org.opencontainers.image.title="<name>"
LABEL org.opencontainers.image.version="<version>"
LABEL org.opencontainers.image.source="https://github.com/jlmonteiro/<repo>"

# Non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app

# Dependencies first (layer caching)
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Source code last
COPY src/ src/

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

USER appuser
ENTRYPOINT ["python", "-m", "my_app"]
```

## .dockerignore

Always include:

```
.git/
.venv/
__pycache__/
*.pyc
tests/
docs/
site/
.env
```

## What NOT to Do

- Don't bake secrets into images (use runtime injection)
- Don't use shell form for ENTRYPOINT (breaks signal handling)
- Don't install build tools in the runtime stage
- Don't skip .dockerignore (causes large build context and potential secret leaks)
