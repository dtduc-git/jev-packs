# jevassert report — support-triage v0.7.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 450 (0 errors, 0 missing answers)
- items: 1350 — accuracy **0.898**, ECE **0.057**
- bootstrap 95%: accuracy CI 0.882–0.915, ECE CI 0.043–0.071
- cost: $0.000031/case ($0.0141 total)
- latency: p50 315ms, p95 391ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 450 | 0 | 0.984 | 0.984 | 0.019 | 0.013 |
| queue | choice | 450 | 0 | 0.860 | 0.922 | 0.062 | — |
| urgency | score | 450 | 0 | 0.849 | 0.945 | 0.096 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.990 | 0.904 |
| 0.60 | 0.973 | 0.908 |
| 0.70 | 0.946 | 0.918 |
| 0.80 | 0.907 | 0.931 |
| 0.90 | 0.864 | 0.947 |
| 0.95 | 0.818 | 0.957 |

## Author thresholds (pack threshold floors)

- auto-accepted 1266/1350 (0.938), precision 0.912
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
