# power-check

This tool tells you how long an A/B test would take at your traffic, before you build the test. It uses only the Python standard library (Python 3.8 or later).

```bash
# Per-visitor click rate: 1% base, detect a doubling, 400 eligible visitors a day
python3 power_check.py clicks --base 0.01 --lift 2 --daily 400
# visitors per arm: 2,319
# days at 400 visitors/day (50% in treatment): 12

# Rare outcomes (signups plus booked meetings): detect 2x at 2 events a day
python3 power_check.py events --ratio 2 --per-day 2
# events needed (both arms): 69
# days at 2 events/day: 35
```

The default is a two-sided alpha of 0.05 and 80% power. Change them with `--alpha` and `--power`, and put those flags before the mode (`python3 power_check.py --power 0.9 events ...`). `--split` goes after the mode and sets the share of traffic in the treatment arm. For a holdout, `--split 0.8` puts 80% in treatment and 20% in the holdout. An uneven split always needs more total traffic than 50/50.

## Which mode to use

- `clicks`: a per-visitor rate, such as the CTA click rate. This is a two-proportion test. Clicks are fast to measure, but they move easily and often only shift between buttons.
- `events`: outcomes too rare to express as a per-visitor rate, such as completed signups and booked meetings. Given the total number of events, each event falls in the treatment arm with a known probability. The tool uses a normal approximation to a one-sample binomial test on that share. At very small event counts the exact power is a little lower, so treat the answer as a floor.

## Reading the answer

If the answer is longer than your campaign will run, the test cannot settle the question. That is still useful to know. Decide on design reasons, count outcomes each month, and agree on a removal rule before the numbers come in. Also check that your largest traffic source can reach the test at all. Ad and QR traffic that lands on the destination page never gets an arm.
