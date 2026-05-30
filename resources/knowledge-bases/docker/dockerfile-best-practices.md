# Dockerfile Standards

## Required Practices

All projects must follow these standards for Docker images.

### Multi-Stage Builds

Always separate build from runtime. The final image must not contain build tools, compilers, or source code beyond what's needed to run.

```dockerfile
# Build stage — full image with build tools
FROM python:3.11 AS build
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY src/ src/

# Runtime stage — slim image, only runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=build /app /app
ENTRYPOINT ["python", "-m", "my_app"]
```

### Base Images

- Always pin the version — never use `latest`
- Use `-slim` variants as the default
- Only use Alpine if all dependencies are verified compatible (musl libc breaks C extensions like numpy, pandas, cryptography)

### Layer Caching

Order instructions from least to most frequently changing. Dependencies before source code — avoids re-downloading packages on every code change.

```dockerfile
COPY pyproject.toml .        # changes occasionally
RUN pip install --no-cache-dir .
COPY src/ src/               # changes frequently
```

### Minimize Layers

Combine commands and clean up in the same `RUN`. Files in a layer are permanent — deleting in a later layer doesn't reduce image size.

```dockerfile
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*
```

### Security

- Run as non-root user in all production images
- Never bake secrets into images (use runtime injection)
- Scan images for vulnerabilities before publishing

```dockerfile
RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser
```

### Runtime

- Always use exec form for `ENTRYPOINT` (enables graceful shutdown via SIGTERM)
- Always include a `HEALTHCHECK` instruction
- Add OCI labels for metadata

```dockerfile
ENTRYPOINT ["python", "-m", "my_app"]

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

LABEL org.opencontainers.image.title="<name>"
LABEL org.opencontainers.image.version="<version>"
LABEL org.opencontainers.image.source="<repo-url>"
```

### .dockerignore

Every project with a Dockerfile must have a `.dockerignore`. At minimum:

```
.git/
.venv/
__pycache__/
*.pyc
tests/
docs/
.env
```

### Performance

- Use `--no-cache-dir` for pip installs
- Pre-download large assets (models, data) at build time to avoid startup latency
