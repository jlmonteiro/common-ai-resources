---
name: "create-test"
description: "Generate tests for existing code following TDD and BDD conventions. Analyzes the target and generates appropriate test type (unit, integration, e2e). Use when user says 'create test', 'generate tests', 'write tests', 'add tests', or 'test this class'."
---

# Create Test

## Prerequisites

Search the following knowledge bases:
- **testing** — TDD, BDD structure, test pyramid, mocking rules, negative scenarios
- Project's language scope (e.g., **java**) — testing framework, test slices, Testcontainers

## Step 1: Identify Target

Ask if not obvious:

> "What do you want to test?"

Determine:
- Target file/class/function
- What layer it belongs to (controller, service, repository, utility)
- External dependencies it uses

## Step 2: Determine Test Type

Based on the layer and dependencies, select the appropriate test type:

| Layer | Test Type | Dependencies |
|-------|-----------|-------------|
| Utility / pure logic | Unit test | None (no mocks needed) |
| Service (internal deps only) | Integration test | Real beans, Testcontainers for infra |
| Service (external deps) | Integration test | Real beans + mock external services |
| Controller / API | Integration test | Full HTTP (MockMvc or equivalent) |
| Repository (custom queries) | Integration test | Testcontainers (real DB) |

Present to user:

> "This is a service with a database dependency and an external payment call. I'll create an integration test with Testcontainers for PostgreSQL and a mock for the payment gateway. OK?"

## Step 3: Identify Scenarios

Analyze the target code and propose test scenarios:

**Happy path:**
- Normal successful execution for each public method

**Negative scenarios (mandatory):**
- Invalid inputs (null, empty, boundary values)
- External dependency failures (timeout, error response)
- Business rule violations
- Authorization failures (if applicable)

**Edge cases:**
- Empty collections
- Concurrent access (if relevant)
- Boundary values (max size, zero, negative)

Present the scenario list:

> "Proposed scenarios:
> 1. ✅ Should create order with valid input
> 2. ✅ Should calculate total correctly with multiple items
> 3. ❌ Should reject order with empty items list
> 4. ❌ Should handle payment gateway timeout
> 5. ❌ Should reject order exceeding credit limit
>
> Add or remove any?"

## Step 4: Generate Tests (TDD)

For each scenario, write the test following BDD structure:

```
Given: [preconditions — setup test data]
When:  [action — call the method/endpoint]
Then:  [assertion — verify outcome]
```

Rules:
- Use descriptive block labels
- Use `and:` for complex setups or multiple assertions
- Use data-driven tests (`where:`) for input validation scenarios
- Use real implementations — mock only external services
- Each test is independent and can run in parallel

## Step 5: Run and Verify

1. Run the tests
2. Confirm they fail (if target code doesn't exist yet — TDD) or pass (if testing existing code)
3. If testing existing code and tests pass → check coverage, identify untested paths
4. If tests fail unexpectedly → the code has a bug (report it)

## Step 6: Present Summary

```
✓ Tests created: OrderServiceSpec

Scenarios:
  ✅ 2 happy path
  ❌ 3 negative
  📊 Coverage: 87% of OrderService

Files:
  - tests/.../OrderServiceSpec.groovy

Missing coverage:
  - Line 42: catch block for IOException (add scenario?)

Next steps:
  - Run 'code-review' to validate test quality
  - Add edge case scenarios if needed
```
