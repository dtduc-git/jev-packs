# jevassert report — moderation v0.8.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 450 (0 errors, 0 missing answers)
- items: 1350 — accuracy **0.917**, ECE **0.013**
- bootstrap 95%: accuracy CI 0.901–0.933, ECE CI 0.008–0.029
- cost: $0.000044/case ($0.0196 total)
- latency: p50 334ms, p95 428ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 450 | 0 | 0.916 | 0.907 | 0.010 | — |
| severity | score | 450 | 0 | 0.847 | 0.912 | 0.067 | — |
| targeted_group | noul | 450 | 0 | 0.989 | 0.959 | 0.030 | 0.008 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.990 | 0.924 |
| 0.60 | 0.953 | 0.941 |
| 0.70 | 0.912 | 0.953 |
| 0.80 | 0.872 | 0.965 |
| 0.90 | 0.797 | 0.977 |
| 0.95 | 0.720 | 0.981 |

## Author thresholds (pack threshold floors)

- auto-accepted 1148/1350 (0.850), precision 0.948
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
