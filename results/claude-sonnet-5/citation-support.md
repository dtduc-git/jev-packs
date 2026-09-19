# jevassert report — citation-support v0.5.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.941**, ECE **0.057**
- bootstrap 95%: accuracy CI 0.925–0.958, ECE CI 0.046–0.072
- cost: $0.002784/case ($1.1135 total)
- latency: p50 1729ms, p95 3344ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 400 | 0 | 0.927 | 0.909 | 0.051 | 0.035 |
| coverage | score | 400 | 0 | 0.955 | 0.896 | 0.059 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.996 | 0.942 |
| 0.60 | 0.960 | 0.973 |
| 0.70 | 0.929 | 0.978 |
| 0.80 | 0.907 | 0.988 |
| 0.90 | 0.736 | 0.998 |
| 0.95 | 0.511 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 729/800 (0.911), precision 0.981
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
