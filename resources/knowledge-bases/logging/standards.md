# Logging Standards

## Format: Structured JSON

All logs must be structured JSON in production — never plain text. This enables machine parsing, indexing, and querying in log aggregation systems (ELK, Loki, CloudWatch, Datadog).

```json
{
  "timestamp": "2026-05-30T21:00:00.123Z",
  "level": "INFO",
  "logger": "com.example.UserService",
  "message": "User created",
  "traceId": "abc123",
  "spanId": "def456",
  "userId": "user-789",
  "service": "user-service",
  "environment": "production"
}
```

For local development, support human-readable plain text format. Switch via environment variable:

```
LOG_FORMAT=json    → structured JSON (default in production/containers)
LOG_FORMAT=text    → human-readable (default in local development)
```

## Log Levels

| Level | Use for | Examples |
|-------|---------|---------|
| ERROR | Failures requiring immediate attention | Unhandled exceptions, data corruption, critical dependency down |
| WARN | Recoverable issues that may need investigation | Retry succeeded, fallback used, deprecated API called |
| INFO | Business events and state transitions | User created, order completed, deployment started |
| DEBUG | Development and troubleshooting detail | Method entry/exit, variable values, query parameters |
| TRACE | Extremely verbose (rarely used in production) | Full request/response bodies, loop iterations |

**Rules:**

- Production runs at INFO level by default
- DEBUG is enabled per-service for troubleshooting (never globally)
- ERROR must always include the exception/stack trace
- WARN must explain what happened and what was done about it

## Required Fields

Every log entry must include:

| Field | Purpose |
|-------|---------|
| `timestamp` | ISO 8601 with milliseconds and UTC |
| `level` | Log level |
| `logger` | Class/module that produced the log |
| `message` | Human-readable description |
| `service` | Application/service name |
| `environment` | Deployment environment (dev, staging, production) |

## Tracing Context

Include distributed tracing IDs in every log for correlation:

| Field | Purpose |
|-------|---------|
| `traceId` | End-to-end request identifier (shared across services) |
| `spanId` | Current operation identifier |
| `requestId` | Unique ID for the incoming HTTP request |

This enables correlating logs across microservices for a single user request.

## Contextual Enrichment (MDC)

Use MDC (Mapped Diagnostic Context) or equivalent to enrich logs with request-scoped data:

- `userId` — authenticated user
- `tenantId` — multi-tenant systems
- `correlationId` — business process identifier
- `requestPath` — HTTP path being served

Set at request entry, clear at request exit. All logs within the request automatically include these fields.

## What to Log

### Always Log

- Authentication events (login, logout, failed attempts)
- Authorization failures (access denied)
- Business state transitions (order created, payment processed)
- External service calls (request sent, response received, duration)
- Errors and exceptions with full context
- Application startup and shutdown
- Configuration loaded (without secret values)

### Never Log

- Passwords, tokens, API keys, or secrets
- Full credit card numbers (mask: `****1234`)
- Personal data beyond what's needed (GDPR)
- Request/response bodies in production at INFO level (use DEBUG)
- Health check requests (noise)
- Successful authentication tokens

## Security & Auditability

### Audit Trail

Security-sensitive operations must produce audit logs with:

- **Who** — user identity (userId, IP address)
- **What** — action performed
- **When** — timestamp
- **Where** — service, endpoint
- **Outcome** — success or failure with reason

### Log Injection Prevention

- Sanitize user input before including in log messages
- Never interpolate raw user input into log strings
- Use parameterized logging: `log.info("User {} created", userId)` — not string concatenation

### Retention

- Application logs: minimum 30 days
- Audit logs: minimum 90 days (or per compliance requirements)
- Security event logs: minimum 1 year

## Performance

- Log asynchronously — never block the request thread on log I/O
- Avoid logging in tight loops
- Use lazy evaluation for expensive log messages: `log.debug("Result: {}", () -> expensiveComputation())`
- Don't log large objects at INFO level — use DEBUG with size limits

## Cloud-Friendly Practices

- Write to stdout/stderr — let the platform handle collection
- Never write to local files in containerized environments
- Use JSON format for automatic parsing by log aggregators
- Include service metadata (name, version, instance) for filtering
- Tag logs with deployment info for canary/blue-green correlation
