---
name: "create-api-endpoint"
description: "Scaffold a REST API endpoint following API First methodology. Creates OAS definition first, then implementation with tests. Use when user says 'add endpoint', 'create API', 'add a route', 'new endpoint', or 'implement REST operation'."
---

# Create API Endpoint

## Prerequisites

Search the following knowledge bases:
- **api** — REST standards, URL design, status codes, error format, data types
- **testing** — TDD, BDD structure, negative scenarios
- Project's language scope (e.g., **java**) — framework conventions

## Step 1: Gather Endpoint Context

Ask the user:

1. "What resource does this endpoint operate on?" (e.g., orders, users, payments)
2. "What operation?" (create, read, list, update, delete, custom action)
3. "Any specific requirements or constraints?"

## Step 2: Design the API Contract (API First)

Based on the answers, propose the endpoint design:

- HTTP method (following REST conventions from api KB)
- URL path (plural nouns, kebab-case, proper nesting)
- Request body schema (if applicable)
- Response schema
- Status codes (success + all error cases)
- Query parameters (pagination, filtering if list operation)

Present to user:

```
Proposed endpoint:

  POST /api/v1/orders

  Request:
    { "customerId": "string", "items": [...], "shippingAddress": {...} }

  Responses:
    201: Created order (returns full resource)
    400: Invalid request format
    422: Validation failed (ProblemDetail with errors array)
    401: Unauthorized

  Does this look correct?
```

Only proceed after user confirms.

## Step 3: Create/Update OAS

Add the endpoint to the OpenAPI specification:

- If `docs/api/openapi.yaml` exists: add to it
- If not: ask "Do you want to create an OpenAPI spec for this project?"

Include:
- Path, method, operationId
- Request body with schema and example
- All response codes with schemas
- Parameter descriptions
- Tags for grouping

## Step 4: Implement (TDD)

Follow TDD — write failing test first, then implement:

### 4.1 Write Failing Test

Create a BDD test for the happy path:

```
Given: [preconditions]
When: [endpoint is called with valid input]
Then: [expected response]
```

Plus at least one negative test:

```
Given: [preconditions]
When: [endpoint is called with invalid input]
Then: [error response with correct status and ProblemDetail]
```

Run tests — confirm they fail.

### 4.2 Implement Endpoint

Based on project's framework, create:
- Controller/route handler (HTTP concerns only)
- Request/response DTOs with validation annotations
- Service method (business logic)
- Repository method (if data access needed)

### 4.3 Run Tests

Confirm all tests pass.

## Step 5: Verify Against Contract

- Validate implementation matches the OAS definition
- Verify all documented status codes are actually returned
- Verify response schemas match

## Step 6: Present Summary

```
✓ Endpoint created: POST /api/v1/orders

Files:
  - docs/api/openapi.yaml (updated)
  - src/.../controller/OrderController
  - src/.../service/OrderService
  - src/.../model/dto/CreateOrderRequest
  - src/.../model/dto/OrderResponse
  - tests/.../OrderControllerSpec (2 scenarios: happy path + validation error)

Next steps:
  - Add more test scenarios (edge cases, auth)
  - Run 'code-review' to validate against standards
```
