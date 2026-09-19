# jevassert report — rag-answerability v0.5.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 420 (0 errors, 0 missing answers)
- items: 840 — accuracy **0.908**, ECE **0.021**
- bootstrap 95%: accuracy CI 0.889–0.927, ECE CI 0.016–0.043
- cost: $0.000025/case ($0.0104 total)
- latency: p50 307ms, p95 727ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 420 | 0 | 0.960 | 0.907 | 0.052 | 0.033 |
| missing_info | choice | 420 | 0 | 0.857 | 0.890 | 0.037 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.981 | 0.917 |
| 0.60 | 0.933 | 0.938 |
| 0.70 | 0.883 | 0.946 |
| 0.80 | 0.824 | 0.965 |
| 0.90 | 0.737 | 0.977 |
| 0.95 | 0.594 | 0.980 |

## Author thresholds (pack threshold floors)

- auto-accepted 672/840 (0.800), precision 0.963
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
