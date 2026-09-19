# jevassert report — rag-answerability v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 50 (0 errors, 0 missing answers)
- items: 100 — accuracy **0.940**, ECE **0.044**
- cost: $0.000020/case ($0.0010 total)
- latency: p50 308ms, p95 744ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 50 | 0 | 0.980 | 0.947 | 0.033 | 0.016 |
| missing_info | choice | 50 | 0 | 0.900 | 0.904 | 0.054 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.940 |
| 0.60 | 0.950 | 0.958 |
| 0.70 | 0.920 | 0.967 |
| 0.80 | 0.890 | 0.989 |
| 0.90 | 0.790 | 0.987 |
| 0.95 | 0.720 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 90/100 (0.900), precision 0.978
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
