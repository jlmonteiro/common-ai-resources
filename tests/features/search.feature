Feature: Knowledge base search
  The MCP server provides semantic search over indexed knowledge bases

  Scenario: Search returns relevant results ranked by score
    Given the knowledge base contains documents about "docker" and "java"
    When I search for "Dockerfile best practices"
    Then results from "docker" are returned with higher scores

  Scenario: Search with valid scope filters results
    Given the knowledge base contains documents about "docker" and "java"
    When I search for "best practices" with scopes "java"
    Then all results are from scope "java"

  Scenario: Search with multiple scopes returns from all specified
    Given the knowledge base contains documents about "docker", "java", and "git"
    When I search for "conventions" with scopes "docker,java"
    Then results do not contain scope "git"

  Scenario: Search with invalid scope returns error
    Given the knowledge base is indexed
    When I search for "test" with scopes "nonexistent"
    Then the result contains "Invalid scope(s): nonexistent"
    And the result contains "Available:"

  Scenario: Search with mixed valid and invalid scopes returns error
    Given the knowledge base is indexed
    When I search for "test" with scopes "java,nonexistent"
    Then the result contains "Invalid scope(s): nonexistent"

  Scenario: Search with no scopes returns results from all KBs
    Given the knowledge base contains documents about "docker" and "java"
    When I search for "conventions" without scopes
    Then results may include any scope

  Scenario: Search with low relevance returns no results
    Given the knowledge base is indexed
    When I search for "xyzzy quantum flux capacitor" with scopes "nonexistent_scope_to_force_empty"
    Then the result contains "Invalid scope(s)"

  Scenario: Search on empty knowledge base
    Given an empty knowledge base directory
    When I search for "anything"
    Then the result is "No knowledge base documents found."

  Scenario: Limit parameter restricts number of results
    Given the knowledge base contains many documents
    When I search for "conventions" with limit 2
    Then at most 2 results are returned
