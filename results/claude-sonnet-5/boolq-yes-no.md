# jevassert report — boolq-yes-no v0.1.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 150 (0 errors, 0 missing answers)
- items: 150 — accuracy **0.893**, ECE **0.092**
- bootstrap 95%: accuracy CI 0.847–0.940, ECE CI 0.051–0.139
- cost: $0.001920/case ($0.2880 total)
- latency: p50 1418ms, p95 2547ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answer_yes | noul | 150 | 0 | 0.893 | 0.940 | 0.092 | 0.089 |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 1.000 | 0.893 |
| 0.60 | 0.987 | 0.899 |
| 0.70 | 0.980 | 0.905 |
| 0.80 | 0.973 | 0.904 |
| 0.90 | 0.840 | 0.929 |
| 0.95 | 0.767 | 0.930 |

## Author thresholds (pack threshold floors)

- auto-accepted 144/150 (0.960), precision 0.903
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
