# :material-file-search: Review Specification

Audits specs for completeness and quality. Checks EARS syntax, traceability, ADRs, and story estimates.

!!! tip "Triggers"
    - "review specification" / "check spec" / "analyze specification" / "audit requirements"

!!! success "Expected Outcomes"
    - Findings: Critical / High / Medium / Low
    - Actionable task list
    - Offer to fix specific findings

## Example

!!! example "Scenario: Review notification service specification"

    **Scope:** Everything

    **Report:**

    ```
    ## Review Findings

    ### Summary
    - Critical: 1
    - High: 2
    - Medium: 3

    ### Findings

    #### [CRITICAL] Requirements: Missing failure scenario
    Location: requirements/notifications.md - FR-1
    Issue: No requirement for what happens when all retry attempts
           are exhausted (message lost silently?)
    Recommendation: Add FR-4 defining dead-letter queue behavior

    #### [HIGH] Design: ADR missing alternatives evidence
    Location: design/notification-architecture.md - ADR-1
    Issue: "Already using Kafka" is not sufficient rationale.
           No benchmarks or capacity analysis provided.
    Recommendation: Add throughput comparison and team expertise assessment

    #### [HIGH] Tasks: Story 2 exceeds 40h guideline
    Location: tasks/1-notification-service.tasks.md - Story 2
    Issue: Email + push + retry + preferences in one story (estimated 12h
           but likely 20h+)
    Recommendation: Split into separate stories per channel

    #### [MEDIUM] Requirements: Ambiguous language
    Location: requirements/notifications.md - NFR-2
    Issue: "quiet hours" not precisely defined — whose timezone?
    Recommendation: Specify "user's configured timezone"
    ```

    Agent: "Would you like to address the critical finding first?"

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/sdd/review-specification/SKILL.md)
