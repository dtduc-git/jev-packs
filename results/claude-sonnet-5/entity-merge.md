# jevassert report — entity-merge v0.4.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 420 (0 errors, 0 missing answers)
- items: 840 — accuracy **0.861**, ECE **0.065**
- bootstrap 95%: accuracy CI 0.837–0.885, ECE CI 0.045–0.084
- cost: $0.003185/case ($1.3378 total)
- latency: p50 2312ms, p95 4020ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| same_entity | noul | 420 | 0 | 0.855 | 0.883 | 0.075 | 0.096 |
| action | choice | 420 | 0 | 0.867 | 0.782 | 0.134 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.987 | 0.867 |
| 0.60 | 0.895 | 0.888 |
| 0.70 | 0.801 | 0.926 |
| 0.80 | 0.721 | 0.934 |
| 0.90 | 0.506 | 0.958 |
| 0.95 | 0.289 | 0.942 |

## Author thresholds (pack threshold floors)

- auto-accepted 617/840 (0.735), precision 0.932
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
