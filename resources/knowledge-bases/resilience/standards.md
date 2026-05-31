# Resilience Standards

## Design Principles

- Assume every dependency will fail — design for it
- Fail fast — don't hold resources waiting for unresponsive services
- Degrade gracefully — partial functionality is better than total failure
- Isolate failures — one failing dependency must not cascade to the entire system

## Patterns

### Circuit Breaker

Prevent repeated calls to a failing dependency. Protect the system from cascading failures.

**States:**

| State | Behavior |
|-------|----------|
| Closed | Normal operation, tracking failure rate |
| Open | Fast-fail immediately, return fallback |
| Half-Open | Allow limited requests to test recovery |

**When to use:**
- External HTTP calls (APIs, microservices)
- Database connections under high load
- Any dependency that can become unresponsive

**When NOT to use:**
- Internal method calls within the same service
- Fast-failing validations
- Fire-and-forget operations

### Retry with Backoff

Automatically retry transient failures with increasing delays.

**Rules:**
- Always use exponential backoff with jitter (prevents thundering herd)
- Set a maximum retry count (typically 3)
- Only retry idempotent operations — or use idempotency keys
- Only retry transient errors (5xx, timeouts) — never client errors (4xx)

**Backoff formula:**

```
delay = baseDelay * (multiplier ^ attempt) + random_jitter
```

### Timeout

Set explicit timeouts on every external call. Never wait indefinitely.

**Rules:**
- Define a timeout budget per request path (end-to-end SLA)
- Allocate per-hop timeouts within the budget
- Propagate deadline headers across services
- When budget is exhausted, fail fast with appropriate error

### Bulkhead

Isolate resources per dependency to prevent one slow service from consuming all capacity.

**Patterns:**
- Separate thread/connection pools per downstream service
- Queue depth limits with backpressure
- Rate limiting per tenant/client

### Fallback

Provide degraded responses when a dependency is unavailable.

**Strategies:**

| Strategy | Use when |
|----------|----------|
| Cached response | Stale data is acceptable |
| Default value | A sensible default exists |
| Empty response | Absence is better than failure |
| Queued for later | Operation can be deferred |

**Rules:**
- Always define a fallback for circuit breakers
- Log when fallback is used (WARN level)
- Monitor fallback usage — sustained fallback indicates unresolved failure
- Never silently swallow errors — the user/caller should know the response is degraded

## Configuration

### Externalize All Thresholds

Never hardcode resilience parameters. Configure via environment or config files:

- Failure rate threshold (circuit breaker)
- Wait duration in open state
- Max retry attempts
- Backoff multiplier and base delay
- Timeout durations
- Bulkhead pool sizes

This allows tuning per environment without code changes.

### Per-Dependency Configuration

Different dependencies have different SLAs. Configure independently:

- Payment gateway: aggressive timeout (5s), 3 retries, circuit breaker at 30% failure
- Internal cache: short timeout (500ms), no retry, no circuit breaker
- Email service: long timeout (30s), 2 retries, circuit breaker at 50% failure

## Ordering

When combining patterns, apply in this order:

```
Request → Retry → Circuit Breaker → Timeout → Bulkhead → Call
```

- Retry wraps circuit breaker (retry triggers, then circuit breaker trips if retries exhaust)
- Timeout is per individual attempt (not total)
- Bulkhead limits concurrent calls regardless of retries

## Testing Resilience

- Test with dependencies down — verify fallbacks activate
- Test with slow dependencies — verify timeouts trigger
- Test with intermittent failures — verify retries and circuit breaker behavior
- Use chaos engineering in staging (inject latency, errors, partitions)
- Monitor error budgets — alert when approaching SLO limits
