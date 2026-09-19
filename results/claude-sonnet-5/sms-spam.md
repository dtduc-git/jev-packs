# jevassert report — sms-spam v0.1.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.947**, ECE **0.039**
- bootstrap 95%: accuracy CI 0.907–0.980, ECE CI 0.021–0.075
- cost: $0.001547/case ($0.2321 total)
- latency: p50 1374ms, p95 2547ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| spam | noul | 150 | 0 | 0.947 | 0.955 | 0.039 | 0.033 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.947 |
| 0.60 | 0.993 | 0.953 |
| 0.70 | 0.967 | 0.966 |
| 0.80 | 0.953 | 0.979 |
| 0.90 | 0.920 | 0.993 |
| 0.95 | 0.880 | 0.992 |

## Author thresholds (pack threshold floors)

- auto-accepted 138/150 (0.920), precision 0.993
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
