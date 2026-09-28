#!/usr/bin/env python3
"""How long would an A/B test take at your traffic? Standard library only.

Two questions:

  clicks  Per-visitor rate test (two proportions). Visitors needed per arm to
          detect a change from a base rate, and days at your daily traffic.
  events  Rare-outcome test (signups, booked meetings). Total events needed to
          detect a rate ratio between arms, and days at your daily event count.
          Conditional on the total, each event lands in the treatment arm with a
          fixed probability, so this is a normal approximation to a one-sample
          binomial test on that share.

Examples:
  python3 power_check.py clicks --base 0.01 --lift 2 --daily 400
  python3 power_check.py clicks --base 0.004 --lift 0.5 --daily 400
  python3 power_check.py --power 0.9 events --ratio 2 --per-day 2

Put --alpha and --power before the mode.
"""
from __future__ import annotations

import argparse
import math
from statistics import NormalDist


def z(alpha: float, power: float) -> tuple[float, float]:
    return NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)


def visitors_per_arm(base: float, lift: float, split: float, alpha: float, power: float) -> tuple[int, int]:
    """(control, treatment) sample sizes. Fleiss's formula with allocation ratio k = treatment/control."""
    p1, p2 = base, base * lift
    if not (0 < p1 < 1 and 0 < p2 < 1) or p1 == p2:
        raise SystemExit('rates must be between 0 and 1 and differ')
    if not 0 < split < 1:
        raise SystemExit('--split must be between 0 and 1')
    k = split / (1 - split)
    za, zb = z(alpha, power)
    pbar = (p1 + k * p2) / (1 + k)
    num = za * math.sqrt(pbar * (1 - pbar) * (1 + 1 / k)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2) / k)
    n_control = math.ceil((num / (p2 - p1)) ** 2)
    return n_control, math.ceil(k * n_control)


def events_total(ratio: float, split: float, alpha: float, power: float) -> int:
    p0 = split
    p1 = ratio * split / (ratio * split + (1 - split))
    za, zb = z(alpha, power)
    num = za * math.sqrt(p0 * (1 - p0)) + zb * math.sqrt(p1 * (1 - p1))
    return math.ceil((num / (p1 - p0)) ** 2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--alpha', type=float, default=0.05)
    ap.add_argument('--power', type=float, default=0.8)
    sub = ap.add_subparsers(dest='mode', required=True)

    c = sub.add_parser('clicks', help='per-visitor rate test')
    c.add_argument('--base', type=float, required=True, help='control rate, e.g. 0.01 for 1%%')
    c.add_argument('--lift', type=float, required=True, help='treatment/control, e.g. 2 for 2x, 0.5 for a halving')
    c.add_argument('--daily', type=float, required=True, help='eligible visitors per day, both arms together')
    c.add_argument('--split', type=float, default=0.5, help='share of traffic in the treatment arm')

    e = sub.add_parser('events', help='rare-outcome test on event counts')
    e.add_argument('--ratio', type=float, required=True, help='treatment rate / control rate, e.g. 2')
    e.add_argument('--per-day', type=float, required=True, help='outcome events per day, both arms together')
    e.add_argument('--split', type=float, default=0.5, help='share of traffic in the treatment arm')

    a = ap.parse_args()
    if a.mode == 'clicks':
        n_c, n_t = visitors_per_arm(a.base, a.lift, a.split, a.alpha, a.power)
        if n_c == n_t:
            print(f'visitors per arm: {n_c:,}')
        else:
            print(f'visitors: control {n_c:,}, treatment {n_t:,}')
        print(f'days at {a.daily:g} visitors/day ({a.split:.0%} in treatment): {math.ceil((n_c + n_t) / a.daily):,}')
    else:
        n = events_total(a.ratio, a.split, a.alpha, a.power)
        print(f'events needed (both arms): {n:,}')
        print(f'days at {a.per_day:g} events/day: {math.ceil(n / a.per_day):,}')


if __name__ == '__main__':
    main()
