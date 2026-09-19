# jevassert report — banking-intent v0.2.0

- model: `qwen2.5:7b` (pack pinned to `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.533**, ECE **0.195**
- bootstrap 95%: accuracy CI 0.460–0.613, ECE CI 0.105–0.240
- cost: $0.000000/case ($0.0000 total)
- latency: p50 32128ms, p95 34272ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| intent | choice | 150 | 0 | 0.533 | 0.580 | 0.195 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.593 | 0.640 |
| 0.60 | 0.407 | 0.738 |
| 0.70 | 0.393 | 0.746 |
| 0.80 | 0.320 | 0.750 |
| 0.90 | 0.253 | 0.737 |
| 0.95 | 0.240 | 0.750 |

## Author thresholds (pack threshold floors)

- auto-accepted 51/150 (0.340), precision 0.863
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
