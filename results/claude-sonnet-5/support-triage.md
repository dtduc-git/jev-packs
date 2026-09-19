# jevassert report — support-triage v0.7.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 450 (0 errors, 0 missing answers)
- items: 1350 — accuracy **0.913**, ECE **0.078**
- bootstrap 95%: accuracy CI 0.899–0.928, ECE CI 0.067–0.092
- cost: $0.005591/case ($2.5160 total)
- latency: p50 3006ms, p95 6426ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 450 | 0 | 0.987 | 0.970 | 0.017 | 0.010 |
| queue | choice | 450 | 0 | 0.889 | 0.755 | 0.134 | — |
| urgency | score | 450 | 0 | 0.864 | 0.781 | 0.114 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.979 | 0.917 |
| 0.60 | 0.893 | 0.947 |
| 0.70 | 0.829 | 0.965 |
| 0.80 | 0.694 | 0.988 |
| 0.90 | 0.457 | 1.000 |
| 0.95 | 0.336 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 1125/1350 (0.833), precision 0.960
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
