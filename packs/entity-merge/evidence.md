# jevassert report — entity-merge v0.3.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 210 (0 errors, 0 missing answers)
- items: 420 — accuracy **0.879**, ECE **0.059**
- bootstrap 95%: accuracy CI 0.848–0.910, ECE CI 0.045–0.088
- cost: $0.000018/case ($0.0038 total)
- latency: p50 315ms, p95 403ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| same_entity | noul | 210 | 0 | 0.881 | 0.825 | 0.070 | 0.086 |
| action | choice | 210 | 0 | 0.876 | 0.844 | 0.051 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.983 | 0.884 |
| 0.60 | 0.900 | 0.910 |
| 0.70 | 0.771 | 0.957 |
| 0.80 | 0.683 | 0.986 |
| 0.90 | 0.486 | 0.990 |
| 0.95 | 0.302 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 283/420 (0.674), precision 0.972
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
