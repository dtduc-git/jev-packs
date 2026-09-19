# jevassert report — rag-answerability v0.6.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 420 (0 errors, 0 missing answers)
- items: 840 — accuracy **0.927**, ECE **0.034**
- bootstrap 95%: accuracy CI 0.910–0.945, ECE CI 0.030–0.061
- cost: $0.004341/case ($1.8232 total)
- latency: p50 2295ms, p95 5179ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 420 | 0 | 0.962 | 0.953 | 0.026 | 0.032 |
| missing_info | choice | 420 | 0 | 0.893 | 0.836 | 0.079 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.998 | 0.930 |
| 0.60 | 0.976 | 0.935 |
| 0.70 | 0.938 | 0.943 |
| 0.80 | 0.810 | 0.966 |
| 0.90 | 0.617 | 0.990 |
| 0.95 | 0.552 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 709/840 (0.844), precision 0.962
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
