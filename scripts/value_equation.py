#!/usr/bin/env python3
"""Score an offer on Hormozi's Value Equation (HOR-2) and name the weakest driver.

    Value = (dream outcome x perceived likelihood of achievement)
            / (time delay x effort and sacrifice)

The equation is a mental model, not a calibrated formula: the score only ranks
offers and drivers against each other. Use it to decide which lever to pull
before building more.

    python scripts/value_equation.py
    python scripts/value_equation.py --dream 8 --likelihood 4 --delay-days 30 --effort 7
    python scripts/value_equation.py --compare offers.json

Scores are 1-10 except delay, given in days. The delay is normalized to a 1-10
scale (1 day = 1, 365+ days = 10) so the four terms stay comparable.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def normalize_delay(days: float) -> float:
    """Map a delay in days to a 1-10 friction score (log scale)."""
    if days <= 0:
        return 1.0
    return min(10.0, max(1.0, 1.0 + 9.0 * math.log10(1 + days) / math.log10(366)))


def ask(prompt: str, default: float) -> float:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"Not a number, using {default}.")
        return default


def read_offer(name: str) -> dict:
    print(f"\n--- {name} ---")
    dream = ask("Dream outcome, 1-10 (how big is the result in the buyer's words)", 5)
    likelihood = ask("Perceived likelihood of achievement, 1-10 (proof, guarantees)", 5)
    delay_days = ask("Time delay to the first result, in days", 30)
    effort = ask("Effort and sacrifice for the buyer, 1-10", 5)
    return {
        "name": name,
        "dream": dream,
        "likelihood": likelihood,
        "delay_days": delay_days,
        "delay": normalize_delay(delay_days),
        "effort": effort,
    }


def score(offer: dict) -> float:
    top = max(offer["dream"], 0.1) * max(offer["likelihood"], 0.1)
    bottom = max(offer["delay"], 0.1) * max(offer["effort"], 0.1)
    return top / bottom


FIXES = {
    "dream": (
        "Raise the dream outcome (HOR-3, HOR-7): define it with timing and emotional "
        "payoff, in the buyer's words, and frame it through status (how peers will see them)."
    ),
    "likelihood": (
        "Raise perceived likelihood (HOR-5): add proof (cases, before/after), and a guarantee "
        "that reverses risk (conditional, or keep working free until an observable improvement)."
    ),
    "delay": (
        "Crush time delay (HOR-2): deliver a first win fast, front-load results, add a bonus "
        "that accelerates the outcome (HOR-9)."
    ),
    "effort": (
        "Crush effort and sacrifice (HOR-2): move from do-it-yourself to done-for-you, "
        "checklists, templates, or onboarding that removes setup work."
    ),
}


def drivers(offer: dict) -> list[tuple[str, float, bool]]:
    """(name, score, higher_is_better)."""
    return [
        ("dream outcome", offer["dream"], True),
        ("perceived likelihood", offer["likelihood"], True),
        ("time delay", offer["delay"], False),
        ("effort and sacrifice", offer["effort"], False),
    ]


def weakest(offer: dict) -> str:
    ranked = []
    for name, value, higher_is_better in drivers(offer):
        badness = (10 - value) if higher_is_better else value
        ranked.append((badness, name))
    ranked.sort(reverse=True)
    return ranked[0][1]


def report(offer: dict) -> None:
    value = score(offer)
    print(f"\n=== {offer['name']} ===")
    for name, val, higher in drivers(offer):
        arrow = "(higher better)" if higher else "(lower better)"
        print(f"  {name:22s} {val:5.1f}/10 {arrow}")
    print(f"  time delay input: {offer['delay_days']} days")
    print(f"\n  Value score: {value:.2f}  (relative only, not a price)")
    weak = weakest(offer)
    key = {"dream outcome": "dream", "perceived likelihood": "likelihood",
           "time delay": "delay", "effort and sacrifice": "effort"}[weak]
    print(f"  Weakest driver: {weak}")
    print(f"  Fix first: {FIXES[key]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score offers on the Value Equation (HOR-2).")
    parser.add_argument("--dream", type=float, help="dream outcome, 1-10")
    parser.add_argument("--likelihood", type=float, help="perceived likelihood, 1-10")
    parser.add_argument("--delay-days", type=float, help="time to first result, in days")
    parser.add_argument("--effort", type=float, help="buyer effort and sacrifice, 1-10")
    parser.add_argument("--compare", metavar="FILE",
                        help="JSON file with a list of offers to rank")
    args = parser.parse_args()

    if args.compare:
        try:
            offers = json.load(open(args.compare, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"Cannot read {args.compare}: {exc}")
            return 1
        for raw in offers:
            offer = {
                "name": raw.get("name", "offer"),
                "dream": float(raw["dream"]),
                "likelihood": float(raw["likelihood"]),
                "delay_days": float(raw.get("delay_days", 30)),
                "delay": normalize_delay(float(raw.get("delay_days", 30))),
                "effort": float(raw["effort"]),
            }
            report(offer)
        ranked = sorted(offers, key=lambda r: score({
            "dream": float(r["dream"]), "likelihood": float(r["likelihood"]),
            "delay": normalize_delay(float(r.get("delay_days", 30))),
            "effort": float(r["effort"])}), reverse=True)
        print("\nRanking: " + " > ".join(r.get("name", "offer") for r in ranked))
        return 0

    if all(v is not None for v in (args.dream, args.likelihood, args.delay_days, args.effort)):
        offer = {
            "name": "offer",
            "dream": args.dream,
            "likelihood": args.likelihood,
            "delay_days": args.delay_days,
            "delay": normalize_delay(args.delay_days),
            "effort": args.effort,
        }
    else:
        offer = read_offer("Your offer")
    report(offer)
    return 0


if __name__ == "__main__":
    sys.exit(main())
