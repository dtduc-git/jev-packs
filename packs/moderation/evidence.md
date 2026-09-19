# jevassert report — moderation v0.4.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 1200 — accuracy **0.791**, ECE **0.087**
- bootstrap 95%: accuracy CI 0.767–0.814, ECE CI 0.067–0.106
- cost: $0.000022/case ($0.0089 total)
- latency: p50 322ms, p95 411ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 400 | 0 | 0.675 | 0.779 | 0.126 | — |
| severity | score | 400 | 0 | 0.703 | 0.878 | 0.175 | — |
| targeted_group | noul | 400 | 0 | 0.995 | 0.964 | 0.031 | 0.005 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.943 | 0.825 |
| 0.60 | 0.873 | 0.864 |
| 0.70 | 0.828 | 0.882 |
| 0.80 | 0.767 | 0.900 |
| 0.90 | 0.695 | 0.927 |
| 0.95 | 0.590 | 0.932 |

## Author thresholds (pack threshold floors)

- auto-accepted 933/1200 (0.777), precision 0.887
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
