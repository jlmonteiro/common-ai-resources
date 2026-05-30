# Image Management Conventions

## Naming

```
ghcr.io/jlmonteiro/<image-name>:<tag>
```

## Tag Strategy

| Tag | When | Mutable? |
|-----|------|----------|
| `X.Y.Z` | On release | No (immutable) |
| `latest` | Every build from main | Yes |

Both tags are applied on release:

```bash
docker build -t ghcr.io/jlmonteiro/myapp:1.2.3 -t ghcr.io/jlmonteiro/myapp:latest .
```

## Docker Compose Conventions

### Service Dependencies

Use `condition: service_healthy` for databases and infrastructure services:

```yaml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy
```

Every infrastructure service must define a `healthcheck`:

```yaml
  postgres:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      timeout: 3s
      retries: 5
```

### Networks

Use custom networks to isolate service groups when the Compose file has 3+ services:

```yaml
networks:
  frontend:
  backend:
```

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
