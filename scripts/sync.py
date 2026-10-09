#!/usr/bin/env python3
"""Check that this skill is up to date with GitHub, and update it if needed.

    python scripts/sync.py

The skill is meant to be installed as a git clone:
    git clone https://github.com/TokDar2410621/wealth-framework ~/.claude/skills/wealth-framework
so updating the clone updates the skill itself.

The last output line is JSON: {"status", "path", "ref", "detail", "skill_md_changed"}

    status  up_to_date        on main and current: nothing to do
            updated           was behind with no local work: now current
            read_origin_main  local work not merged into main: nothing touched,
                              read the current files from origin/main (git show)
            offline           GitHub unreachable: local copy used, freshness NOT verified
            not_a_clone       installed by copying files: freshness cannot be checked
            error             not this skill's repository
    ref     what to read: "HEAD" (the files on disk) or "origin/main"
    skill_md_changed  true when the update changed SKILL.md: re-read it before going on

Never destroys anything: no local change, no unpushed commit. Needs git and Python 3.8+.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_SLUG = "tokdar2410621/wealth-framework"
BRANCH = "main"
TIMEOUT = 120


def git(path: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, timeout=TIMEOUT)


def result(status: str, path: Path, ref: str, detail: str, changed: bool = False) -> dict:
    return {"status": status, "path": str(path), "ref": ref, "detail": detail, "skill_md_changed": changed}


def fast_forward(path: Path) -> bool:
    return git(path, "merge", "--quiet", "--ff-only", f"origin/{BRANCH}").returncode == 0


def skill_md_changed(path: Path, before: str) -> bool:
    return bool(git(path, "diff", "--name-only", before, "HEAD", "--", "SKILL.md").stdout.strip())


def sync(repo: Path) -> dict:
    if not (repo / ".git").exists():
        return result(
            "not_a_clone", repo, "HEAD",
            "installed by copy: reinstall with git clone https://github.com/TokDar2410621/wealth-framework to get updates",
        )
    origin = git(repo, "remote", "get-url", "origin").stdout.strip().lower().replace("\\", "/")
    if REPO_SLUG not in origin:
        return result("error", repo, "", f"origin is not {REPO_SLUG}")

    if git(repo, "fetch", "--quiet", "origin", BRANCH).returncode != 0:
        return result("offline", repo, "HEAD", "GitHub unreachable: local copy used, freshness NOT verified")

    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    dirty = bool(git(repo, "status", "--porcelain", "--untracked-files=no").stdout.strip())
    behind = int(git(repo, "rev-list", "--count", f"HEAD..origin/{BRANCH}").stdout.strip() or 0)
    ahead = int(git(repo, "rev-list", "--count", f"origin/{BRANCH}..HEAD").stdout.strip() or 0)
    before = git(repo, "rev-parse", "HEAD").stdout.strip()

    if branch == BRANCH:
        if behind == 0:
            return result("up_to_date", repo, "HEAD", "main is current")
        if not dirty and ahead == 0 and fast_forward(repo):
            return result("updated", repo, "HEAD", f"{behind} commit(s) pulled", skill_md_changed(repo, before))
        reason = "local files modified" if dirty else "local main diverged from origin/main"
        return result("read_origin_main", repo, f"origin/{BRANCH}", f"{reason}: nothing touched")

    merged = git(repo, "merge-base", "--is-ancestor", "HEAD", f"origin/{BRANCH}").returncode == 0
    if merged and not dirty and git(repo, "checkout", "--quiet", BRANCH).returncode == 0:
        if fast_forward(repo):
            return result("updated", repo, "HEAD", f"branch {branch} was already merged: back on main, current",
                          skill_md_changed(repo, before))
        return result("read_origin_main", repo, f"origin/{BRANCH}", "local main diverged from origin/main: nothing merged")
    reason = "local files modified" if dirty else "commits not merged into main"
    return result("read_origin_main", repo, f"origin/{BRANCH}", f"branch {branch}, {reason}: nothing touched")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    try:
        state = sync(repo)
    except FileNotFoundError:
        state = result("error", repo, "", "git is not installed")
    except subprocess.TimeoutExpired:
        state = result("offline", repo, "HEAD", "git too slow (timeout): freshness NOT verified")
    print(f"[wealth-framework] {state['status']}: {state['detail']}")
    print(json.dumps(state))
    return 1 if state["status"] == "error" else 0


if __name__ == "__main__":
    sys.exit(main())
