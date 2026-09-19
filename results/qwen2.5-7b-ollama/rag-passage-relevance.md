# jevassert report — rag-passage-relevance v0.4.0

- model: `qwen2.5:7b` (pack pinned to `jev-1.13.0`)
- cases: 400 (0 errors, 0 missing answers)
- items: 800 — accuracy **0.552**, ECE **0.326**
- bootstrap 95%: accuracy CI 0.521–0.589, ECE CI 0.298–0.355
- cost: $0.000000/case ($0.0000 total)
- latency: p50 8844ms, p95 10097ms

## Per question

| question | type | n | missing | accuracy | mean p(decision) | ECE | Brier |
|---|---|---|---|---|---|---|---|
| relevant | noul | 400 | 0 | 0.915 | 0.955 | 0.040 | 0.064 |
| quality | score | 400 | 0 | 0.190 | 0.803 | 0.613 | — |

## Coverage at decision probability

| accept if p >= | coverage | precision |
|---|---|---|
| 0.50 | 0.968 | 0.567 |
| 0.60 | 0.890 | 0.597 |
| 0.70 | 0.821 | 0.639 |
| 0.80 | 0.764 | 0.674 |
| 0.90 | 0.671 | 0.739 |
| 0.95 | 0.630 | 0.758 |

## Author thresholds (pack threshold floors)

- auto-accepted 632/800 (0.790), precision 0.639
- labels without a floor (usually `unknown`) always route to review

## Gates

No gates declared in gates.yaml.
