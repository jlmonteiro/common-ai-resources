Feature: Knowledge base listing and scopes
  The MCP server provides tools to discover available knowledge bases and scopes

  Scenario: List scopes returns all top-level directories
    Given the knowledge base contains directories "docker", "java", "git"
    When I list scopes
    Then the result contains "docker", "java", "git"

  Scenario: List scopes on empty KB
    Given an empty knowledge base directory
    When I list scopes
    Then the result is "No scopes found."

  Scenario: List knowledge bases returns all topics
    Given the knowledge base contains directories "docker", "java", "git"
    When I list knowledge bases
    Then the result contains "docker", "java", "git"

  Scenario: List knowledge bases on empty directory
    Given an empty knowledge base directory
    When I list knowledge bases
    Then the result is "No knowledge bases found."

  Scenario: Index is built only once
    Given the knowledge base is indexed
    When I search twice for "test"
    Then the index is not rebuilt on the second call
