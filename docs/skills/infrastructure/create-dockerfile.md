# :material-docker: Create Dockerfile

Generates a Dockerfile — multi-stage, non-root, health check, OCI labels. Auto-detects language.

!!! tip "Triggers"
    - "create dockerfile" / "add docker" / "dockerize" / "containerize"

!!! success "Expected Outcomes"
    - Multi-stage Dockerfile (build + runtime)
    - Non-root user, health check, exec form entrypoint
    - OCI labels, .dockerignore
    - Verified with `docker build`

## Example

!!! example "Scenario: Dockerize a Python FastAPI app"

    **Step 1:** Detects `pyproject.toml`, `src/main.py`, port 8080.

    **Step 2:** "I'll use `python:3.11` for build and `python:3.11-slim` for runtime. OK?"

    User: "Yes"

    **Step 3:** Generates:

    ```dockerfile
    FROM python:3.11 AS build
    WORKDIR /app
    COPY pyproject.toml .
    RUN pip install --no-cache-dir .
    COPY src/ src/

    FROM python:3.11-slim

    LABEL org.opencontainers.image.title="order-service"
    LABEL org.opencontainers.image.version="0.1.0"
    LABEL org.opencontainers.image.source="https://github.com/user/repo"

    RUN addgroup --system appgroup && adduser --system --group appuser
    WORKDIR /app
    COPY --from=build --chown=appuser:appgroup /app /app

    HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
        CMD curl -f http://localhost:8080/health || exit 1

    USER appuser
    ENTRYPOINT ["python", "-m", "main"]
    ```

    **Step 4:** `.dockerignore` generated.

    **Step 5:** `docker build -t order-service:local .` → success (142MB).

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/infrastructure/create-dockerfile/SKILL.md)
