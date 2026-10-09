#!/usr/bin/env python3
"""Interview the user about an offer, then print an AGENT BRIEF for Claude to score.

The tool does NOT score anything. It collects the offer facts (interactive or
via arguments) and prints a markdown brief. The agent (Claude, with this skill
loaded) reads the brief and does the scoring: it rates each Value Equation
driver, computes the score, names the weakest driver, and delivers a brutal
"grill me" critique with fixes citing HOR-2 to HOR-10.

    python scripts/value_equation.py
    python scripts/value_equation.py --name "SEO retainer" --price 750 \\
        --dream "10 qualified calls a month" --proof "3 client cases" \\
        --delay-days 45 --effort "they approve content" --delivery dfy
"""
from __future__ import annotations

import argparse
import sys


def ask(prompt: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    raw = input(f"{prompt}{hint}: ").strip()
    return raw or default


def yn(prompt: str) -> str:
    raw = input(f"{prompt} (y/n) [n]: ").strip().lower()
    return "yes" if raw in ("y", "yes") else "no"


def collect(args: argparse.Namespace) -> dict:
    if args.name is not None:
        return {
            "name": args.name,
            "price": args.price or "not stated",
            "dream": args.dream or "not stated",
            "proof": args.proof or "not stated",
            "delay_days": args.delay_days or "not stated",
            "effort": args.effort or "not stated",
            "guarantee": args.guarantee or "none stated",
            "bonuses": args.bonuses or "none stated",
            "delivery": args.delivery or "not stated",
        }
    print("Offer interview (the agent will score; just give the facts).\n")
    facts = {
        "name": ask("Offer name"),
        "price": ask("Price"),
        "dream": ask("Dream outcome, in the buyer's words"),
        "proof": ask("Proof elements (cases, testimonials, numbers)"),
        "delay_days": ask("Days until the buyer sees the first result", "30"),
        "effort": ask("What the buyer must do / sacrifice to get the result"),
    }
    has_guarantee = yn("Is there a guarantee")
    facts["guarantee"] = ask("  Guarantee wording") if has_guarantee == "yes" else "none stated"
    has_bonuses = yn("Are there bonuses")
    facts["bonuses"] = ask("  Bonuses (each with its value)") if has_bonuses == "yes" else "none stated"
    facts["delivery"] = ask("Delivery: diy, dfy, or mixed", "not stated")
    return facts


BRIEF = """# AGENT BRIEF: score this offer on the Value Equation (HOR-2)

You are the scoring agent. The script collected facts; it scored nothing.
Score from the facts below only. Never invent facts, numbers, or proof.

## The offer (user-supplied facts)
- Name: {name}
- Price: {price}
- Dream outcome (buyer's words): {dream}
- Proof / likelihood elements: {proof}
- Time to first result: {delay_days} days
- Buyer effort / sacrifice: {effort}
- Guarantee: {guarantee}
- Bonuses: {bonuses}
- Delivery: {delivery}

## Your job
1. Score each driver 1-10 with one line of justification grounded ONLY in the facts above:
   - Dream outcome (higher better; HOR-3, HOR-7: timing, emotional payoff, status)
   - Perceived likelihood (higher better; HOR-5: proof, guarantee strength)
   - Time delay (lower better; convert the days above to a 1-10 friction score, HOR-2)
   - Effort and sacrifice (lower better; HOR-2)
2. Compute Value = (dream x likelihood) / (delay x effort). The number is relative,
   not a price. Name the weakest driver.
3. GRILL ME. Brutal, specific, no flattery. Every hit names the violated law
   (HOR-2 to HOR-10 only, laws that exist in sources/hormozi-100m-offers.md) and the
   concrete fix. Missing facts are grill material too: "none stated" means the offer
   has no guarantee, no proof, or no bonuses, say so.
4. Verdict: weak / solid / Grand Slam en devenir, plus the ONE next action.

Rules: cite only laws that exist in the source files, with ID and level.
A missing fact never becomes an assumed strength.
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect an offer and print the agent scoring brief (HOR-2).")
    parser.add_argument("--name")
    parser.add_argument("--price")
    parser.add_argument("--dream")
    parser.add_argument("--proof")
    parser.add_argument("--delay-days")
    parser.add_argument("--effort")
    parser.add_argument("--guarantee")
    parser.add_argument("--bonuses")
    parser.add_argument("--delivery")
    args = parser.parse_args()

    facts = collect(args)
    print("\n" + BRIEF.format(**facts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
