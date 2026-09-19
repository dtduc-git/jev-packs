# jevassert report — sms-spam v0.1.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.953**, ECE **0.040**
- bootstrap 95%: accuracy CI 0.913–0.987, ECE CI 0.032–0.074
- cost: $0.000014/case ($0.0021 total)
- latency: p50 183ms, p95 358ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| spam | noul | 150 | 0 | 0.953 | 0.923 | 0.040 | 0.037 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.953 |
| 0.60 | 0.967 | 0.972 |
| 0.70 | 0.940 | 0.972 |
| 0.80 | 0.893 | 0.978 |
| 0.90 | 0.833 | 0.984 |
| 0.95 | 0.660 | 0.990 |

## Author thresholds (pack threshold floors)

- auto-accepted 125/150 (0.833), precision 0.984
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
