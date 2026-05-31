# Observability Standards

## Three Pillars

Every service must implement all three:

| Pillar | Purpose | Answers |
|--------|---------|---------|
| **Metrics** | Quantitative health monitoring | "Is the system healthy? How fast? How many errors?" |
| **Tracing** | Request flow across services | "Where did this request go? What's slow?" |
| **Logging** | Event details for debugging | "What happened? Why did it fail?" |

## Metrics

### RED Method (for services)

Every service must expose:

| Metric | What it measures |
|--------|-----------------|
| **Rate** | Requests per second |
| **Errors** | Failed requests per second |
| **Duration** | Response time distribution (p50, p95, p99) |

### USE Method (for infrastructure)

| Metric | What it measures |
|--------|-----------------|
| **Utilization** | How busy the resource is (CPU %, memory %) |
| **Saturation** | Queue depth, pending work |
| **Errors** | Resource errors (disk failures, OOM kills) |

### Naming Conventions

- Use dot notation: `<service>.<component>.<metric>` (e.g., `orders.payment.duration`)
- Use lowercase
- Include unit in name when not obvious: `request.duration.seconds`, `queue.size.messages`
- Tags must be low cardinality — never use user IDs, request IDs, or unbounded values

### SLOs (Service Level Objectives)

Define for every service:

- **Availability**: target uptime (e.g., 99.9%)
- **Latency**: p50 < 100ms, p95 < 300ms, p99 < 1s
- **Error rate**: < 0.1% of requests

Use error budgets — when budget is exhausted, prioritize reliability over features.

## Tracing

### Distributed Tracing

- Every request must carry a trace ID across all services
- Use W3C Trace Context standard for propagation
- Every service boundary (HTTP call, message publish/consume) creates a new span

### Span Requirements

Every span must include:

- Operation name (what was done)
- Duration
- Status (success/error)
- Service name and version
- Relevant attributes (HTTP method, URL, status code, DB statement)

### Context Propagation

- Propagate trace context in HTTP headers (`traceparent`, `tracestate`)
- Propagate in message headers for async communication
- Propagate across thread boundaries in async/parallel code
- Never drop context — broken traces are useless

### What to Trace

- All inbound HTTP requests (automatic via instrumentation)
- All outbound HTTP calls
- Database queries
- Message publish and consume
- Cache operations
- Custom business operations (payment processing, order fulfillment)

## Health Checks

Every service must expose:

| Endpoint | Purpose | Failure action |
|----------|---------|---------------|
| `/health/liveness` | Is the process alive? | Restart container |
| `/health/readiness` | Can it serve traffic? | Remove from load balancer |
| `/health/startup` | Has initialization completed? | Wait (don't kill during boot) |

### Rules

- Liveness: check process is running — never check dependencies here (cascading restarts)
- Readiness: check critical dependencies (database connected, cache reachable)
- Startup: use for slow-starting services (model loading, cache warming)
- Health checks must respond within 100ms
- Return structured response with component status

## Alerting

### Principles

- Alert on symptoms (high error rate, slow responses) — not causes (high CPU)
- Every alert must be actionable — if you can't do anything, it's not an alert
- Include runbook link in every alert definition
- Define severity levels with response expectations

### Severity Levels

| Level | Response Time | Examples |
|-------|--------------|---------|
| Critical | Immediate (page on-call) | Service down, data loss, security breach |
| High | Within 1 hour | Error rate spike, degraded performance |
| Medium | Within business day | Disk filling, certificate expiring soon |
| Low | Next sprint | Non-critical warnings, optimization opportunities |

### Anti-Patterns

- Don't alert on every error — alert on error *rate* exceeding threshold
- Don't alert on metrics you never act on (alert fatigue)
- Don't set thresholds too tight — allow normal variance
- Don't page for non-critical issues

## Dashboards

### Standard Dashboard Layout

Every service should have a dashboard with:

1. **Overview** — request rate, error rate, latency (RED)
2. **Dependencies** — status of downstream services
3. **Resources** — CPU, memory, disk, connections
4. **Business metrics** — domain-specific KPIs

### Rules

- Use consistent time ranges across panels
- Include SLO targets as reference lines
- Show rate of change, not just absolute values
- Group related metrics visually
