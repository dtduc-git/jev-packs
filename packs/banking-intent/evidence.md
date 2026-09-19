# jevassert report — banking-intent v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.853**, ECE **0.077**
- bootstrap 95%: accuracy CI 0.800–0.907, ECE CI 0.044–0.136
- cost: $0.000028/case ($0.0042 total)
- latency: p50 316ms, p95 778ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| intent | choice | 150 | 0 | 0.853 | 0.931 | 0.077 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.987 | 0.865 |
| 0.60 | 0.933 | 0.879 |
| 0.70 | 0.887 | 0.887 |
| 0.80 | 0.853 | 0.891 |
| 0.90 | 0.800 | 0.925 |
| 0.95 | 0.767 | 0.948 |

## Author thresholds (pack threshold floors)

- auto-accepted 128/150 (0.853), precision 0.922
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
