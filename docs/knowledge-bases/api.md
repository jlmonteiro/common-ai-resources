# :material-api: API

Standards for REST API design, documentation, and backward compatibility.

<div class="grid cards" markdown>

- :material-file-document-edit:{ .lg .middle } **API First**

    ---

    Define OAS before code. Review, accept, then implement.

- :material-routes:{ .lg .middle } **URL Design**

    ---

    Plural nouns, kebab-case, max 3 nesting levels.

- :material-alert-circle:{ .lg .middle } **Error Handling**

    ---

    RFC 7807 Problem Details, resilience status codes (429, 503).

- :material-book-open-page-variant:{ .lg .middle } **Pagination**

    ---

    Offset-based with envelope, default 20, max 100.

- :material-source-branch:{ .lg .middle } **Versioning**

    ---

    URL path (`/api/v1/`), sunset headers, backward compatibility.

- :material-clock-outline:{ .lg .middle } **Data Types**

    ---

    ISO 8601 timestamps/durations, UTC, strings for money.

</div>

## Source

| File | Description |
|------|-------------|
| [`rest-standards.md`](https://github.com/jlmonteiro/common-ai-resources/blob/main/resources/knowledge-bases/api/rest-standards.md) | Full REST API standards |
