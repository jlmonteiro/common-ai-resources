Feature: Knowledge base chunking
  The MCP server splits markdown files into searchable chunks

  Scenario: Split markdown by headings
    Given a markdown file with multiple headings
    When the file is chunked
    Then each heading section becomes a separate chunk

  Scenario: Large section is split recursively
    Given a markdown file with a section exceeding 500 characters
    When the file is chunked
    Then the large section is split into multiple chunks with overlap

  Scenario: Small section stays intact
    Given a markdown file with a section under 500 characters
    When the file is chunked
    Then the section remains as a single chunk

  Scenario: Heading hierarchy is preserved in chunk text
    Given a markdown file with nested headings
    When the file is chunked
    Then each chunk contains its heading breadcrumb

  Scenario: Scope is derived from first directory level
    Given a markdown file at "java/resilience.md"
    When the file is chunked
    Then the scope is "java"

  Scenario: Root level file gets scope general
    Given a markdown file at "README.md"
    When the file is chunked
    Then the scope is "general"

  Scenario: Empty file produces no chunks
    Given an empty markdown file
    When the file is chunked
    Then no chunks are produced

  Scenario: File with no headings produces single chunk
    Given a markdown file with no headings
    When the file is chunked
    Then a single chunk is produced
