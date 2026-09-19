# jevassert report — moderation v0.8.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 450 (1 errors, 3 missing answers)
- items: 1347 — accuracy **0.923**, ECE **0.050**
- bootstrap 95%: accuracy CI 0.909–0.936, ECE CI 0.039–0.063
- cost: $0.005829/case ($2.6229 total)
- latency: p50 2207ms, p95 6278ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 449 | 1 | 0.915 | 0.870 | 0.048 | — |
| severity | score | 449 | 1 | 0.869 | 0.781 | 0.092 | — |
| targeted_group | noul | 449 | 1 | 0.984 | 0.967 | 0.017 | 0.013 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.976 | 0.930 |
| 0.60 | 0.912 | 0.952 |
| 0.70 | 0.859 | 0.963 |
| 0.80 | 0.775 | 0.974 |
| 0.90 | 0.664 | 0.989 |
| 0.95 | 0.536 | 0.992 |

## Author thresholds (pack threshold floors)

- auto-accepted 1076/1347 (0.799), precision 0.967
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
