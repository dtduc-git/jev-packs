# jevassert report — support-triage v0.4.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 1200 — accuracy **0.797**, ECE **0.095**
- bootstrap 95%: accuracy CI 0.774–0.820, ECE CI 0.077–0.115
- cost: $0.000023/case ($0.0092 total)
- latency: p50 323ms, p95 392ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 400 | 0 | 0.980 | 0.984 | 0.023 | 0.014 |
| queue | choice | 400 | 0 | 0.850 | 0.917 | 0.067 | — |
| urgency | score | 400 | 0 | 0.560 | 0.767 | 0.207 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.972 | 0.804 |
| 0.60 | 0.902 | 0.834 |
| 0.70 | 0.844 | 0.859 |
| 0.80 | 0.771 | 0.893 |
| 0.90 | 0.690 | 0.920 |
| 0.95 | 0.629 | 0.942 |

## Author thresholds (pack threshold floors)

- auto-accepted 1002/1200 (0.835), precision 0.851
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
