# REST API Standards

## Methodology: API First

Design the API before implementing it:

1. **Define** — Write the OpenAPI Specification (OAS 3.x)
2. **Review** — Validate with stakeholders and consumers
3. **Accept** — Finalize the contract
4. **Implement** — Build the server against the accepted spec
5. **Verify** — Ensure implementation matches the spec

Never write code before the API contract is agreed upon.

## URL Design

### Resource Naming

- Use plural nouns for collections: `/users`, `/orders`, `/products`
- Use kebab-case for multi-word resources: `/order-items`, `/payment-methods`
- Nest for relationships: `/users/{id}/orders`
- Maximum 3 levels of nesting — beyond that, use query parameters or top-level resources

### Path Parameters vs Query Parameters

| Use path for | Use query for |
|-------------|--------------|
| Resource identity (`/users/{id}`) | Filtering (`?status=active`) |
| Required hierarchy (`/users/{id}/orders`) | Pagination (`?page=1&size=20`) |
| | Sorting (`?sort=created_at,desc`) |
| | Optional fields (`?fields=id,name`) |

### Complex Queries

When query parameters become too many or too complex (>2000 chars, nested filters):

- Use `POST /resources/search` with a request body
- This is not creating a resource — it's a query action
- Document clearly in OAS that this is a search endpoint

### Bulk Operations

For operations on multiple resources:

- Use `POST /resources/batch` with an array in the body
- Return individual results per item (some may succeed, some may fail)
- Never use repeated query parameters for bulk IDs

## HTTP Methods

| Method | Purpose | Idempotent | Request Body |
|--------|---------|-----------|-------------|
| GET | Retrieve resource(s) | Yes | No |
| POST | Create resource | No | Yes |
| PUT | Full replacement | Yes | Yes |
| PATCH | Partial update | Yes | Yes |
| DELETE | Remove resource | Yes | No |

### PUT vs PATCH

**PUT** replaces the entire resource. Omitted fields are set to null/default:

```
PUT /users/123
{"name": "John", "email": "john@test.com"}

→ Result: name="John", email="john@test.com", phone=null (cleared)
```

**PATCH** updates only the provided fields. Omitted fields remain unchanged:

```
PATCH /users/123
{"email": "new@test.com"}

→ Result: name="John" (unchanged), email="new@test.com", phone="+1234" (unchanged)
```

**Rule:** Use PATCH for most updates. Use PUT only when the client owns the full resource state and intends to replace it entirely.

## Status Codes

### Success

| Code | When |
|------|------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE (no content) |

### Client Errors

| Code | When |
|------|------|
| 400 | Invalid request body or parameters |
| 401 | Missing or invalid authentication |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Validation failed (semantically invalid) |

### Server Errors

| Code | When |
|------|------|
| 500 | Unexpected server error (unhandled exception) |
| 502 | Upstream service returned invalid response |
| 503 | Service temporarily unavailable (overloaded, maintenance) |
| 504 | Upstream service timed out |

### Resilience Scenarios

| Scenario | Status Code | Retry-After Header |
|----------|------------|-------------------|
| Client exceeded rate limit | 429 | Yes (seconds until quota resets) |
| Server overloaded (all clients affected) | 503 | Yes (estimated recovery time) |
| Circuit breaker open | 503 | Yes (estimated recovery time) |
| Max retries exhausted to upstream | 502 or 504 | No |
| Dependency unavailable (fallback used) | 200 (degraded) | No |
| Dependency unavailable (no fallback) | 503 | Yes |

**Rules:**

- Use 429 when a specific client hit their rate limit — other clients may still be served
- Use 503 when the server itself is overloaded or a dependency is down — affects all clients
- Always include `Retry-After` header with 429 and 503 responses
- Use 502/504 when the failure is in an upstream service, not this service
- If a fallback response is served, return 200 but indicate degraded state in response metadata

## Error Response Format

Use RFC 7807 Problem Details for all errors:

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Email format is invalid",
  "instance": "/users/123"
}
```

**Rules:**

- Always include `type`, `title`, `status`, and `detail`
- `type` is a URI identifying the error category
- Never expose stack traces or internal details in production
- Add custom fields for additional context (e.g., `errors` array for validation, `retryAfter` for rate limits):

```json
{
  "type": "https://api.example.com/errors/validation-failed",
  "title": "Validation Failed",
  "status": 422,
  "detail": "Multiple fields failed validation",
  "errors": [
    {"field": "email", "message": "Invalid format"},
    {"field": "age", "message": "Must be at least 18"}
  ]
}
```

## Pagination

Use offset-based pagination with consistent envelope:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "size": 20,
    "totalElements": 142,
    "totalPages": 8
  }
}
```

**Rules:**

- Default page size: 20
- Maximum page size: 100
- Always return pagination metadata
- Use `page` and `size` query parameters

## Versioning

- Use URL path versioning: `/api/v1/users`
- Increment version only for breaking changes
- Support previous version for a documented deprecation period
- Document sunset date in response headers: `Sunset: Sat, 01 Jan 2027 00:00:00 GMT`

## Backward Compatibility

### Breaking Changes (require new version)

- Removing a field from response
- Renaming a field
- Changing a field type
- Removing an endpoint
- Making an optional field required

### Non-Breaking Changes (safe within same version)

- Adding a new optional field to response
- Adding a new endpoint
- Adding a new optional query parameter
- Adding a new enum value

## OpenAPI Specification

### Requirements

- Every API must have an OAS 3.x document
- Spec must be the source of truth — implementation follows spec, not the other way around
- Include descriptions for all endpoints, parameters, and schemas
- Include request/response examples
- Define all error responses per endpoint

### File Location

```
docs/api/
├── openapi.yaml       # Main spec
└── schemas/           # Shared schema definitions (if large)
```

### Validation

- Lint the spec before review (e.g., Spectral, swagger-cli)
- Generate client SDKs from the spec to verify usability
- Run contract tests to ensure implementation matches spec

## Request/Response Conventions

- Use camelCase for JSON field names
- Wrap collections in a named field (not bare arrays): `{"data": [...]}`
- Include `id` in all resource responses
- Return the created/updated resource in POST/PUT/PATCH responses

### Data Types

| Type | Format | Example |
|------|--------|---------|
| Timestamps | ISO 8601 with timezone | `"2026-05-30T21:00:00Z"` |
| Dates (no time) | ISO 8601 date | `"2026-05-30"` |
| Durations | ISO 8601 duration | `"PT30M"` (30 minutes), `"P7D"` (7 days) |
| Intervals | ISO 8601 interval | `"2026-05-01T00:00:00Z/2026-05-31T23:59:59Z"` |
| Money | String with currency field | `{"amount": "99.99", "currency": "EUR"}` |
| Enums | UPPER_SNAKE_CASE strings | `"PAYMENT_PENDING"` |

**Rules:**

- Always use UTC for timestamps — never local time
- Use strings for monetary values — never floats (precision loss)
- Include timezone offset or `Z` suffix — never bare timestamps
- Durations and intervals follow ISO 8601 — never custom formats like `"30 mins"`

## Security

- Always require authentication (except public endpoints explicitly documented)
- Use Bearer tokens in Authorization header
- Validate all input — never trust client data
- Rate limit all endpoints
- Return 401 for missing auth, 403 for insufficient permissions — never 404 to hide resources
