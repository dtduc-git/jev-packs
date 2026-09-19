# jevassert report — citation-support v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 100 (0 errors, 0 missing answers)
- items: 200 — accuracy **0.890**, ECE **0.076**
- bootstrap 95%: accuracy CI 0.850–0.930, ECE CI 0.041–0.104
- cost: $0.000017/case ($0.0017 total)
- latency: p50 323ms, p95 767ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 100 | 0 | 0.980 | 0.935 | 0.045 | 0.017 |
| coverage | score | 100 | 0 | 0.800 | 0.929 | 0.131 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.995 | 0.894 |
| 0.60 | 0.980 | 0.903 |
| 0.70 | 0.955 | 0.927 |
| 0.80 | 0.925 | 0.935 |
| 0.90 | 0.795 | 0.950 |
| 0.95 | 0.605 | 0.967 |

## Author thresholds (pack threshold floors)

- auto-accepted 181/200 (0.905), precision 0.928
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
