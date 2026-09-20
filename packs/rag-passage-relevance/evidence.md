# jevassert report — rag-passage-relevance v0.5.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.921**, ECE **0.021**
- bootstrap 95%: accuracy CI 0.902–0.940, ECE CI 0.016–0.042
- cost: $0.000020/case ($0.0081 total)
- latency: p50 322ms, p95 435ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 400 | 0 | 0.970 | 0.957 | 0.015 | 0.024 |
| quality | score | 400 | 0 | 0.873 | 0.898 | 0.036 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.994 | 0.923 |
| 0.60 | 0.955 | 0.935 |
| 0.70 | 0.914 | 0.949 |
| 0.80 | 0.869 | 0.957 |
| 0.90 | 0.805 | 0.967 |
| 0.95 | 0.730 | 0.973 |

## Author thresholds (pack threshold floors)

- auto-accepted 692/800 (0.865), precision 0.949
- labels without a floor (usually `unknown`) always route to review

## Gates

- **PASS** `min_accuracy` — accuracy 0.921 >= 0.890
- **PASS** `max_ece` — ece 0.021 <= 0.050
- **PASS** `max_cost_per_case_usd` — cost/case $0.000020 <= $0.000040
- **PASS** `max_p95_latency_ms` — p95 435ms <= 652ms
