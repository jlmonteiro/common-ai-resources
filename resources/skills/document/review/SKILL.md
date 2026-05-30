---
name: "review-document"
description: "Interactive item-by-item review of a document. Presents each section for feedback before moving to the next. Use when user says 'review this document', 'review the KB', 'go through this file', 'review item by item', or 'let me review'."
---

# Review Document

## Step 1: Read and Parse

Read the entire document to understand its structure. Break it into logical review items (sections, paragraphs, or individual points depending on document type).

## Step 2: Present Items One at a Time

For each item, use this format:

```
**§ [Section Path]**

[Content of the item exactly as written]

---

[Context: why this item matters, how it relates to the rest, or potential issues]

[Examples: if applicable, show good/bad examples or alternatives]

---

Thoughts?
```

## Step 3: Handle Feedback

Wait for the user's response:

- **"ok" or similar** → item accepted as-is, move to next
- **Feedback provided** → discuss, propose changes, apply once agreed, then move on
- **Question asked** → answer it, then re-present the item for a decision

## Step 4: Apply Changes

After agreement on a change:

1. Apply the modification to the file
2. Confirm briefly (do NOT re-show the full item)
3. Move to the next item

## Step 5: Summary

After the last item, report:

- Total items reviewed
- Items accepted without changes
- Items modified
- Offer to show the final document or commit the changes

## Rules

- Never skip items or batch multiple items unless the user explicitly asks
- Never modify the document without explicit approval
- Keep context and examples concise — focus is on the item content
- Use the section path (breadcrumb) so the user knows where they are
