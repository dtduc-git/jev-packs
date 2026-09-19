# jevassert report — entity-merge v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 55 (0 errors, 0 missing answers)
- items: 110 — accuracy **0.882**, ECE **0.046**
- cost: $0.000018/case ($0.0010 total)
- latency: p50 321ms, p95 764ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| same_entity | noul | 55 | 0 | 0.855 | 0.849 | 0.113 | 0.094 |
| action | choice | 55 | 0 | 0.909 | 0.869 | 0.098 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.991 | 0.890 |
| 0.60 | 0.891 | 0.918 |
| 0.70 | 0.773 | 0.965 |
| 0.80 | 0.727 | 0.988 |
| 0.90 | 0.591 | 1.000 |
| 0.95 | 0.464 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 83/110 (0.755), precision 0.988
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
