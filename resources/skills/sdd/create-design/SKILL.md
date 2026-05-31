---
name: "create-design"
description: "Create or update design documents for a specification. Use when user says 'create design', 'design specification', or 'add design doc'."
---

# Create or Update Design

Design documents are **persistent** — they evolve across epics. Files live in `.specs/design/`.

## Prerequisites

- `.specs/requirements/requirements.md` must exist with at least one requirement
- Search the **sdd** knowledge base for design templates, ADR format, and quality checklist

## Steps

### 1. Initialize Structure

```bash
mkdir -p .specs/design
```

Check if `design/design.md` index exists. If not, use the template from the SDD knowledge base.

### 2. Read Requirements

Read requirements index and relevant topic pages to understand what needs to be designed.

### 3. Determine Scope

Ask:
- "What is the design topic?" (e.g., REST Architecture, Security, Data Models)
- "What technology stack should be used?"
- "Are there existing systems to integrate with?"

### 4. Create or Update Files

- Reference requirement IDs in design decisions
- Include ADRs with Problem, Solution, Alternatives, Rationale, Consequences
- Update test scenarios (`design/test-scenarios.md`) with Given/When/Then
- Update the design index

### 5. Present to User

Report what was created/updated, suggest next steps (create tasks).
