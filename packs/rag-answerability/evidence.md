# jevassert report — rag-answerability v0.4.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.861**, ECE **0.051**
- bootstrap 95%: accuracy CI 0.839–0.886, ECE CI 0.030–0.070
- cost: $0.000020/case ($0.0081 total)
- latency: p50 320ms, p95 397ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 400 | 0 | 0.940 | 0.911 | 0.030 | 0.045 |
| missing_info | choice | 400 | 0 | 0.782 | 0.850 | 0.085 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.963 | 0.877 |
| 0.60 | 0.896 | 0.894 |
| 0.70 | 0.843 | 0.912 |
| 0.80 | 0.785 | 0.944 |
| 0.90 | 0.680 | 0.972 |
| 0.95 | 0.576 | 0.987 |

## Author thresholds (pack threshold floors)

- auto-accepted 631/800 (0.789), precision 0.921
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
