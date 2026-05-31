---
name: "review-skill"
description: "Review a skill by validating against knowledge bases and simulating execution step by step. Use when user says 'review skill', 'check this skill', 'simulate skill', or 'walk me through this skill'."
---

# Review Skill

## Prerequisites

Search the **ai/skills** knowledge base for skill development guidelines (frontmatter, description quality, structure, activation).

## Step 1: Validate Structure

Read the SKILL.md file and check against the skills development KB:

- [ ] Has YAML frontmatter with `name` and `description`
- [ ] Name is kebab-case
- [ ] Description contains functional intent + trigger phrases
- [ ] Description is machine-facing, not human-facing
- [ ] Steps are numbered and focused
- [ ] Each step has clear success criteria
- [ ] One skill = one workflow (not multiple concerns)

Report any violations before proceeding.

## Step 2: Validate Against Knowledge Bases

For each step in the skill, search relevant knowledge bases to verify:

- Instructions align with documented standards
- Referenced KBs exist and are relevant
- No contradictions with established conventions
- No missing KB references that should be consulted

Report findings.

## Step 3: Simulate Execution

Walk through the skill step by step, presenting each as if executing it:

For each step:

1. **Show the step** — what the agent would do
2. **Provide context** — why this step matters, what it achieves
3. **Show an example** — concrete input/output for a realistic scenario
4. **Wait for feedback** — ask "Thoughts?" before moving to the next step

If the user provides feedback:
- Discuss and propose changes
- Apply changes once agreed
- Then move to the next step

If the user says "ok":
- Move to the next step

## Step 4: Summary

After all steps are simulated:

- Total steps reviewed
- Issues found (structure, KB alignment, logic gaps)
- Steps accepted vs modified
- Offer to apply all changes
