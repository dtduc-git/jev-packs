# support-triage

Route one inbound customer support message to the right queue, flag explicit
refund requests and rank urgency.

## Questions

| question | type | labels |
|---|---|---|
| `refund_request` | noul | true / false |
| `queue` | choice | billing, technical, shipping, account, other, unknown |
| `urgency` | score | low, normal, high, critical, unknown |

### Labeling rules

- `refund_request` is **explicit only**: the sender asks for a refund, return or
  money back. "The item arrived damaged", "pricing is unfair" or "I might
  cancel" are `false`; "I want my money back" is `true`.
- `queue` follows the fix, not the symptom: anything that ends in money moving
  back goes to `billing` (including returns and fee reversals); delivery and
  address issues go to `shipping`.
- `urgency` follows the pack.yaml `level_descriptions` anchors literally:
  `critical` = ongoing outage or data loss; `high` = work blocked, money at
  stake or access lost; `normal` = standard request without impact; `low` =
  feedback, pre-sales, cosmetic. The sender's own tone does not raise urgency
  by itself.
- Gold cases are labeled from `message` alone, with no ticket history.

## Provenance

All 50 cases were written for this pack (CC0-1.0). No external dataset.
Messages are synthetic; any resemblance to real tickets is coincidental.

## Thresholds

Conservative floors for a no-human step: 0.8 on both `refund_request` labels,
0.6 per queue, 0.7 per urgency level. `unknown` has no floor — it always routes
to review.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.840**, ECE 0.062,
$0.000023/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
