# jevassert report — citation-support v0.4.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.910**, ECE **0.081**
- bootstrap 95%: accuracy CI 0.890–0.930, ECE CI 0.059–0.101
- cost: $0.002505/case ($1.0018 total)
- latency: p50 1690ms, p95 2641ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| supports | noul | 400 | 0 | 0.975 | 0.918 | 0.057 | 0.023 |
| coverage | score | 400 | 0 | 0.845 | 0.861 | 0.161 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.998 | 0.912 |
| 0.60 | 0.981 | 0.920 |
| 0.70 | 0.948 | 0.926 |
| 0.80 | 0.874 | 0.937 |
| 0.90 | 0.624 | 0.990 |
| 0.95 | 0.446 | 1.000 |

## Author thresholds (pack threshold floors)

- auto-accepted 729/800 (0.911), precision 0.925
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
