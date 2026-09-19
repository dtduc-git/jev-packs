# jevassert report — citation-support v0.3.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 200 (0 errors, 0 missing answers)
- items: 400 — accuracy **0.905**, ECE **0.032**
- bootstrap 95%: accuracy CI 0.875–0.932, ECE CI 0.022–0.064
- cost: $0.000017/case ($0.0035 total)
- latency: p50 318ms, p95 410ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 200 | 0 | 0.990 | 0.933 | 0.057 | 0.013 |
| coverage | score | 200 | 0 | 0.820 | 0.928 | 0.110 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.998 | 0.907 |
| 0.60 | 0.978 | 0.916 |
| 0.70 | 0.953 | 0.934 |
| 0.80 | 0.907 | 0.945 |
| 0.90 | 0.800 | 0.959 |
| 0.95 | 0.615 | 0.976 |

## Author thresholds (pack threshold floors)

- auto-accepted 358/400 (0.895), precision 0.933
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
