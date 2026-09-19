# jevassert report — rag-passage-relevance v0.4.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.892**, ECE **0.039**
- bootstrap 95%: accuracy CI 0.870–0.914, ECE CI 0.029–0.065
- cost: $0.002618/case ($1.0472 total)
- latency: p50 1673ms, p95 2462ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 400 | 0 | 0.960 | 0.933 | 0.033 | 0.030 |
| quality | score | 400 | 0 | 0.825 | 0.781 | 0.098 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.990 | 0.896 |
| 0.60 | 0.890 | 0.928 |
| 0.70 | 0.805 | 0.955 |
| 0.80 | 0.728 | 0.964 |
| 0.90 | 0.594 | 0.983 |
| 0.95 | 0.522 | 0.988 |

## Author thresholds (pack threshold floors)

- auto-accepted 628/800 (0.785), precision 0.955
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
