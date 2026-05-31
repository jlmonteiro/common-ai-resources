# :material-sitemap: Create Design

Creates design documents tracing back to requirements. Includes ADRs with evidence-based rationale and test scenarios.

!!! tip "Triggers"
    - "create design" / "design specification" / "add design doc"

!!! success "Expected Outcomes"
    - Components with interfaces and error handling
    - ADRs (Problem, Solution, Alternatives, Rationale, Consequences)
    - Test scenarios (Given/When/Then) validating requirements

## Example

!!! example "Scenario: Notification architecture"

    Reads requirements. Creates `.specs/design/notification-architecture.md`:

    ```markdown
    # Notification Architecture

    ## Components

    ### NotificationConsumer
    **Purpose**: Consume order events from Kafka
    **Technology**: Spring Kafka

    ### NotificationRouter
    **Purpose**: Route to correct channel based on user preferences
    **Interfaces**: Receives event, queries preferences, dispatches

    ### EmailSender / PushSender
    **Purpose**: Deliver via SendGrid / Firebase

    ## Architectural Decision Records

    ### ADR-1: Use Kafka Consumer Groups for Scaling

    **Problem:** Need to handle high event volume without duplicates.

    **Solution:** Kafka consumer groups with partition-based assignment.

    **Alternatives:**

    | Alternative | Pros | Cons |
    |---|---|---|
    | Polling DB | Simple | Latency, DB load |
    | RabbitMQ | Flexible routing | Another dependency |

    **Rationale:** Already using Kafka, consumer groups scale horizontally.

    **Consequences:** Ordering per-user not guaranteed across partitions.
    ```

    Also creates test scenarios linking to FR-1, FR-2.

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/sdd/create-design/SKILL.md)
