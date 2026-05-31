# :material-clipboard-list: Create Tasks

Breaks down requirements into user stories with hour estimates. One file per epic.

!!! tip "Triggers"
    - "create tasks" / "break down stories" / "generate tasks" / "plan the work"

!!! success "Expected Outcomes"
    - Stories (1-40 hours each) with acceptance criteria
    - Dependencies identified, first story establishes CI/CD
    - Total estimate provided

## Example

!!! example "Scenario: Notification service tasks"

    Creates `.specs/tasks/1-notification-service.tasks.md`:

    ```markdown
    # Tasks: Notification Service

    ## Epic
    - **Epic ID**: —
    - **Status**: Draft

    ## References

    | ID | Name |
    |---|---|
    | FR-1 | Order Event Notifications |
    | FR-2 | Notification Channel Preferences |
    | NFR-1 | Rate Limiting |

    ## User Stories

    ### Story 1: Kafka Consumer Setup
    - **Estimate**: 8h
    - **Description**: Set up Spring Kafka consumer for order-events topic
      with CI/CD pipeline and basic health check.
    - **Dependencies**: None
    - **Acceptance Criteria**:
      - [ ] Consumer connects to Kafka and reads events
      - [ ] Health check endpoint exposed
      - [ ] CI pipeline runs tests on PR

    ### Story 2: Email Notification Delivery
    - **Estimate**: 12h
    - **Description**: Implement email sending via SendGrid with retry logic.
    - **Dependencies**: Story 1
    - **Acceptance Criteria**:
      - [ ] Email sent on order shipped event
      - [ ] Retry 3× with exponential backoff on failure
      - [ ] Integration test with WireMock for SendGrid
    ```

    Total estimate: 40h (5 stories).

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/sdd/create-tasks/SKILL.md)
