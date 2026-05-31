---
name: "review-specification"
description: "Review specification for gaps and improvements. Use when user says 'review specification', 'check spec', 'analyze specification', or 'audit requirements'."
---

# Review Specification

Analyze specification files for completeness, quality, and potential improvements.

## Prerequisites

Search the **sdd** knowledge base for quality checklists (requirements and design).

## Steps

### 1. Ask Scope

- Requirements
- Design
- Tasks (specific task file)
- Everything

### 2. Read Files

Based on scope, read relevant files from `.specs/`.

### 3. Analyze

**Requirements:**
- All have acceptance criteria using EARS syntax
- User journeys are complete narratives
- IDs are sequential and consistent
- Index is up to date
- No ambiguous language (check banned words from KB)

**Design:**
- Components map to requirements (traceability)
- Test scenarios validate requirements
- ADRs have Problem, Solution, Alternatives, Rationale
- Error handling defined per component

**Tasks:**
- All requirements addressed by at least one task
- Stories are 1-40 hours each
- Each story has acceptance criteria
- Dependencies identified
- First story establishes CI/CD

**Document Quality:**
- Proper heading hierarchy
- Consistent formatting
- No broken links
- Terminology matches glossary

### 4. Generate Report

Categorize findings: Critical / High / Medium / Low

Present summary with actionable task list.

### 5. Offer to Fix

Ask if the user wants to address specific findings.
