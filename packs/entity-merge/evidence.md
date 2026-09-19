# jevassert report — entity-merge v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 105 (0 errors, 0 missing answers)
- items: 210 — accuracy **0.890**, ECE **0.050**
- bootstrap 95%: accuracy CI 0.848–0.933, ECE CI 0.040–0.099
- cost: $0.000018/case ($0.0019 total)
- latency: p50 324ms, p95 748ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| same_entity | noul | 105 | 0 | 0.857 | 0.835 | 0.065 | 0.093 |
| action | choice | 105 | 0 | 0.924 | 0.849 | 0.075 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.971 | 0.902 |
| 0.60 | 0.886 | 0.919 |
| 0.70 | 0.776 | 0.963 |
| 0.80 | 0.710 | 0.980 |
| 0.90 | 0.524 | 0.991 |
| 0.95 | 0.376 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 148/210 (0.705), precision 0.980
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
