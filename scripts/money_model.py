#!/usr/bin/env python3
"""Check a money model against Hormozi's $100M Money Models thresholds (MNY-1..3).

    python scripts/money_model.py
    python scripts/money_model.py --cac 120 --profit-30d 300 --ltgp 900 --humans 1

Inputs are gross profit (never revenue). CAC must be fully loaded
(ad spend, sales cost, onboarding cost).

Verdicts:
  - 30-Day Rule (MNY-2): 30-day gross profit per customer >= CAC to run paid
    acquisition at all; >= 2x CAC is the Client-Financed Acquisition target (MNY-1).
  - LTGP:CAC (MNY-3): 3:1 with no human in the loop, 6:1 with one, 9:1 with two,
    12:1 with three. Below the bar, the model cannot buy growth profitably.
"""
from __future__ import annotations

import argparse
import sys

RATIOS = {0: 3.0, 1: 6.0, 2: 9.0, 3: 12.0}


def ask(prompt: str, default: float) -> float:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"Not a number, using {default}.")
        return default


def verdict_30d(profit_30d: float, cac: float) -> tuple[str, str]:
    if cac <= 0:
        return "n/a", "CAC must be above zero to judge the model."
    ratio = profit_30d / cac
    if ratio >= 2.0:
        return (f"PASS ({ratio:.1f}x CAC)",
                "Client-Financed Acquisition: one customer funds itself plus two more (MNY-1). Scale ad spend.")
    if ratio >= 1.0:
        return (f"WEAK ({ratio:.1f}x CAC)",
                "30-Day Rule met but below the 2x target (MNY-2). Fix: raise the entry price, "
                "add a day-one upsell (MNY-5), or cut CAC before scaling.")
    return (f"FAIL ({ratio:.1f}x CAC)",
            "30-Day Rule broken (MNY-2): acquisition burns cash. Do not scale paid ads. "
            "Fix first: a profitable attraction offer (MNY-4) or a cheaper channel.")


def verdict_ratio(ltgp: float, cac: float, humans: int) -> tuple[str, str]:
    if cac <= 0:
        return "n/a", "CAC must be above zero to judge the model."
    bar = RATIOS.get(min(humans, 3), 12.0)
    ratio = ltgp / cac
    if ratio >= bar:
        return (f"PASS ({ratio:.1f}:1 vs {bar:.0f}:1 bar)",
                "Healthy: the model can outbid competitors on acquisition (MNY-3).")
    return (f"FAIL ({ratio:.1f}:1 vs {bar:.0f}:1 bar)",
            "Below the LTGP:CAC bar (MNY-3). Fix: raise lifetime value with upsells and "
            "continuity (MNY-5, MNY-7), or cut CAC. Never scale on revenue alone.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a money model (MNY-1..3).")
    parser.add_argument("--cac", type=float, help="fully loaded CAC")
    parser.add_argument("--profit-30d", type=float,
                        help="gross profit collected per customer in the first 30 days")
    parser.add_argument("--ltgp", type=float, help="lifetime gross profit per customer")
    parser.add_argument("--humans", type=int, choices=[0, 1, 2, 3],
                        help="humans in the delivery loop")
    args = parser.parse_args()

    if all(v is not None for v in (args.cac, args.profit_30d, args.ltgp, args.humans)):
        cac, profit_30d, ltgp, humans = args.cac, args.profit_30d, args.ltgp, args.humans
    else:
        print("Money model check (gross profit figures, never revenue).")
        cac = ask("Fully loaded CAC", 100)
        profit_30d = ask("Gross profit collected per customer in the first 30 days", 100)
        ltgp = ask("Lifetime gross profit per customer", 400)
        humans = int(ask("Humans in the delivery loop (0-3)", 0))

    label_30d, advice_30d = verdict_30d(profit_30d, cac)
    label_ratio, advice_ratio = verdict_ratio(ltgp, cac, humans)

    print(f"\n  30-Day Rule (MNY-2): {label_30d}")
    print(f"    {advice_30d}")
    print(f"  LTGP:CAC (MNY-3):   {label_ratio}")
    print(f"    {advice_ratio}")

    ok_30d = label_30d.startswith("PASS")
    ok_ratio = label_ratio.startswith("PASS")
    if ok_30d and ok_ratio:
        print("\n  Overall: the model can buy growth. Next: perfect one offer at a time (MNY-8).")
    elif not ok_30d:
        print("\n  Overall: fix the first 30 days before anything else (MNY-4, MNY-5).")
    else:
        print("\n  Overall: fix lifetime value before scaling spend (MNY-5, MNY-6, MNY-7).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
