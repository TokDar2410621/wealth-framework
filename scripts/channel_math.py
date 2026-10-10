#!/usr/bin/env python3
"""Cold-channel arithmetic (FLE-3, FLE-7): is a silence a verdict, or just a small number?

    python scripts/channel_math.py --sends 40 --reply-rate 0.03
    python scripts/channel_math.py --sends 40 --reply-rate 3% --positive-rate 30% --close-rate 20%

Give rates from a benchmark you can name, or from your own past sends. The script assumes each
send replies independently with the same probability; real campaigns vary, so read the output
as an order of magnitude.

The last output line is JSON.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

INFORMATIVE_THRESHOLD = 0.10  # FLE-3: if P(0) is above 10%, a zero cannot be a verdict


def rate(text: str) -> float:
    """Accept 0.03, 3% or 3 (read as percent when above 1)."""
    value = float(text.strip().rstrip("%"))
    if text.strip().endswith("%") or value > 1:
        value /= 100
    if not 0 < value < 1:
        raise argparse.ArgumentTypeError("a rate must be between 0 and 100%")
    return value


def sends_for(p: float, confidence: float = 1 - INFORMATIVE_THRESHOLD) -> int:
    """Sends needed so that at least one success has this probability."""
    return math.ceil(math.log(1 - confidence) / math.log(1 - p))


def compute(sends: int, reply_rate: float, positive_rate: float | None = None, close_rate: float | None = None) -> dict:
    if sends < 1:
        raise ValueError("sends must be at least 1")
    p_zero = (1 - reply_rate) ** sends
    result = {
        "sends": sends,
        "reply_rate": reply_rate,
        "expected_replies": round(sends * reply_rate, 2),
        "p_zero_replies": round(p_zero, 4),
        "zero_is_informative": p_zero <= INFORMATIVE_THRESHOLD,
        "sends_for_informative_zero": sends_for(reply_rate),
    }
    if positive_rate is not None and close_rate is not None:
        deal_rate = reply_rate * positive_rate * close_rate
        result.update({
            "deal_rate_per_send": round(deal_rate, 6),
            "expected_deals": round(sends * deal_rate, 3),
            "p_zero_deals": round((1 - deal_rate) ** sends, 4),
            "sends_for_one_deal_90pct": sends_for(deal_rate),
        })
    return result


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Expected replies and deals, and whether a zero means anything (FLE-3).")
    parser.add_argument("--sends", type=int, required=True, help="messages actually sent (not drafted)")
    parser.add_argument("--reply-rate", type=rate, required=True, help="reply rate per send, e.g. 3%% or 0.03")
    parser.add_argument("--positive-rate", type=rate, help="share of replies that are interested")
    parser.add_argument("--close-rate", type=rate, help="share of interested replies that buy")
    args = parser.parse_args()
    try:
        r = compute(args.sends, args.reply_rate, args.positive_rate, args.close_rate)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"{r['sends']} sends at {r['reply_rate']:.1%}: about {r['expected_replies']} replies expected; "
          f"P(0 replies) = {r['p_zero_replies']:.0%}.")
    if r["zero_is_informative"]:
        print("A zero here IS informative (P(0) <= 10%): the assumed rate is likely wrong for this offer or segment.")
    else:
        print(f"A zero here is NOT a verdict (P(0) > 10%). For an informative zero, send about "
              f"{r['sends_for_informative_zero']} (FLE-3). Before rewriting the copy, check the sends really left (FLE-7).")
    if "expected_deals" in r:
        print(f"Expected deals: {r['expected_deals']}; P(0 deals) = {r['p_zero_deals']:.0%}; "
              f"about {r['sends_for_one_deal_90pct']} sends for a 90% chance of one deal.")
    print(json.dumps(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
