# jevassert report — moderation v0.7.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 450 (1 errors, 3 missing answers)
- items: 1347 — accuracy **0.908**, ECE **0.043**
- bootstrap 95%: accuracy CI 0.892–0.923, ECE CI 0.032–0.057
- cost: $0.005264/case ($2.3686 total)
- latency: p50 2177ms, p95 6111ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 449 | 1 | 0.922 | 0.865 | 0.067 | — |
| severity | score | 449 | 1 | 0.815 | 0.766 | 0.081 | — |
| targeted_group | noul | 449 | 1 | 0.987 | 0.965 | 0.022 | 0.014 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.976 | 0.916 |
| 0.60 | 0.901 | 0.942 |
| 0.70 | 0.831 | 0.963 |
| 0.80 | 0.751 | 0.974 |
| 0.90 | 0.649 | 0.989 |
| 0.95 | 0.533 | 0.993 |

## Author thresholds (pack threshold floors)

- auto-accepted 1035/1347 (0.768), precision 0.961
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
