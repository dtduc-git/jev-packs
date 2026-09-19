# jevassert report — moderation v0.6.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 450 (1 errors, 3 missing answers)
- items: 1347 — accuracy **0.899**, ECE **0.033**
- bootstrap 95%: accuracy CI 0.883–0.915, ECE CI 0.023–0.052
- cost: $0.004594/case ($2.0673 total)
- latency: p50 2117ms, p95 4861ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 449 | 1 | 0.900 | 0.870 | 0.062 | — |
| severity | score | 449 | 1 | 0.808 | 0.798 | 0.055 | — |
| targeted_group | noul | 449 | 1 | 0.989 | 0.958 | 0.031 | 0.013 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.974 | 0.909 |
| 0.60 | 0.921 | 0.928 |
| 0.70 | 0.874 | 0.935 |
| 0.80 | 0.777 | 0.953 |
| 0.90 | 0.664 | 0.978 |
| 0.95 | 0.549 | 0.986 |

## Author thresholds (pack threshold floors)

- auto-accepted 1090/1347 (0.809), precision 0.938
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
