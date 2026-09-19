# jevassert report — sms-spam v0.1.0

- model: `qwen2.5:7b` (pack pinned to `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.813**, ECE **0.107**
- bootstrap 95%: accuracy CI 0.747–0.873, ECE CI 0.066–0.176
- cost: $0.000000/case ($0.0000 total)
- latency: p50 4688ms, p95 5686ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| spam | noul | 150 | 0 | 0.813 | 0.903 | 0.107 | 0.135 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.813 |
| 0.60 | 0.973 | 0.822 |
| 0.70 | 0.913 | 0.854 |
| 0.80 | 0.860 | 0.876 |
| 0.90 | 0.633 | 0.926 |
| 0.95 | 0.520 | 0.936 |

## Author thresholds (pack threshold floors)

- auto-accepted 95/150 (0.633), precision 0.926
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
