# jevassert report — sms-spam v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.967**, ECE **0.053**
- bootstrap 95%: accuracy CI 0.933–0.993, ECE CI 0.036–0.085
- cost: $0.000014/case ($0.0021 total)
- latency: p50 308ms, p95 724ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| spam | noul | 150 | 0 | 0.967 | 0.924 | 0.053 | 0.037 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.967 |
| 0.60 | 0.967 | 0.972 |
| 0.70 | 0.940 | 0.972 |
| 0.80 | 0.900 | 0.978 |
| 0.90 | 0.813 | 0.984 |
| 0.95 | 0.680 | 0.990 |

## Author thresholds (pack threshold floors)

- auto-accepted 122/150 (0.813), precision 0.984
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
