#!/usr/bin/env python3
"""Decision journal: every verdict with its cheapest test, then what really happened.

This is Dalio's loop (DAL-4: pain + reflection = progress) made concrete: the filter states a
test, a deadline and the number that decides; once the deadline passes, the result comes back
and the filter's own record builds up.

    python scripts/journal.py add --decision "Cold email for local SEO" --verdict conditions \\
        --laws FLE-3,FLS-12 --test "46 prospects x 3 touches, one vertical" \\
        --deadline 2026-11-15 --decides "1 reply asking for the audit"
    python scripts/journal.py due          # tests past their deadline, still open
    python scripts/journal.py close 3 --executed yes --outcome not_met --note "0 replies on 46"
    python scripts/journal.py stats

The journal is a local file, never inside the skill folder and never published:
$WEALTH_JOURNAL if set, else ~/.wealth-framework/journal.jsonl. It is append-only (one JSON
event per line). The last output line of every command is JSON.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from collections import Counter
from pathlib import Path

VERDICTS = ("go", "conditions", "no-go")
OUTCOMES = ("met", "not_met")


def journal_path() -> Path:
    custom = os.environ.get("WEALTH_JOURNAL", "").strip()
    return Path(custom).expanduser() if custom else Path.home() / ".wealth-framework" / "journal.jsonl"


def read_events(path: Path) -> tuple[list[dict], int]:
    """All valid events, and the number of unreadable lines (kept in the file, skipped here)."""
    if not path.exists():
        return [], 0
    events, bad = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            bad += 1
    return events, bad


def append(path: Path, event: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def decisions(events: list[dict]) -> dict[int, dict]:
    """Decisions by id, each with its result if one was recorded (the last one wins)."""
    table: dict[int, dict] = {}
    for e in events:
        if e.get("type") == "decision":
            table[e["id"]] = dict(e, result=None)
        elif e.get("type") == "result" and e.get("id") in table:
            table[e["id"]]["result"] = e
    return table


def today(value: str | None) -> dt.date:
    return dt.date.fromisoformat(value) if value else dt.date.today()


def cmd_add(args, path: Path) -> dict:
    deadline = dt.date.fromisoformat(args.deadline)
    events, _ = read_events(path)
    new_id = max([e["id"] for e in events if e.get("type") == "decision"], default=0) + 1
    event = {
        "type": "decision", "id": new_id, "date": today(args.date).isoformat(),
        "decision": args.decision, "verdict": args.verdict,
        "laws": [x.strip().upper() for x in args.laws.split(",") if x.strip()] if args.laws else [],
        "test": args.test, "deadline": deadline.isoformat(), "decides": args.decides,
    }
    append(path, event)
    print(f"Logged decision #{new_id}: test due {deadline.isoformat()}.")
    return event


def open_items(table: dict[int, dict]) -> list[dict]:
    return [d for d in table.values() if d["result"] is None]


def cmd_due(args, path: Path) -> list[dict]:
    events, _ = read_events(path)
    limit = today(args.today)
    due = [d for d in open_items(decisions(events)) if dt.date.fromisoformat(d["deadline"]) <= limit]
    if not due:
        print("No test past its deadline.")
    for d in due:
        print(f"#{d['id']} ({d['deadline']}): {d['decision']} | test: {d['test']} | decides: {d['decides']}")
    return due


def cmd_open(args, path: Path) -> list[dict]:
    events, _ = read_events(path)
    items = open_items(decisions(events))
    for d in items:
        print(f"#{d['id']} due {d['deadline']}: {d['decision']}")
    if not items:
        print("No open decision.")
    return items


def cmd_close(args, path: Path) -> dict:
    events, _ = read_events(path)
    table = decisions(events)
    if args.id not in table:
        raise ValueError(f"no decision #{args.id}")
    executed = args.executed == "yes"
    if executed and args.outcome not in OUTCOMES:
        raise ValueError("an executed test needs --outcome met or not_met")
    event = {
        "type": "result", "id": args.id, "date": today(args.date).isoformat(),
        "executed": executed, "outcome": args.outcome if executed else "void", "note": args.note or "",
    }
    append(path, event)
    label = event["outcome"] if executed else "void: the test was not run (execution, not design)"
    print(f"Closed #{args.id}: {label}.")
    return event


def compute_stats(table: dict[int, dict]) -> dict:
    closed = [d for d in table.values() if d["result"] is not None]
    executed = [d for d in closed if d["result"]["executed"]]
    by_verdict = {}
    for v in VERDICTS:
        runs = [d for d in executed if d["verdict"] == v]
        by_verdict[v] = {
            "decisions": sum(1 for d in table.values() if d["verdict"] == v),
            "tests_run": len(runs),
            "met": sum(1 for d in runs if d["result"]["outcome"] == "met"),
            "not_met": sum(1 for d in runs if d["result"]["outcome"] == "not_met"),
        }
    in_misses = Counter(law for d in executed if d["result"]["outcome"] == "not_met" for law in d["laws"])
    return {
        "decisions": len(table),
        "open": len(table) - len(closed),
        "closed": len(closed),
        "execution_rate": round(len(executed) / len(closed), 2) if closed else None,
        "met_rate_when_run": round(sum(1 for d in executed if d["result"]["outcome"] == "met") / len(executed), 2) if executed else None,
        "by_verdict": by_verdict,
        "laws_in_missed_tests": dict(in_misses.most_common(10)),
    }


def cmd_stats(args, path: Path) -> dict:
    events, bad = read_events(path)
    s = compute_stats(decisions(events))
    print(f"{s['decisions']} decisions, {s['open']} open, {s['closed']} closed.")
    if s["closed"]:
        print(f"Tests actually run: {s['execution_rate']:.0%} of closed decisions (FLE-7: a test not run decides nothing).")
    if s["met_rate_when_run"] is not None:
        print(f"Tests met when run: {s['met_rate_when_run']:.0%}.")
    if bad:
        print(f"Warning: {bad} unreadable line(s) skipped in {path}.")
    s["unreadable_lines"] = bad
    return s


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Decision journal for the wealth-framework filter.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="log a verdict and its cheapest test")
    add.add_argument("--decision", required=True)
    add.add_argument("--verdict", required=True, choices=VERDICTS)
    add.add_argument("--laws", default="", help="comma-separated law IDs, e.g. HOR-2,FLE-3")
    add.add_argument("--test", required=True, help="the cheapest test, one action")
    add.add_argument("--deadline", required=True, help="YYYY-MM-DD")
    add.add_argument("--decides", required=True, help="the number that decides")
    add.add_argument("--date", help="YYYY-MM-DD (default: today)")

    due = sub.add_parser("due", help="open tests past their deadline")
    due.add_argument("--today", help="YYYY-MM-DD (default: today)")
    sub.add_parser("open", help="all open decisions")

    close = sub.add_parser("close", help="record what happened")
    close.add_argument("id", type=int)
    close.add_argument("--executed", required=True, choices=("yes", "no"))
    close.add_argument("--outcome", choices=OUTCOMES, help="required when the test was executed")
    close.add_argument("--note", default="")
    close.add_argument("--date", help="YYYY-MM-DD (default: today)")

    sub.add_parser("stats", help="the filter's record")

    args = parser.parse_args()
    path = journal_path()
    commands = {"add": cmd_add, "due": cmd_due, "open": cmd_open, "close": cmd_close, "stats": cmd_stats}
    try:
        out = commands[args.command](args, path)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
