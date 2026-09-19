# jevassert report — rag-passage-relevance v0.3.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 200 (0 errors, 0 missing answers)
- items: 400 — accuracy **0.895**, ECE **0.044**
- bootstrap 95%: accuracy CI 0.863–0.925, ECE CI 0.024–0.072
- cost: $0.000018/case ($0.0035 total)
- latency: p50 309ms, p95 377ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 200 | 0 | 0.965 | 0.955 | 0.016 | 0.028 |
| quality | score | 200 | 0 | 0.825 | 0.906 | 0.081 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.895 |
| 0.60 | 0.973 | 0.902 |
| 0.70 | 0.912 | 0.932 |
| 0.80 | 0.875 | 0.940 |
| 0.90 | 0.815 | 0.951 |
| 0.95 | 0.723 | 0.972 |

## Author thresholds (pack threshold floors)

- auto-accepted 348/400 (0.870), precision 0.931
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
