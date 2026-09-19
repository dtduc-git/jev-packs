# jevassert report — rag-passage-relevance v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 100 (0 errors, 0 missing answers)
- items: 200 — accuracy **0.860**, ECE **0.071**
- bootstrap 95%: accuracy CI 0.810–0.905, ECE CI 0.037–0.111
- cost: $0.000018/case ($0.0018 total)
- latency: p50 330ms, p95 799ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 100 | 0 | 0.930 | 0.943 | 0.032 | 0.048 |
| quality | score | 100 | 0 | 0.790 | 0.895 | 0.106 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.860 |
| 0.60 | 0.960 | 0.880 |
| 0.70 | 0.890 | 0.904 |
| 0.80 | 0.860 | 0.919 |
| 0.90 | 0.790 | 0.930 |
| 0.95 | 0.665 | 0.977 |

## Author thresholds (pack threshold floors)

- auto-accepted 173/200 (0.865), precision 0.908
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
