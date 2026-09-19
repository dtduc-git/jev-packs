# jevassert report — moderation v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 100 (0 errors, 0 missing answers)
- items: 300 — accuracy **0.793**, ECE **0.088**
- bootstrap 95%: accuracy CI 0.747–0.837, ECE CI 0.053–0.126
- cost: $0.000022/case ($0.0022 total)
- latency: p50 322ms, p95 767ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 100 | 0 | 0.710 | 0.794 | 0.098 | — |
| severity | score | 100 | 0 | 0.670 | 0.843 | 0.178 | — |
| targeted_group | noul | 100 | 0 | 1.000 | 0.961 | 0.039 | 0.005 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.933 | 0.818 |
| 0.60 | 0.873 | 0.855 |
| 0.70 | 0.820 | 0.878 |
| 0.80 | 0.760 | 0.904 |
| 0.90 | 0.653 | 0.934 |
| 0.95 | 0.553 | 0.958 |

## Author thresholds (pack threshold floors)

- auto-accepted 233/300 (0.777), precision 0.880
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
