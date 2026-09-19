# jevassert report — rag-passage-relevance v0.4.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.899**, ECE **0.035**
- bootstrap 95%: accuracy CI 0.879–0.920, ECE CI 0.020–0.053
- cost: $0.000018/case ($0.0070 total)
- latency: p50 313ms, p95 390ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 400 | 0 | 0.968 | 0.957 | 0.017 | 0.024 |
| quality | score | 400 | 0 | 0.830 | 0.895 | 0.065 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.999 | 0.900 |
| 0.60 | 0.956 | 0.918 |
| 0.70 | 0.914 | 0.932 |
| 0.80 | 0.861 | 0.946 |
| 0.90 | 0.802 | 0.960 |
| 0.95 | 0.720 | 0.972 |

## Author thresholds (pack threshold floors)

- auto-accepted 697/800 (0.871), precision 0.931
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
