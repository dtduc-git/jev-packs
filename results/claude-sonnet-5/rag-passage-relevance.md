# jevassert report — rag-passage-relevance v0.5.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.899**, ECE **0.049**
- bootstrap 95%: accuracy CI 0.876–0.919, ECE CI 0.037–0.074
- cost: $0.002830/case ($1.1319 total)
- latency: p50 1698ms, p95 2561ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 400 | 0 | 0.968 | 0.913 | 0.055 | 0.030 |
| quality | score | 400 | 0 | 0.830 | 0.796 | 0.101 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.990 | 0.904 |
| 0.60 | 0.885 | 0.935 |
| 0.70 | 0.823 | 0.948 |
| 0.80 | 0.736 | 0.952 |
| 0.90 | 0.571 | 0.976 |
| 0.95 | 0.496 | 0.987 |

## Author thresholds (pack threshold floors)

- auto-accepted 636/800 (0.795), precision 0.950
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
