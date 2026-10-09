#!/usr/bin/env python3
"""Interview the user about their numbers, then print an AGENT BRIEF for Claude.

The tool does NOT judge anything. It collects the money-model facts (interactive
or via arguments) and prints a markdown brief. The agent (Claude, with this skill
loaded) reads the brief and judges the model against MNY-1 to MNY-3, then
delivers a brutal "grill me" verdict with the fix order.

All figures are gross profit, never revenue. CAC must be fully loaded
(ad spend, sales cost, onboarding cost).

    python scripts/money_model.py
    python scripts/money_model.py --cac 120 --profit-30d 300 --ltgp 900 \\
        --humans 1 --context "SEO retainer for local SMEs"
"""
from __future__ import annotations

import argparse
import sys


def ask(prompt: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    raw = input(f"{prompt}{hint}: ").strip()
    return raw or default


def collect(args: argparse.Namespace) -> dict:
    if args.cac is not None:
        return {
            "cac": args.cac,
            "profit_30d": args.profit_30d or "not stated",
            "ltgp": args.ltgp or "not stated",
            "humans": args.humans if args.humans is not None else "not stated",
            "context": args.context or "not stated",
        }
    print("Money-model interview (gross profit figures, never revenue).\n")
    return {
        "cac": ask("Fully loaded CAC"),
        "profit_30d": ask("Gross profit collected per customer in the first 30 days"),
        "ltgp": ask("Lifetime gross profit per customer"),
        "humans": ask("Humans in the delivery loop (0-3)", "0"),
        "context": ask("What the business sells (one line)"),
    }


BRIEF = """# AGENT BRIEF: judge this money model (MNY-1 to MNY-3)

You are the judging agent. The script collected numbers; it judged nothing.
Judge from the numbers below only. Never invent numbers.

## The numbers (user-supplied)
- Fully loaded CAC: {cac}
- Gross profit per customer in the first 30 days: {profit_30d}
- Lifetime gross profit per customer (LTGP): {ltgp}
- Humans in the delivery loop: {humans}
- Context: {context}

## Your job
1. 30-Day Rule (MNY-2): compute 30-day profit / CAC.
   - Below 1: FAIL, paid acquisition burns cash.
   - 1 to 2: pass, but below the Client-Financed Acquisition target.
   - 2 and above: target met (MNY-1), one customer funds itself plus two more.
2. LTGP:CAC (MNY-3): the bar is 3:1 with no human in the loop, 6:1 with one,
   9:1 with two, 12:1 with three. Compute the ratio, judge against the bar.
3. GRILL ME. Brutal, specific, no flattery. Every hit names the violated law
   (MNY-1 to MNY-10 only, laws that exist in sources/hormozi-100m-money-models.md)
   and the concrete fix, in fix order: profitable attraction first (MNY-4), then
   upsell the next problem (MNY-5), downsell the terms never the price (MNY-6),
   continuity last (MNY-7), one offer at a time (MNY-8).
4. Verdict: the model can buy growth / fix the first 30 days first /
   fix lifetime value before scaling spend.

Rules: cite only laws that exist in the source files, with ID and level.
Ratios are the author's stated bars (level orange); present them as bars, not facts.
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect money-model numbers and print the agent judging brief (MNY-1..3).")
    parser.add_argument("--cac")
    parser.add_argument("--profit-30d")
    parser.add_argument("--ltgp")
    parser.add_argument("--humans")
    parser.add_argument("--context")
    args = parser.parse_args()

    facts = collect(args)
    print("\n" + BRIEF.format(**facts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
