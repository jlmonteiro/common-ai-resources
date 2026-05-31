# :material-clipboard-check: Review Skill

Validates a skill against knowledge bases and simulates execution step by step with examples.

!!! tip "Triggers"
    - "review skill" / "check this skill" / "simulate skill" / "walk me through this skill"

!!! success "Expected Outcomes"
    - Structure validated (frontmatter, naming, steps)
    - KB alignment verified
    - Each step simulated with context and examples
    - Issues reported

## Example

!!! example "Scenario: Review the create-design skill"

    **Step 1 — Validate Structure:**

    | Check | Result |
    |-------|--------|
    | Name: `create-design` | ✅ kebab-case |
    | Description: functional intent | ✅ |
    | Description: triggers | ✅ 3 phrases |
    | Steps numbered | ✅ 5 steps |
    | Single workflow | ✅ |

    Issue found: description says "add ADR" as trigger — could cause false activation.

    **Step 2 — KB Alignment:**

    All instructions match SDD KB templates ✅. ADR format matches ✅.

    **Step 3 — Simulate:**

    Walks through each step with a notification service example:

    > **Step 2 — Read Requirements:** reads FR-1 through NFR-2. ✅
    >
    > **Step 4 — Create Files:** generates components, ADR with alternatives table, test scenarios. ✅

    "Thoughts?" → User provides feedback → changes applied → next step.

    **Summary:** 1 issue (false trigger), 0 KB contradictions, all steps valid.

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/development/review-skill/SKILL.md)
