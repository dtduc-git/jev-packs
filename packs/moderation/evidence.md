# jevassert report — moderation v0.3.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 200 (0 errors, 0 missing answers)
- items: 600 — accuracy **0.795**, ECE **0.080**
- bootstrap 95%: accuracy CI 0.762–0.827, ECE CI 0.056–0.109
- cost: $0.000022/case ($0.0045 total)
- latency: p50 318ms, p95 408ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| action | choice | 200 | 0 | 0.700 | 0.789 | 0.116 | — |
| severity | score | 200 | 0 | 0.690 | 0.861 | 0.171 | — |
| targeted_group | noul | 200 | 0 | 0.995 | 0.963 | 0.032 | 0.006 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.940 | 0.824 |
| 0.60 | 0.877 | 0.859 |
| 0.70 | 0.817 | 0.888 |
| 0.80 | 0.760 | 0.908 |
| 0.90 | 0.685 | 0.934 |
| 0.95 | 0.570 | 0.944 |

## Author thresholds (pack threshold floors)

- auto-accepted 462/600 (0.770), precision 0.892
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
