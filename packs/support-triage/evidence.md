# jevassert report — support-triage v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 100 (0 errors, 0 missing answers)
- items: 300 — accuracy **0.847**, ECE **0.063**
- bootstrap 95%: accuracy CI 0.807–0.887, ECE CI 0.037–0.101
- cost: $0.000023/case ($0.0023 total)
- latency: p50 324ms, p95 837ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 100 | 0 | 0.980 | 0.982 | 0.021 | 0.009 |
| queue | choice | 100 | 0 | 0.870 | 0.928 | 0.068 | — |
| urgency | score | 100 | 0 | 0.690 | 0.807 | 0.125 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.987 | 0.851 |
| 0.60 | 0.937 | 0.875 |
| 0.70 | 0.890 | 0.895 |
| 0.80 | 0.813 | 0.910 |
| 0.90 | 0.717 | 0.935 |
| 0.95 | 0.653 | 0.944 |

## Author thresholds (pack threshold floors)

- auto-accepted 267/300 (0.890), precision 0.888
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
