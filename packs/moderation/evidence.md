# jevassert report — moderation v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 50 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.787**, ECE **0.095**
- cost: $0.000022/case ($0.0011 total)
- latency: p50 314ms, p95 786ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 50 | 0 | 0.700 | 0.810 | 0.184 | — |
| severity | score | 50 | 0 | 0.660 | 0.845 | 0.203 | — |
| targeted_group | noul | 50 | 0 | 1.000 | 0.956 | 0.044 | 0.007 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.953 | 0.804 |
| 0.60 | 0.887 | 0.850 |
| 0.70 | 0.833 | 0.872 |
| 0.80 | 0.773 | 0.888 |
| 0.90 | 0.647 | 0.928 |
| 0.95 | 0.493 | 0.919 |

## Author thresholds (pack threshold floors)

- auto-accepted 115/150 (0.767), precision 0.861
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
