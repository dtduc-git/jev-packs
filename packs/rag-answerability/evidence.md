# jevassert report — rag-answerability v0.2.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 100 (0 errors, 0 missing answers)
- items: 200 — accuracy **0.905**, ECE **0.040**
- bootstrap 95%: accuracy CI 0.860–0.945, ECE CI 0.025–0.078
- cost: $0.000020/case ($0.0020 total)
- latency: p50 306ms, p95 753ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 100 | 0 | 0.970 | 0.925 | 0.045 | 0.028 |
| missing_info | choice | 100 | 0 | 0.840 | 0.882 | 0.073 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.975 | 0.913 |
| 0.60 | 0.940 | 0.926 |
| 0.70 | 0.885 | 0.949 |
| 0.80 | 0.830 | 0.970 |
| 0.90 | 0.725 | 0.986 |
| 0.95 | 0.665 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 165/200 (0.825), precision 0.958
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
