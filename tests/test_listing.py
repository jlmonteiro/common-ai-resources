from unittest.mock import patch

from pytest_bdd import scenario, given, when, then, parsers

import common_ai.mcp_server as server


@scenario("features/listing.feature", "List scopes returns all top-level directories")
def test_list_scopes():
    pass


@scenario("features/listing.feature", "List scopes on empty KB")
def test_list_scopes_empty():
    pass


@scenario("features/listing.feature", "List knowledge bases returns all topics")
def test_list_kbs():
    pass


@scenario("features/listing.feature", "List knowledge bases on empty directory")
def test_list_kbs_empty():
    pass


@scenario("features/listing.feature", "Index is built only once")
def test_index_cached():
    pass


# --- Given steps ---

@given(parsers.parse('the knowledge base contains directories "{dirs}"'), target_fixture="kb")
def kb_with_dirs(kb_with_docs):
    return kb_with_docs


@given("an empty knowledge base directory", target_fixture="kb")
def kb_empty(empty_kb):
    return empty_kb


@given("the knowledge base is indexed", target_fixture="kb")
def kb_indexed(kb_with_docs):
    with patch.object(server, "KB_PATH", kb_with_docs):
        server._build_index()
    return kb_with_docs


# --- When steps ---

@when("I list scopes", target_fixture="result")
def do_list_scopes(kb):
    with patch.object(server, "KB_PATH", kb):
        return server.list_scopes()


@when("I list knowledge bases", target_fixture="result")
def do_list_kbs(kb):
    with patch.object(server, "KB_PATH", kb):
        return server.list_knowledge_bases()


@when(parsers.parse('I search twice for "{query}"'), target_fixture="result")
def search_twice(kb):
    with patch.object(server, "KB_PATH", kb):
        server.search_knowledge("test")
        chunks_after_first = len(server._chunks)
        server.search_knowledge("test")
        chunks_after_second = len(server._chunks)
        return {"first": chunks_after_first, "second": chunks_after_second}


# --- Then steps ---

@then(parsers.parse('the result contains "{items}"'))
def verify_contains_items(result, items):
    for item in items.split('", "'):
        item = item.strip('"')
        assert item in result


@then(parsers.parse('the result is "{expected}"'))
def verify_exact(result, expected):
    assert result == expected


@then("the index is not rebuilt on the second call")
def verify_index_cached(result):
    assert result["first"] == result["second"]
    assert result["first"] > 0
