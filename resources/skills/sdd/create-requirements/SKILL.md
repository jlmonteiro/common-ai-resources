---
name: "create-requirements"
description: "Create or update requirements for a specification. Use when user says 'create requirements', 'start specification', 'new spec requirements', 'add requirements', 'gather requirements', 'what do we need to build', or describes a feature that needs requirements analysis."
---

# Create or Update Requirements

Requirements are **persistent** — they evolve across epics. Files live in `.specs/requirements/`.

## Prerequisites

Search the **sdd** knowledge base for requirements templates, EARS pattern, and quality checklist.

## Steps

### 1. Initialize Structure

```bash
mkdir -p .specs/requirements .specs/design .specs/tasks
```

Check if `requirements/requirements.md` index exists. If not, use the template from the SDD knowledge base.

### 2. Determine Scope

If the index already exists, ask:
- Add requirements to an existing topic page, or
- Create a new topic page

### 3. Analyze Context

Before asking questions:
- Check for existing implementations related to the topic
- Review related requirements already in `.specs/requirements/`
- Identify patterns, frameworks, and conventions in use

### 4. Gather Requirements

Ask focused questions adapted to context (limit 3 per turn):

**Always ask:**
1. "What problem does this solve and who are the users?"
2. "What are the key functional requirements?"

**Ask based on context:**
- Data topics: "What are the data entities and relationships?"
- API topics: "What are the expected inputs/outputs and error cases?"
- UI topics: "What are the key user journeys?"
- If relevant: non-functional requirements, dependencies, constraints

After initial gathering:
- "What should happen when things go wrong?"
- "Are there constraints on who/when/how this is used?"

### 5. Validate Understanding

Summarize requirements back to the user before creating files. Only proceed after confirmation.

### 6. Create or Update Files

- Use EARS syntax for acceptance criteria
- Include rationale for each requirement
- Update the index with new IDs and links
- Split topic pages at ~200 lines
- Validate against the requirements quality checklist from the SDD KB

### 7. Present to User

Report what was created/updated, list new requirement IDs, suggest next steps (create design).
