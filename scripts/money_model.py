#!/usr/bin/env python3
"""Compute a money model against the $100M Money Models bars (MNY-1 to MNY-3).

Arithmetic and thresholds are exact, so the script computes them; the agent interprets the
result with the laws. All figures are GROSS PROFIT per customer, never revenue, and CAC is fully
loaded (ads, sales time, onboarding).

    python scripts/money_model.py --cac 120 --profit-30d 300 --ltgp 900 --humans 1
    python scripts/money_model.py --cac 120 --upfront 200 --monthly 75 --months 8 --margin 70 --humans 1

The second form derives gross profit: 30-day profit = (upfront + one month) x margin,
lifetime profit = (upfront + monthly x months) x margin.

The last output line is JSON. Bars are the author's (level 🟠): present them as bars, not facts.
"""
from __future__ import annotations

import argparse
import json
import sys

LTGP_BARS = {0: 3.0, 1: 6.0, 2: 9.0, 3: 12.0}


def evaluate(cac: float, profit_30d: float, ltgp: float, humans: int) -> dict:
    """The 30-day rule, Client-Financed Acquisition and the LTGP:CAC bar for this many humans."""
    if cac <= 0:
        raise ValueError("CAC must be above 0 (a channel with no acquisition cost has no ratio)")
    if profit_30d < 0 or ltgp < 0:
        raise ValueError("gross profit cannot be negative here")
    if ltgp < profit_30d:
        raise ValueError("lifetime gross profit cannot be lower than the 30-day gross profit")
    humans = max(0, min(int(humans), 3))

    ratio_30d = profit_30d / cac
    if ratio_30d < 1:
        rule = "fail"
        rule_text = "fails the 30-day rule: each paid customer burns cash before paying back (MNY-2)"
    elif ratio_30d < 2:
        rule = "pass"
        rule_text = "passes the 30-day rule, below the Client-Financed Acquisition target of 2x (MNY-1)"
    else:
        rule = "target"
        rule_text = "meets Client-Financed Acquisition: one customer funds itself and others (MNY-1)"

    bar = LTGP_BARS[humans]
    ltgp_ratio = ltgp / cac
    return {
        "cac": cac,
        "profit_30d": profit_30d,
        "ltgp": ltgp,
        "humans_in_delivery": humans,
        "ratio_30d": round(ratio_30d, 2),
        "thirty_day_rule": rule,
        "thirty_day_text": rule_text,
        "customers_funded_in_30d": max(0, int(ratio_30d) - 1),
        "ltgp_cac": round(ltgp_ratio, 2),
        "ltgp_bar": bar,
        "ltgp_pass": ltgp_ratio >= bar,
        "verdict": (
            "can buy growth" if rule != "fail" and ltgp_ratio >= bar
            else "fix the first 30 days first" if rule == "fail"
            else "fix lifetime value before scaling spend"
        ),
    }


def derive(upfront: float, monthly: float, months: float, margin_pct: float) -> tuple[float, float]:
    """Gross profit over 30 days and over the customer's life, from revenue and margin."""
    if not 0 < margin_pct <= 100:
        raise ValueError("margin must be a percentage between 0 and 100")
    margin = margin_pct / 100
    first_month = monthly if months >= 1 else monthly * months
    return (upfront + first_month) * margin, (upfront + monthly * months) * margin


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Money model against MNY-1 to MNY-3 (gross profit, never revenue).")
    parser.add_argument("--cac", type=float, required=True, help="fully loaded cost to acquire one customer")
    parser.add_argument("--profit-30d", type=float, help="gross profit per customer collected in the first 30 days")
    parser.add_argument("--ltgp", type=float, help="lifetime gross profit per customer")
    parser.add_argument("--upfront", type=float, default=0.0, help="revenue collected on day 1 (with --margin)")
    parser.add_argument("--monthly", type=float, default=0.0, help="recurring revenue per month (with --margin)")
    parser.add_argument("--months", type=float, default=0.0, help="average months a customer stays (with --margin)")
    parser.add_argument("--margin", type=float, help="gross margin in percent, to derive profit from revenue")
    parser.add_argument("--humans", type=int, default=0, help="humans in the delivery loop (0 to 3)")
    args = parser.parse_args()

    try:
        if args.profit_30d is not None and args.ltgp is not None:
            profit_30d, ltgp = args.profit_30d, args.ltgp
        elif args.margin is not None:
            profit_30d, ltgp = derive(args.upfront, args.monthly, args.months, args.margin)
        else:
            raise ValueError("give --profit-30d and --ltgp, or revenue figures with --margin")
        result = evaluate(args.cac, profit_30d, ltgp, args.humans)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"30-day gross profit / CAC = {result['ratio_30d']}: {result['thirty_day_text']}")
    print(f"LTGP:CAC = {result['ltgp_cac']}:1 against a bar of {result['ltgp_bar']:g}:1 "
          f"with {result['humans_in_delivery']} human(s) in delivery (MNY-3): "
          f"{'pass' if result['ltgp_pass'] else 'below the bar'}")
    print(f"Verdict on the model: {result['verdict']} (bars are the author's claims, not audited data)")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
