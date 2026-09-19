# jevassert report — support-triage v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 50 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.840**, ECE **0.062**
- cost: $0.000023/case ($0.0012 total)
- latency: p50 316ms, p95 781ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 50 | 0 | 0.980 | 0.979 | 0.020 | 0.008 |
| queue | choice | 50 | 0 | 0.860 | 0.923 | 0.070 | — |
| urgency | score | 50 | 0 | 0.680 | 0.799 | 0.170 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.840 |
| 0.60 | 0.947 | 0.859 |
| 0.70 | 0.867 | 0.892 |
| 0.80 | 0.773 | 0.922 |
| 0.90 | 0.693 | 0.952 |
| 0.95 | 0.640 | 0.969 |

## Author thresholds (pack threshold floors)

- auto-accepted 130/150 (0.867), precision 0.877
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
