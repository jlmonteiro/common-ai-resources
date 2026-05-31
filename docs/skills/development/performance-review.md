# :material-speedometer: Performance Review

Identifies bottlenecks, N+1 queries, memory issues, and scaling concerns. Quantifies impact.

!!! tip "Triggers"
    - "performance review" / "check performance" / "why is this slow" / "optimize"

!!! success "Expected Outcomes"
    - Bottlenecks with evidence and quantified impact
    - Fixes with expected improvement
    - Trade-off analysis

## Example

!!! example "Scenario: Slow /orders endpoint"

    **Step 1 — Scope:**

    > "What do you want to analyze?"

    User: "The /orders endpoint is slow under load"

    **Step 2 — Analyze:**

    Agent traces the request path:

    ```
    OrderController.listOrders()
      → OrderService.findByCustomer(id)
        → orderRepository.findByCustomerId(id)     // 1 query
        → for each order:
            order.getItems()                        // N queries (lazy load!)
        → for each order:
            paymentService.getStatus(order.paymentId)  // N HTTP calls (sequential!)
    ```

    **Findings:**

    ```
    🔴 N+1 Query in OrderService.findByCustomer()
       Impact: 100 orders = 101 DB queries
       Evidence: Lazy-loaded items collection accessed in loop
       Fix: Use JOIN FETCH or @EntityGraph
       Expected: 101 queries → 1 query

    🟡 Sequential HTTP calls to payment service
       Impact: 100 orders × 50ms = 5000ms serial
       Evidence: Loop calling paymentService.getStatus() one by one
       Fix: Use CompletableFuture.allOf() for parallel calls
       Expected: 5000ms → ~50ms (parallel)

    🟢 No pagination on findByCustomerId
       Impact: Returns unbounded list — grows with customer history
       Fix: Add Pageable parameter, default page size 20
       Expected: Constant response time regardless of history size
    ```

    **Step 5:** "Which findings should I address? I'll start with the N+1 (critical)."

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/development/performance-review/SKILL.md)
