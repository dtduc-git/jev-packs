# jevassert report — citation-support v0.4.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.919**, ECE **0.022**
- bootstrap 95%: accuracy CI 0.900–0.938, ECE CI 0.015–0.043
- cost: $0.000017/case ($0.0069 total)
- latency: p50 320ms, p95 390ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 400 | 0 | 0.995 | 0.937 | 0.058 | 0.010 |
| coverage | score | 400 | 0 | 0.843 | 0.922 | 0.081 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.999 | 0.920 |
| 0.60 | 0.978 | 0.931 |
| 0.70 | 0.940 | 0.949 |
| 0.80 | 0.901 | 0.960 |
| 0.90 | 0.804 | 0.972 |
| 0.95 | 0.627 | 0.984 |

## Author thresholds (pack threshold floors)

- auto-accepted 710/800 (0.887), precision 0.948
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
