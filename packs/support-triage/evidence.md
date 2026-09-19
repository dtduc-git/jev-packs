# jevassert report — support-triage v0.5.0

- model: `jev-1.13.0` (recorded against `jev-1.13.0`)
- cases: 430 (0 errors, 0 missing answers)
- items: 1290 — accuracy **0.843**, ECE **0.059**
- bootstrap 95%: accuracy CI 0.823–0.864, ECE CI 0.046–0.079
- cost: $0.000027/case ($0.0117 total)
- latency: p50 314ms, p95 386ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| refund_request | noul | 430 | 0 | 0.981 | 0.984 | 0.022 | 0.014 |
| queue | choice | 430 | 0 | 0.856 | 0.916 | 0.060 | — |
| urgency | score | 430 | 0 | 0.693 | 0.795 | 0.130 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.969 | 0.852 |
| 0.60 | 0.911 | 0.874 |
| 0.70 | 0.867 | 0.890 |
| 0.80 | 0.791 | 0.920 |
| 0.90 | 0.712 | 0.954 |
| 0.95 | 0.660 | 0.968 |

## Author thresholds (pack threshold floors)

- auto-accepted 1112/1290 (0.862), precision 0.883
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in pack.yaml.
