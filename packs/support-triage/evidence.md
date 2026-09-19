# jevassert report — support-triage v0.3.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 200 (0 errors, 0 missing answers)
- items: 600 — accuracy **0.815**, ECE **0.089**
- bootstrap 95%: accuracy CI 0.785–0.847, ECE CI 0.064–0.118
- cost: $0.000023/case ($0.0046 total)
- latency: p50 320ms, p95 394ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 200 | 0 | 0.985 | 0.982 | 0.016 | 0.007 |
| queue | choice | 200 | 0 | 0.870 | 0.925 | 0.063 | — |
| urgency | score | 200 | 0 | 0.590 | 0.798 | 0.210 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.980 | 0.820 |
| 0.60 | 0.932 | 0.841 |
| 0.70 | 0.873 | 0.865 |
| 0.80 | 0.797 | 0.895 |
| 0.90 | 0.705 | 0.920 |
| 0.95 | 0.648 | 0.946 |

## Author thresholds (pack threshold floors)

- auto-accepted 525/600 (0.875), precision 0.855
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
