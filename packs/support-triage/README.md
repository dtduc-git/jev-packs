# support-triage

Route one inbound customer support message to the right queue, flag explicit
refund requests and rank urgency.

## Questions

| question | type | labels |
|---|---|---|
| `refund_request` | noul | true / false |
| `queue` | choice | billing, technical, shipping, account, other, unknown |
| `urgency` | score | normal, high, critical, unknown |

### Labeling rules

- `refund_request` is **explicit only**: the sender asks for a refund, a
  return, a charge reversal or money back. "The item arrived damaged",
  "pricing is unfair" or "I might cancel" are `false`; "I want my money back"
  is `true`.
- `queue` follows the fix, not the symptom: anything that ends in money moving
  back goes to `billing` (including returns and fee reversals); delivery and
  address issues go to `shipping`; user, workspace, team and settings
  management (including data export and deletion) goes to `account`; pre-sales
  questions, evaluations and compliance checks (audit logs, data regions) go
  to `other`.
- `urgency` uses three operational levels: `critical` = a capability the
  sender depends on is completely unavailable right now with no routine fix,
  data is being lost, or a live security incident; `high` = something is not
  working, failing, delayed, missing or costing money (bugs, delivery
  problems, stuck requests, refunds), **including access a routine support
  action can restore** (password reset, restore from backup, re-invite);
  `normal` = requests, questions, feedback, feature requests. Tone never
  changes the level. (The former `low` level was removed: feedback has the
  same operational urgency as any other request.)
- Gold cases are labeled from `message` alone, with no ticket history.

## Provenance

All 400 cases were written for this pack (CC0-1.0). No external dataset.
Messages are synthetic; any resemblance to real tickets is coincidental.

## Thresholds

Conservative floors for a no-human step: 0.8 on both `refund_request` labels,
0.6 per queue, 0.7 per urgency level. `unknown` has no floor — it always routes
to review.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.887**, ECE 0.059,
$0.000028/case. The 0.6.0 redesign (three operational urgency levels; bugs and
delivery problems are `high`) lifted `urgency` from 0.69 to 0.83. Full report:
[evidence.md](evidence.md); raw recording: [predictions.jsonl](predictions.jsonl).
