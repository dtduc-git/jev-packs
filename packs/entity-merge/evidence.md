# jevassert report — entity-merge v0.4.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 420 (0 errors, 0 missing answers)
- items: 840 — accuracy **0.857**, ECE **0.017**
- bootstrap 95%: accuracy CI 0.832–0.880, ECE CI 0.021–0.054
- cost: $0.000018/case ($0.0075 total)
- latency: p50 308ms, p95 385ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| same_entity | noul | 420 | 0 | 0.876 | 0.832 | 0.048 | 0.097 |
| action | choice | 420 | 0 | 0.838 | 0.855 | 0.044 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.989 | 0.857 |
| 0.60 | 0.917 | 0.875 |
| 0.70 | 0.813 | 0.909 |
| 0.80 | 0.708 | 0.924 |
| 0.90 | 0.477 | 0.955 |
| 0.95 | 0.311 | 0.981 |

## Author thresholds (pack threshold floors)

- auto-accepted 562/840 (0.669), precision 0.918
- labels without a floor (usually `unknown`) always route to review

## Gates

- **PASS** `min_accuracy` — accuracy 0.857 >= 0.820
- **PASS** `max_ece` — ece 0.017 <= 0.050
- **PASS** `max_cost_per_case_usd` — cost/case $0.000018 <= $0.000036
- **PASS** `max_p95_latency_ms` — p95 385ms <= 578ms
