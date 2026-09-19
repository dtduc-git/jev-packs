# jevassert report — support-triage v0.6.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 450 (0 errors, 0 missing answers)
- items: 1350 — accuracy **0.905**, ECE **0.072**
- bootstrap 95%: accuracy CI 0.890–0.921, ECE CI 0.062–0.090
- cost: $0.005089/case ($2.2902 total)
- latency: p50 2619ms, p95 5671ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 450 | 0 | 0.987 | 0.972 | 0.015 | 0.010 |
| queue | choice | 450 | 0 | 0.884 | 0.760 | 0.124 | — |
| urgency | score | 450 | 0 | 0.844 | 0.768 | 0.113 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.962 | 0.916 |
| 0.60 | 0.888 | 0.942 |
| 0.70 | 0.822 | 0.957 |
| 0.80 | 0.694 | 0.990 |
| 0.90 | 0.476 | 1.000 |
| 0.95 | 0.336 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 1121/1350 (0.830), precision 0.956
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
