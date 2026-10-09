"""scripts/sync.py against real git repositories: a local "GitHub" (bare repo) and clones.

    pytest tests
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync.py"


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def env(tmp_path, monkeypatch):
    for key, value in {
        "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com",
    }.items():
        monkeypatch.setenv(key, value)
    remote = tmp_path / "TokDar2410621" / "wealth-framework.git"
    remote.parent.mkdir()
    run("init", "--quiet", "--bare", "--initial-branch=main", str(remote))
    author = tmp_path / "author"
    run("clone", "--quiet", str(remote), str(author))
    (author / "scripts").mkdir()
    shutil.copy(SCRIPT, author / "scripts" / "sync.py")
    (author / "SKILL.md").write_text("v1\n", encoding="utf-8")
    (author / "cheatsheet.md").write_text("rules v1\n", encoding="utf-8")
    run("add", ".", cwd=author)
    run("commit", "--quiet", "-m", "v1", cwd=author)
    run("push", "--quiet", "origin", "main", cwd=author)
    return {"tmp": tmp_path, "remote": remote, "author": author}


def publish(env, name: str, content: str) -> str:
    (env["author"] / name).write_text(content, encoding="utf-8")
    run("commit", "--quiet", "-am", f"update {name}", cwd=env["author"])
    run("push", "--quiet", "origin", "main", cwd=env["author"])
    return run("rev-parse", "HEAD", cwd=env["author"])


def install(env) -> Path:
    skill = env["tmp"] / "skills" / "wealth-framework"
    run("clone", "--quiet", str(env["remote"]), str(skill))
    return skill


def sync(skill: Path) -> dict:
    out = subprocess.run([sys.executable, str(skill / "scripts" / "sync.py")], capture_output=True, text=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_up_to_date(env):
    assert sync(install(env))["status"] == "up_to_date"


def test_behind_is_updated_and_reports_skill_md_change(env):
    skill = install(env)
    new = publish(env, "SKILL.md", "v2\n")
    state = sync(skill)
    assert state["status"] == "updated"
    assert state["skill_md_changed"] is True
    assert run("rev-parse", "HEAD", cwd=skill) == new


def test_update_without_skill_md_change(env):
    skill = install(env)
    publish(env, "cheatsheet.md", "rules v2\n")
    state = sync(skill)
    assert state["status"] == "updated"
    assert state["skill_md_changed"] is False
    assert (skill / "cheatsheet.md").read_text(encoding="utf-8") == "rules v2\n"


def test_merged_branch_goes_back_to_main(env):
    skill = install(env)
    run("checkout", "--quiet", "-b", "old", cwd=skill)
    new = publish(env, "cheatsheet.md", "rules v2\n")
    assert sync(skill)["status"] == "updated"
    assert run("rev-parse", "--abbrev-ref", "HEAD", cwd=skill) == "main"
    assert run("rev-parse", "HEAD", cwd=skill) == new


def test_local_edits_never_overwritten(env):
    skill = install(env)
    (skill / "cheatsheet.md").write_text("my notes\n", encoding="utf-8")
    publish(env, "cheatsheet.md", "rules v2\n")
    state = sync(skill)
    assert state["status"] == "read_origin_main"
    assert (skill / "cheatsheet.md").read_text(encoding="utf-8") == "my notes\n"
    assert run("show", "origin/main:cheatsheet.md", cwd=skill) == "rules v2"


def test_offline_keeps_local_copy(env):
    skill = install(env)
    env["remote"].rename(env["remote"].with_name("elsewhere.git"))
    state = sync(skill)
    assert state["status"] == "offline"
    assert "NOT verified" in state["detail"]


def test_copied_install_is_reported(env):
    copy = env["tmp"] / "copied" / "wealth-framework"
    shutil.copytree(env["author"], copy, ignore=shutil.ignore_patterns(".git"))
    assert sync(copy)["status"] == "not_a_clone"


def test_wrong_repository_is_an_error(env, tmp_path):
    other = tmp_path / "other.git"
    run("init", "--quiet", "--bare", "--initial-branch=main", str(other))
    skill = install(env)
    run("remote", "set-url", "origin", str(other), cwd=skill)
    assert sync(skill)["status"] == "error"
