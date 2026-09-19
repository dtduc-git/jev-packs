# jevassert report — rag-answerability v0.3.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 200 (0 errors, 0 missing answers)
- items: 400 — accuracy **0.877**, ECE **0.037**
- bootstrap 95%: accuracy CI 0.843–0.910, ECE CI 0.024–0.069
- cost: $0.000020/case ($0.0041 total)
- latency: p50 313ms, p95 369ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 200 | 0 | 0.935 | 0.918 | 0.045 | 0.042 |
| missing_info | choice | 200 | 0 | 0.820 | 0.862 | 0.061 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.970 | 0.892 |
| 0.60 | 0.920 | 0.916 |
| 0.70 | 0.845 | 0.938 |
| 0.80 | 0.805 | 0.960 |
| 0.90 | 0.710 | 0.989 |
| 0.95 | 0.615 | 0.996 |

## Author thresholds (pack threshold floors)

- auto-accepted 323/400 (0.807), precision 0.941
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
