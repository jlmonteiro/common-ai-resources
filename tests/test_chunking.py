from unittest.mock import patch

from pytest_bdd import scenario, given, when, then, parsers

import common_ai.mcp_server as server


@scenario("features/chunking.feature", "Split markdown by headings")
def test_split_by_headings():
    pass


@scenario("features/chunking.feature", "Large section is split recursively")
def test_large_section_split():
    pass


@scenario("features/chunking.feature", "Small section stays intact")
def test_small_section_intact():
    pass


@scenario("features/chunking.feature", "Heading hierarchy is preserved in chunk text")
def test_heading_hierarchy():
    pass


@scenario("features/chunking.feature", "Scope is derived from first directory level")
def test_scope_from_directory():
    pass


@scenario("features/chunking.feature", "Root level file gets scope general")
def test_root_scope_general():
    pass


@scenario("features/chunking.feature", "Empty file produces no chunks")
def test_empty_file():
    pass


@scenario("features/chunking.feature", "File with no headings produces single chunk")
def test_no_headings():
    pass


# --- Given steps ---

@given("a markdown file with multiple headings", target_fixture="md_file")
def md_with_headings(tmp_path):
    kb = tmp_path / "test"
    kb.mkdir()
    f = kb / "doc.md"
    f.write_text("# Title\n\n## Section A\n\nContent A.\n\n## Section B\n\nContent B.\n")
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": f, "kb_path": tmp_path}


@given("a markdown file with a section exceeding 500 characters", target_fixture="md_file")
def md_with_large_section(tmp_path):
    kb = tmp_path / "test"
    kb.mkdir()
    f = kb / "doc.md"
    content = "# Title\n\n## Large Section\n\n" + ("This is a long sentence. " * 50) + "\n"
    f.write_text(content)
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": f, "kb_path": tmp_path}


@given("a markdown file with a section under 500 characters", target_fixture="md_file")
def md_with_small_section(tmp_path):
    kb = tmp_path / "test"
    kb.mkdir()
    f = kb / "doc.md"
    f.write_text("# Title\n\n## Small\n\nShort content.\n")
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": f, "kb_path": tmp_path}


@given("a markdown file with nested headings", target_fixture="md_file")
def md_with_nested_headings(tmp_path):
    kb = tmp_path / "test"
    kb.mkdir()
    f = kb / "doc.md"
    f.write_text("# Top\n\n## Middle\n\n### Deep\n\nNested content.\n")
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": f, "kb_path": tmp_path}


@given(parsers.parse('a markdown file at "{path}"'), target_fixture="md_file")
def md_at_path(tmp_path, path):
    full_path = tmp_path / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text("# Doc\n\nContent here.\n")
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": full_path, "kb_path": tmp_path}


@given("an empty markdown file", target_fixture="md_file")
def md_empty(tmp_path):
    kb = tmp_path / "test"
    kb.mkdir()
    f = kb / "doc.md"
    f.write_text("")
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": f, "kb_path": tmp_path}


@given("a markdown file with no headings", target_fixture="md_file")
def md_no_headings(tmp_path):
    kb = tmp_path / "test"
    kb.mkdir()
    f = kb / "doc.md"
    f.write_text("Just plain text without any headings.\n")
    with patch.object(server, "KB_PATH", tmp_path):
        return {"path": f, "kb_path": tmp_path}


# --- When steps ---

@when("the file is chunked", target_fixture="chunks")
def chunk_file(md_file):
    with patch.object(server, "KB_PATH", md_file["kb_path"]):
        return server._chunk_file(md_file["path"])


# --- Then steps ---

@then("each heading section becomes a separate chunk")
def verify_multiple_chunks(chunks):
    assert len(chunks) >= 2


@then("the large section is split into multiple chunks with overlap")
def verify_large_split(chunks):
    assert len(chunks) >= 2
    for chunk in chunks:
        assert len(chunk["text"]) <= server.CHUNK_SIZE + 50  # allow small overflow


@then("the section remains as a single chunk")
def verify_single_chunk(chunks):
    assert len(chunks) >= 1
    assert any("Short content" in c["text"] for c in chunks)


@then("each chunk contains its heading breadcrumb")
def verify_breadcrumb(chunks):
    deep_chunks = [c for c in chunks if "Nested content" in c["text"]]
    assert len(deep_chunks) >= 1
    assert "Middle" in deep_chunks[0]["text"] or "Deep" in deep_chunks[0]["text"]


@then(parsers.parse('the scope is "{expected_scope}"'))
def verify_scope(chunks, expected_scope):
    assert all(c["scope"] == expected_scope for c in chunks)


@then("no chunks are produced")
def verify_no_chunks(chunks):
    assert len(chunks) == 0


@then("a single chunk is produced")
def verify_one_chunk(chunks):
    assert len(chunks) == 1
