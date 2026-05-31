# :material-file-eye: Review Document

Interactive item-by-item review. Presents each section with context and examples, waits for feedback before moving on.

!!! tip "Triggers"
    - "review this document" / "review the KB" / "go through this file"
    - "review item by item" / "let me review"

!!! success "Expected Outcomes"
    - Each item presented with context and examples
    - Changes applied only after explicit approval
    - Summary: items reviewed, accepted, modified

## Example

!!! example "Scenario: Reviewing a knowledge base document"

    Agent reads the file, breaks into sections, presents first item:

    > **§ Docker Standards → Multi-Stage Builds**
    >
    > Separate build dependencies from runtime to minimize image size.
    >
    > ---
    >
    > *Context: Multi-stage builds are the #1 technique for reducing image size. The example is Python-specific.*
    >
    > ---
    >
    > Thoughts?

    User: "Add motivation and dos/donts"

    Agent proposes additions. User approves. Changes applied. Moves to next item.

    ...

    **Summary:**
    - Total items: 13
    - Accepted: 7
    - Modified: 6

## Source

[:material-file-code: SKILL.md](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/skills/document/review/SKILL.md)
