# jevassert report — moderation v0.6.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 450 (0 errors, 0 missing answers)
- items: 1350 — accuracy **0.906**, ECE **0.027**
- bootstrap 95%: accuracy CI 0.890–0.921, ECE CI 0.018–0.043
- cost: $0.000031/case ($0.0138 total)
- latency: p50 326ms, p95 1036ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 450 | 0 | 0.916 | 0.906 | 0.015 | — |
| severity | score | 450 | 0 | 0.811 | 0.917 | 0.106 | — |
| targeted_group | noul | 450 | 0 | 0.991 | 0.959 | 0.032 | 0.008 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.987 | 0.912 |
| 0.60 | 0.961 | 0.921 |
| 0.70 | 0.921 | 0.933 |
| 0.80 | 0.879 | 0.947 |
| 0.90 | 0.796 | 0.964 |
| 0.95 | 0.706 | 0.979 |

## Author thresholds (pack threshold floors)

- auto-accepted 1163/1350 (0.861), precision 0.929
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
