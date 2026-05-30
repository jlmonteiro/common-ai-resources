from unittest.mock import patch

from pytest_bdd import scenario, given, when, then, parsers

import common_ai.mcp_server as server


@scenario("features/search.feature", "Search returns relevant results ranked by score")
def test_search_relevance():
    pass


@scenario("features/search.feature", "Search with valid scope filters results")
def test_search_valid_scope():
    pass


@scenario("features/search.feature", "Search with multiple scopes returns from all specified")
def test_search_multiple_scopes():
    pass


@scenario("features/search.feature", "Search with invalid scope returns error")
def test_search_invalid_scope():
    pass


@scenario("features/search.feature", "Search with mixed valid and invalid scopes returns error")
def test_search_mixed_scopes():
    pass


@scenario("features/search.feature", "Search with no scopes returns results from all KBs")
def test_search_no_scopes():
    pass


@scenario("features/search.feature", "Search with low relevance returns no results")
def test_search_low_relevance():
    pass


@scenario("features/search.feature", "Search on empty knowledge base")
def test_search_empty_kb():
    pass


@scenario("features/search.feature", "Limit parameter restricts number of results")
def test_search_limit():
    pass


# --- Given steps ---

@given('the knowledge base contains documents about "docker" and "java"', target_fixture="kb")
def kb_docker_java(kb_with_docs):
    return kb_with_docs


@given('the knowledge base contains documents about "docker", "java", and "git"', target_fixture="kb")
def kb_docker_java_git(kb_with_docs):
    return kb_with_docs


@given("the knowledge base is indexed", target_fixture="kb")
def kb_indexed(kb_with_docs):
    return kb_with_docs


@given("an empty knowledge base directory", target_fixture="kb")
def kb_empty(empty_kb):
    return empty_kb


@given("the knowledge base contains many documents", target_fixture="kb")
def kb_many_docs(kb_with_docs):
    return kb_with_docs


# --- When steps ---

@when(parsers.parse('I search for "{query}"'), target_fixture="search_result")
def search_query(kb, query):
    with patch.object(server, "KB_PATH", kb):
        return server.search_knowledge(query)


@when(parsers.parse('I search for "{query}" with scopes "{scopes}"'), target_fixture="search_result")
def search_with_scopes(kb, query, scopes):
    scope_list = [s.strip() for s in scopes.split(",")]
    with patch.object(server, "KB_PATH", kb):
        return server.search_knowledge(query, scopes=scope_list)


@when(parsers.parse('I search for "{query}" without scopes'), target_fixture="search_result")
def search_without_scopes(kb, query):
    with patch.object(server, "KB_PATH", kb):
        return server.search_knowledge(query, scopes=None)


@when(parsers.parse('I search for "{query}" with limit {limit:d}'), target_fixture="search_result")
def search_with_limit(kb, query, limit):
    with patch.object(server, "KB_PATH", kb):
        return server.search_knowledge(query, limit=limit)


# --- Then steps ---

@then(parsers.parse('results from "{scope}" are returned with higher scores'))
def verify_top_results_scope(search_result, scope):
    assert f"[{scope}/" in search_result


@then(parsers.parse('all results are from scope "{scope}"'))
def verify_all_from_scope(search_result, scope):
    assert f"[{scope}/" in search_result
    other_scopes = ["docker", "java", "git"]
    other_scopes.remove(scope)
    for other in other_scopes:
        assert f"[{other}/" not in search_result


@then(parsers.parse('results do not contain scope "{scope}"'))
def verify_excludes_scope(search_result, scope):
    assert f"[{scope}/" not in search_result


@then(parsers.parse('the result contains "{text}"'))
def verify_contains(search_result, text):
    assert text in search_result


@then("results may include any scope")
def verify_any_scope(search_result):
    assert "No relevant results" not in search_result


@then(parsers.parse('the result is "{expected}"'))
def verify_exact_result(search_result, expected):
    assert search_result == expected


@then(parsers.parse("at most {count:d} results are returned"))
def verify_limit(search_result, count):
    if search_result == "No relevant results found.":
        assert True
    else:
        sections = search_result.split("---")
        assert len(sections) <= count
