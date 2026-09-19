# jevassert report — support-triage v0.6.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 450 (0 errors, 0 missing answers)
- items: 1350 — accuracy **0.887**, ECE **0.059**
- bootstrap 95%: accuracy CI 0.871–0.904, ECE CI 0.044–0.073
- cost: $0.000028/case ($0.0124 total)
- latency: p50 325ms, p95 398ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 450 | 0 | 0.980 | 0.983 | 0.023 | 0.014 |
| queue | choice | 450 | 0 | 0.849 | 0.913 | 0.064 | — |
| urgency | score | 450 | 0 | 0.833 | 0.930 | 0.097 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.994 | 0.890 |
| 0.60 | 0.965 | 0.905 |
| 0.70 | 0.932 | 0.919 |
| 0.80 | 0.890 | 0.937 |
| 0.90 | 0.835 | 0.957 |
| 0.95 | 0.786 | 0.965 |

## Author thresholds (pack threshold floors)

- auto-accepted 1251/1350 (0.927), precision 0.912
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
