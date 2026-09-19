# jevassert report — banking-intent v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.840**, ECE **0.090**
- bootstrap 95%: accuracy CI 0.780–0.893, ECE CI 0.056–0.158
- cost: $0.000029/case ($0.0044 total)
- latency: p50 324ms, p95 750ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| intent | choice | 150 | 0 | 0.840 | 0.930 | 0.090 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.980 | 0.844 |
| 0.60 | 0.933 | 0.871 |
| 0.70 | 0.893 | 0.873 |
| 0.80 | 0.853 | 0.875 |
| 0.90 | 0.800 | 0.908 |
| 0.95 | 0.787 | 0.915 |

## Author thresholds (pack threshold floors)

- auto-accepted 129/150 (0.860), precision 0.907
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
