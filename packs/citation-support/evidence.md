# jevassert report — citation-support v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 50 (0 errors, 0 missing answers)
- items: 100 — accuracy **0.910**, ECE **0.054**
- cost: $0.000017/case ($0.0009 total)
- latency: p50 319ms, p95 776ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 50 | 0 | 0.980 | 0.934 | 0.046 | 0.014 |
| coverage | score | 50 | 0 | 0.840 | 0.929 | 0.124 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.990 | 0.919 |
| 0.60 | 0.970 | 0.928 |
| 0.70 | 0.950 | 0.947 |
| 0.80 | 0.920 | 0.957 |
| 0.90 | 0.800 | 0.950 |
| 0.95 | 0.630 | 0.968 |

## Author thresholds (pack threshold floors)

- auto-accepted 91/100 (0.910), precision 0.945
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
