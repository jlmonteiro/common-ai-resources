# Image Management Standards

## Naming Convention

```
<registry>/<namespace>/<image-name>:<tag>
```

## Tag Strategy

### Production

| Tag | Purpose | Mutable? |
|-----|---------|----------|
| `X.Y.Z` | Specific release version | No (immutable) |
| `latest` | Most recent stable release | Yes |

Always apply both on release:

```bash
docker build -t <image>:1.2.3 -t <image>:latest .
```

### Development

| Tag | Purpose |
|-----|---------|
| `latest` | Latest build from main |
| `<branch-name>` | Feature branch build |
| `<sha>` | Specific commit (CI traceability) |

### Rules

- Production tags are immutable — never overwrite a versioned tag
- Use SemVer for release tags (must match git tags)
- `latest` is always mutable

## Docker Compose Standards

### Service Dependencies

Always use `condition: service_healthy` for infrastructure services. Every infrastructure service must define a `healthcheck`:

```yaml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5
```

| Condition | Use when |
|-----------|----------|
| `service_started` | Service just needs to be running |
| `service_healthy` | Service must be ready to accept connections |
| `service_completed_successfully` | Init/setup containers that run once |

### Networks

Use custom networks to isolate service groups when the Compose file has 3+ services:

```yaml
services:
  app:
    networks: [frontend, backend]
  postgres:
    networks: [backend]
  nginx:
    networks: [frontend]

networks:
  frontend:
  backend:
```

Services can only communicate if they share a network.

### Volumes

- Named volumes for persistence (databases, caches)
- Bind mounts only for development (live reload)
- Never share database volumes between containers

### Environment Overrides

Use `docker-compose.override.yml` for local development (auto-loaded, not committed):

```yaml
services:
  app:
    build: .
    volumes:
      - ./src:/app/src
    environment:
      - APP_ENV=development
```
