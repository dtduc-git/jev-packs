# jevassert report — citation-support v0.5.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.979**, ECE **0.034**
- bootstrap 95%: accuracy CI 0.969–0.988, ECE CI 0.027–0.042
- cost: $0.000019/case ($0.0077 total)
- latency: p50 331ms, p95 410ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 400 | 0 | 0.995 | 0.937 | 0.058 | 0.010 |
| coverage | score | 400 | 0 | 0.963 | 0.953 | 0.016 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.979 |
| 0.60 | 0.990 | 0.982 |
| 0.70 | 0.974 | 0.986 |
| 0.80 | 0.944 | 0.996 |
| 0.90 | 0.854 | 1.000 |
| 0.95 | 0.662 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 740/800 (0.925), precision 0.986
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
