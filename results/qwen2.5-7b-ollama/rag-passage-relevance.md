# jevassert report — rag-passage-relevance v0.5.0

- model: `qwen2.5:7b` (pack pinned to `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.557**, ECE **0.319**
- bootstrap 95%: accuracy CI 0.525–0.593, ECE CI 0.288–0.348
- cost: $0.000000/case ($0.0000 total)
- latency: p50 13300ms, p95 15137ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 400 | 0 | 0.915 | 0.955 | 0.040 | 0.060 |
| quality | score | 400 | 0 | 0.200 | 0.798 | 0.598 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.954 | 0.571 |
| 0.60 | 0.884 | 0.604 |
| 0.70 | 0.834 | 0.636 |
| 0.80 | 0.765 | 0.680 |
| 0.90 | 0.657 | 0.751 |
| 0.95 | 0.616 | 0.775 |

## Author thresholds (pack threshold floors)

- auto-accepted 630/800 (0.787), precision 0.637
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
