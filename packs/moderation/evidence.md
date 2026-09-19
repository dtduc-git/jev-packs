# jevassert report — moderation v0.5.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 430 (0 errors, 0 missing answers)
- items: 1290 — accuracy **0.872**, ECE **0.050**
- bootstrap 95%: accuracy CI 0.853–0.891, ECE CI 0.037–0.069
- cost: $0.000028/case ($0.0122 total)
- latency: p50 317ms, p95 385ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 430 | 0 | 0.928 | 0.910 | 0.018 | — |
| severity | score | 430 | 0 | 0.698 | 0.881 | 0.197 | — |
| targeted_group | noul | 430 | 0 | 0.991 | 0.960 | 0.031 | 0.008 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.987 | 0.876 |
| 0.60 | 0.947 | 0.888 |
| 0.70 | 0.901 | 0.902 |
| 0.80 | 0.852 | 0.913 |
| 0.90 | 0.770 | 0.932 |
| 0.95 | 0.677 | 0.940 |

## Author thresholds (pack threshold floors)

- auto-accepted 1106/1290 (0.857), precision 0.896
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
