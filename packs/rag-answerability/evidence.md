# jevassert report — rag-answerability v0.6.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 420 (0 errors, 0 missing answers)
- items: 840 — accuracy **0.930**, ECE **0.027**
- bootstrap 95%: accuracy CI 0.912–0.946, ECE CI 0.019–0.045
- cost: $0.000032/case ($0.0133 total)
- latency: p50 320ms, p95 408ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 420 | 0 | 0.964 | 0.908 | 0.057 | 0.033 |
| missing_info | choice | 420 | 0 | 0.895 | 0.902 | 0.023 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.993 | 0.930 |
| 0.60 | 0.946 | 0.946 |
| 0.70 | 0.905 | 0.957 |
| 0.80 | 0.839 | 0.972 |
| 0.90 | 0.727 | 0.979 |
| 0.95 | 0.583 | 0.984 |

## Author thresholds (pack threshold floors)

- auto-accepted 678/840 (0.807), precision 0.973
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
