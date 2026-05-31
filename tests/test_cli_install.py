import json

import pytest
from pytest_bdd import given, when, then, scenarios, parsers

from common_ai.installer import Installer
from common_ai.registry import Registry

scenarios("features/cli_install.feature")


@pytest.fixture
def target_dir(tmp_path):
    return tmp_path / "target"


@pytest.fixture
def context():
    return {}


@given("a target directory")
def given_target(target_dir, context):
    context["target"] = target_dir


@given("the registry")
def given_registry(context):
    context["registry"] = Registry()


@when(parsers.parse('I run install with tool "{tool}" name "{name}" skills "{skills}" kbs "{kbs}" and dry-run'))
def run_dry_run(tool, name, skills, kbs, context, capsys):
    installer = Installer(tool=tool, name=name, target=str(context["target"]), skills=[skills], kbs=[kbs])
    installer.dry_run()
    context["output"] = capsys.readouterr().out


@when(parsers.parse('I run install with tool "{tool}" name "{name}" skills "{skills}" kbs "{kbs}"'))
def run_install(tool, name, skills, kbs, context):
    installer = Installer(tool=tool, name=name, target=str(context["target"]), skills=[skills], kbs=[kbs])
    installer.execute()


@when(parsers.parse('I run install with tool "{tool}" name "{name}" and no filters'))
def run_install_all(tool, name, context):
    installer = Installer(tool=tool, name=name, target=str(context["target"]), skills=[], kbs=[])
    installer.execute()


@when(parsers.parse('I run install with tool "{tool}" name "{name}" skills "{skills}" and kbs "{kbs}"'))
def run_install_multi_kbs(tool, name, skills, kbs, context):
    kb_list = [k.strip() for k in kbs.split(",")]
    installer = Installer(tool=tool, name=name, target=str(context["target"]), skills=[skills], kbs=kb_list)
    installer.execute()


@when(parsers.parse('I run install with tool "{tool}" name "{name}" skills "{skills}" kbs "{kbs}" and capture output'))
def run_install_capture(tool, name, skills, kbs, context, capsys):
    installer = Installer(tool=tool, name=name, target=str(context["target"]), skills=[skills], kbs=[kbs])
    installer.execute()
    context["output"] = capsys.readouterr().out


@when(parsers.parse('I search for skill "{name}"'))
def search_skill(name, context):
    context["results"] = context["registry"].find_skills(name)


@when(parsers.parse('I search for kb "{name}"'))
def search_kb(name, context):
    context["results"] = context["registry"].find_kbs(name)


@then(parsers.parse('the output contains "{text}"'))
def output_contains(text, context):
    assert text in context["output"]


@then("no files are written")
def no_files(context):
    assert not context["target"].exists()


@then(parsers.parse('the file "{path}" exists in target'))
def file_exists(path, context):
    assert (context["target"] / path).exists()


@then(parsers.parse('the agent JSON exists at parent with name "{name}"'))
def agent_json_exists(name, context):
    agent_file = context["target"].parent / f"{name}-agent.json"
    assert agent_file.exists()
    data = json.loads(agent_file.read_text())
    assert data["name"] == name


@then(parsers.parse("skills directory contains more than {count:d} skill"))
def skills_count(count, context):
    skills_dir = context["target"] / "skills"
    skill_files = list(skills_dir.rglob("SKILL.md"))
    assert len(skill_files) > count


@then(parsers.parse("knowledge-bases directory contains more than {count:d} scope"))
def kbs_count(count, context):
    kb_dir = context["target"] / "knowledge-bases"
    scopes = [d for d in kb_dir.iterdir() if d.is_dir()]
    assert len(scopes) > count


@then(parsers.parse('the agent JSON has name "{name}"'))
def agent_json_name(name, context):
    agent_file = context["target"].parent / f"{name}-agent.json"
    data = json.loads(agent_file.read_text())
    assert data["name"] == name


@then("the agent JSON has a skill resource")
def agent_json_has_skill(context):
    agent_files = list(context["target"].parent.glob("*-agent.json"))
    data = json.loads(agent_files[0].read_text())
    skill_resources = [r for r in data["resources"] if isinstance(r, str) and "skill://" in r]
    assert len(skill_resources) == 1


@then(parsers.parse("the agent JSON has {count:d} knowledge base resources"))
def agent_json_kb_count(count, context):
    agent_files = list(context["target"].parent.glob("*-agent.json"))
    data = json.loads(agent_files[0].read_text())
    kb_resources = [r for r in data["resources"] if isinstance(r, dict) and r.get("type") == "knowledgeBase"]
    assert len(kb_resources) == count


@then(parsers.parse('the file "{path}" contains "{text}"'))
def file_contains(path, text, context):
    content = (context["target"] / path).read_text()
    assert text in content


@then(parsers.parse('the file "{path}" does not contain "{text}"'))
def file_not_contains(path, text, context):
    content = (context["target"] / path).read_text()
    assert text not in content


@then(parsers.parse("exactly {count:d} skill is found"))
def skill_found_count(count, context):
    assert len(context["results"]) == count


@then(parsers.parse("exactly {count:d} kb is found"))
def kb_found_count(count, context):
    assert len(context["results"]) == count
