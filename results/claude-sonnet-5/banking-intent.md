# jevassert report — banking-intent v0.2.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.847**, ECE **0.110**
- bootstrap 95%: accuracy CI 0.787–0.900, ECE CI 0.069–0.152
- cost: $0.005792/case ($0.8688 total)
- latency: p50 2757ms, p95 5731ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| intent | choice | 150 | 0 | 0.847 | 0.813 | 0.110 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.940 | 0.887 |
| 0.60 | 0.847 | 0.929 |
| 0.70 | 0.760 | 0.947 |
| 0.80 | 0.693 | 0.952 |
| 0.90 | 0.493 | 0.973 |
| 0.95 | 0.287 | 0.977 |

## Author thresholds (pack threshold floors)

- auto-accepted 112/150 (0.747), precision 0.964
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
