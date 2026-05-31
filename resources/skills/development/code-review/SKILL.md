---
name: "code-review"
description: "Comprehensive code review against project standards using focused KB searches per topic. Adapts to the project's tech stack. Use when user says 'review code', 'code review', 'check code quality', 'review this PR', or 'review my changes'."
---

# Code Review

## Prerequisites

- Read `project-context.md` to understand the tech stack
- Call `list_scopes` on the MCP knowledge base to see available scopes

## Step 1: Detect Project Context

Identify the project's tech stack by examining:
- Build files (`pyproject.toml`, `build.gradle.kts`, `package.json`, `go.mod`)
- Source language (Java, Python, Go, TypeScript, etc.)
- Frameworks (Spring Boot, FastAPI, Express, etc.)
- Infrastructure (Docker, Kubernetes, Helm)

### Determine Applicable Scopes

**Always applicable (any project):**
- `testing` — test structure, coverage, negative scenarios
- `security` — input validation, secrets, auth patterns
- `resilience` — error handling, retries, fallbacks
- `logging` — structured logging, levels, sensitive data
- `observability` — metrics, tracing, health checks
- `api` — REST conventions (if API code is being reviewed)
- `git` — commit messages, PR conventions

**Stack-specific (include only if detected):**
- `java` — if Java/Kotlin project
- `gradle` — if Gradle build system
- `docker` — if Dockerfile or docker-compose present
- `helm` — if Helm charts present
- `k8s` — if Kubernetes manifests present
- `databases` — if database code or migrations present

## Step 2: Identify Changed Files

Determine what's being reviewed:
- `git diff --name-only` for uncommitted changes
- `git diff main --name-only` for branch changes
- Or specific files the user points to

Categorize changes: source code, tests, config, infrastructure, documentation.

## Step 3: Execute Review

### Execution Strategy

**If sub-agents/task delegation is available:**

Spawn one focused agent per review area. Each agent:
- Searches only its relevant KB scope(s)
- Reviews only the files relevant to its area
- Returns a structured findings list

**If not available:**

Run reviews sequentially — one area at a time, summarize findings, then move to next.

### Review Areas

Execute each area as a separate focused operation:

#### 3.1 Code Quality & Style
- **Scopes:** project's language scope (e.g., `java`)
- **Check:** naming, complexity, architecture patterns, modern language features, import style

#### 3.2 Testing
- **Scopes:** `testing` + language scope
- **Check:** test coverage for changes, BDD structure, negative scenarios, mocking rules, test isolation

#### 3.3 Security
- **Scopes:** `security`
- **Check:** input validation, secrets exposure, auth patterns, injection risks, data protection

#### 3.4 Resilience & Error Handling
- **Scopes:** `resilience` + language scope
- **Check:** error handling, retries, timeouts, fallbacks, circuit breakers (if applicable)

#### 3.5 Logging & Observability
- **Scopes:** `logging`, `observability`
- **Check:** structured logging, appropriate levels, no sensitive data logged, metrics/tracing for new operations

#### 3.6 API Design (if API changes)
- **Scopes:** `api`
- **Check:** REST conventions, status codes, error format, backward compatibility, pagination

#### 3.7 Infrastructure (if infra changes)
- **Scopes:** `docker`, `helm`, `k8s` (as applicable)
- **Check:** Dockerfile standards, image tagging, resource limits, security context, probes

#### 3.8 Database (if DB changes)
- **Scopes:** `databases`
- **Check:** naming conventions, migration strategy, expand-contract pattern

#### 3.9 Documentation
- **Scopes:** project's language scope
- **Check:** missing/outdated README, API docs (OAS matches implementation), inline comments for complex logic, changelog updated

#### 3.10 Performance
- **Scopes:** project's language scope, `databases`
- **Check:** N+1 queries, unnecessary allocations, missing pagination on collections, unbounded lists, expensive operations in loops

#### 3.11 Dependency Hygiene
- **Scopes:** `security`, project's build scope (e.g., `gradle`)
- **Check:** unpinned versions, unused dependencies, known vulnerabilities, open version ranges

## Step 4: Consolidate Findings

Merge results from all areas. Categorize:

| Severity | Meaning | Action |
|----------|---------|--------|
| 🔴 Critical | Security vulnerability, data loss risk, breaking change | Must fix before merge |
| 🟡 High | Bug, missing test, convention violation | Should fix before merge |
| 🟢 Medium | Improvement opportunity, minor convention miss | Fix or acknowledge |
| ℹ️ Info | Suggestion, alternative approach | Optional |

## Step 5: Present Report

```
## Code Review Summary

**Files reviewed:** {N}
**Findings:** 🔴 {N} Critical | 🟡 {N} High | 🟢 {N} Medium | ℹ️ {N} Info

### Findings

#### 🔴 [Security] SQL injection risk in UserService.java:42
**Standard:** Input validation — parameterized queries (security KB)
**Issue:** String concatenation in SQL query
**Fix:** Use parameterized query

#### 🟡 [Testing] Missing negative test for OrderController
**Standard:** At least one negative test per happy path (testing KB)
**Issue:** No test for invalid order ID
**Fix:** Add test for 404 response

...
```

## Step 6: Offer to Fix

Ask: "Would you like me to fix any of these findings?"

If yes, address in priority order (critical first).
