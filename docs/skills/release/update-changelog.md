# :material-file-document-edit: Update Changelog

Adds entries to CHANGELOG.md following Keep a Changelog format. Categorizes changes and uses imperative mood.

!!! tip "Triggers"
    - "update changelog" / "add to changelog" / "log this change"

!!! success "Expected Outcomes"
    - Entry added under `[Unreleased]` with correct category
    - Imperative mood, user perspective
    - No duplicates

## Example

!!! example "Scenario: After adding a new knowledge base"

    Agent reads current CHANGELOG, determines category:

    > Change type: `feat` → category: **Added**

    Writes entry:

    ```markdown
    ### Added
    - Docker knowledge base (Dockerfile standards, image management conventions)
    ```

    Verifies:
    - ✅ Under `[Unreleased]`
    - ✅ Correct category (Added)
    - ✅ No duplicate
    - ✅ Imperative mood, user perspective

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/release/update-changelog/SKILL.md)
