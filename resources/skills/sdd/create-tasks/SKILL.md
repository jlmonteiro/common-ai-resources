---
name: "create-tasks"
description: "Create tasks file with user story breakdown. Use when user says 'create tasks', 'break down stories', 'generate tasks', or 'plan the work'."
---

# Create Tasks

Tasks are **transactional** — one file per epic. Files live in `.specs/tasks/` as `{id}-{slug}.tasks.md`.

## Prerequisites

- `.specs/requirements/requirements.md` exists with requirements
- `.specs/design/design.md` exists with design
- Search the **sdd** knowledge base for task templates and story guidelines

## Steps

### 1. Initialize Structure

```bash
mkdir -p .specs/tasks
```

Check if `tasks/tasks.md` index exists. If not, use the template from the SDD knowledge base.

### 2. Read Requirements and Design

Understand:
- Requirements and acceptance criteria
- Components and architecture
- Test scenarios

### 3. Ask for Epic Context

- "What is the title for this epic/feature?"
- "Which requirements does this address?"

### 4. Generate User Stories

For each relevant requirement, create stories:
- Each story: 1-40 hours of work
- Each story includes implementation AND tests
- First story establishes CI/CD foundation
- Identify dependencies between stories
- Use INVEST criteria

### 5. Create Task File

Create `.specs/tasks/{id}-{slug}.tasks.md`:
- Sequential ID
- Slug: lowercase, hyphenated, max 50 chars
- Set status to Draft

### 6. Update Tasks Index

Add new row to `tasks/tasks.md`.

### 7. Present to User

Report stories created, total estimate, suggest next steps.
