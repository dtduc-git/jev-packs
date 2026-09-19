# jevassert report — rag-answerability v0.5.0

- model: `claude-sonnet-5` (pack pinned to `jev-1.13.0`)
- cases: 420 (0 errors, 0 missing answers)
- items: 840 — accuracy **0.908**, ECE **0.059**
- bootstrap 95%: accuracy CI 0.889–0.929, ECE CI 0.041–0.073
- cost: $0.003695/case ($1.5518 total)
- latency: p50 2087ms, p95 4309ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| answerable | noul | 420 | 0 | 0.960 | 0.950 | 0.032 | 0.028 |
| missing_info | choice | 420 | 0 | 0.857 | 0.839 | 0.097 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.996 | 0.910 |
| 0.60 | 0.965 | 0.927 |
| 0.70 | 0.926 | 0.946 |
| 0.80 | 0.836 | 0.977 |
| 0.90 | 0.636 | 0.989 |
| 0.95 | 0.552 | 0.994 |

## Author thresholds (pack threshold floors)

- auto-accepted 719/840 (0.856), precision 0.965
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
