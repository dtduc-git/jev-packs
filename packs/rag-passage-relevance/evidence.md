# jevassert report — rag-passage-relevance v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 50 (0 errors, 0 missing answers)
- items: 100 — accuracy **0.880**, ECE **0.058**
- cost: $0.000018/case ($0.0009 total)
- latency: p50 319ms, p95 793ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 50 | 0 | 0.960 | 0.951 | 0.043 | 0.035 |
| quality | score | 50 | 0 | 0.800 | 0.901 | 0.109 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.880 |
| 0.60 | 0.990 | 0.879 |
| 0.70 | 0.900 | 0.922 |
| 0.80 | 0.860 | 0.930 |
| 0.90 | 0.830 | 0.940 |
| 0.95 | 0.690 | 0.957 |

## Author thresholds (pack threshold floors)

- auto-accepted 89/100 (0.890), precision 0.921
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
