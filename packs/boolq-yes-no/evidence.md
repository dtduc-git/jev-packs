# jevassert report — boolq-yes-no v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.887**, ECE **0.063**
- bootstrap 95%: accuracy CI 0.833–0.933, ECE CI 0.031–0.105
- cost: $0.000018/case ($0.0027 total)
- latency: p50 312ms, p95 711ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answer_yes | noul | 150 | 0 | 0.887 | 0.906 | 0.063 | 0.081 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.887 |
| 0.60 | 0.967 | 0.897 |
| 0.70 | 0.900 | 0.926 |
| 0.80 | 0.833 | 0.952 |
| 0.90 | 0.700 | 0.952 |
| 0.95 | 0.593 | 0.978 |

## Author thresholds (pack threshold floors)

- auto-accepted 119/150 (0.793), precision 0.958
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
