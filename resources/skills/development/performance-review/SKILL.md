---
name: "performance-review"
description: "Focused performance analysis of code or system. Identifies bottlenecks, N+1 queries, memory issues, and scaling concerns. Use when user says 'performance review', 'check performance', 'why is this slow', 'optimize', or 'performance audit'."
---

# Performance Review

## Prerequisites

Search the following knowledge bases:
- **observability** — metrics, SLOs, RED method
- **resilience** — timeouts, bulkhead, scaling
- **databases** — query patterns (if DB involved)
- Project's language scope — caching, connection pools

## Step 1: Determine Scope

Ask:

> "What do you want to analyze?
> 1. Specific endpoint/method (I know what's slow)
> 2. General codebase scan (find potential issues)
> 3. Load test results (I have metrics/traces)"

## Step 2: Analyze

### If specific endpoint:
- Trace the request path end-to-end
- Identify I/O operations (DB queries, HTTP calls, file access)
- Check for sequential calls that could be parallel
- Measure or estimate time per operation

### If general scan:
Check for common performance anti-patterns:

#### Database
- N+1 queries (loop with individual queries instead of batch)
- Missing indexes on filtered/joined columns
- Unbounded queries (no LIMIT, fetching entire tables)
- Lazy loading outside transaction boundaries

#### Collections & Memory
- Unbounded lists (no pagination, no max size)
- Loading entire dataset into memory for filtering
- String concatenation in loops (use StringBuilder/join)
- Large objects in session/cache without TTL

#### I/O & Network
- Sequential external calls that could be parallel
- Missing connection pooling
- No timeout on external calls
- Synchronous operations that could be async

#### Caching
- Repeated expensive computations without caching
- Cache without TTL (stale data)
- Cache without size limit (memory leak)

### If load test results:
- Identify p95/p99 latency outliers
- Check error rate under load
- Identify resource saturation (CPU, memory, connections)
- Find the bottleneck (DB, network, CPU-bound code)

## Step 3: Classify Findings

| Impact | Criteria |
|--------|----------|
| 🔴 Critical | Causes outages under normal load, O(n²) or worse |
| 🟡 High | Degrades under moderate load, wastes significant resources |
| 🟢 Medium | Suboptimal but functional, improvement opportunity |
| ℹ️ Info | Micro-optimization, not worth the complexity trade-off |

## Step 4: Present Report

```
## Performance Review

**Scope:** {what was analyzed}
**Findings:** 🔴 {N} | 🟡 {N} | 🟢 {N} | ℹ️ {N}

### 🔴 N+1 Query in OrderService.getOrdersWithItems()
**Impact:** 100 orders = 101 queries (1 + 100 item fetches)
**Evidence:** Each order triggers a separate SELECT for items
**Fix:** Use JOIN FETCH or @EntityGraph
**Expected improvement:** 101 queries → 1 query

### 🟡 Sequential payment + notification calls
**Impact:** 200ms + 150ms = 350ms serial (could be 200ms parallel)
**Fix:** Use CompletableFuture.allOf() or async events
```

## Step 5: Offer Fixes

For each finding, propose a fix with:
- Expected improvement (quantified)
- Trade-offs (complexity, readability)
- Whether a benchmark test should be added

Ask: "Which findings should I address?"
