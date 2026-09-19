# Disagreement harvest — Jev 1.13.0 vs Claude Sonnet 5 (2026-09-19)

Tool: `scripts/disagreements.py`. Raw dumps: `review/<a>-vs-<b>/<pack>.jsonl`
(gitignored); machine summary: `summary.json` next to this file.

6427 items, 458 case-level disagreements (7.1%): 221 Jev-only correct,
205 Sonnet-only correct, 33 both-wrong, 3 missing (one Sonnet case error on
moderation). Only one pack separates the models significantly on accuracy:
`citation-support` (fixed below) and `support-triage` (Sonnet ahead, p=0.012).

## Fixed: citation-support v0.5.0 — coverage was ambiguous

**Finding.** All 22 both-wrong cases were contradictions ("claim: guilty" vs
"quote: acquitted") where gold is `coverage: full` by design (polarity-blind:
the quote addresses the detail) but both models read `coverage` as
*support*-coverage and answered `partial`/`none`. The intended semantics lived
in the pack README, not in the instruction sent to the model.

**Fix.** The `coverage` instruction and level descriptions now state the
polarity-blind rule explicitly. Labels unchanged.

**Verified result.** both-wrong 22 → 0; Jev 0.919 → **0.979**, Sonnet
0.910 → **0.941**; the pack now separates the models (42–12, McNemar
**p < 0.001**, previously p = 0.281). One wording fix removed a systematic
false signal and turned a tie into a real measurement — the flywheel working.

## Remaining clusters (proposals, not yet applied)

### moderation — severity boundaries (12 both-wrong, 91 total disagreements)

`none` / `low` / `medium` are fuzzy for insults and *reporting* threats:
"I will report you to the authorities" → gold `low`, Jev `high`, Sonnet
`none`; "I hope your channel dies" → gold `medium`, Jev `high`, Sonnet `low`;
"Thanks for nothing, genius" → gold `low`, Jev `medium`, Sonnet `none`.

**Proposal.** A severity pass with operational rules, like the urgency pass
that moved triage 0.69 → 0.83: decide explicitly whether *reporting* threats
(platform/employer/authorities) count as `low` (gold says yes), define
`medium` as wishing harm, and make `none` unreachable for directed insults.
Re-label against the new rules, bump the pack, re-record.

### rag-answerability — missing_info kind boundaries (11 both-wrong)

Gold expects `other`/`unknown` where models pick a specific kind
("Which payment methods are accepted?" + "Billing is handled by an external
payment processor" → gold `unknown`, models `other`/`entity`). The
first-matching-kind rule does not settle deferrals that name a source.

**Proposal.** Sharpen the option meanings (the failure is what each kind
*means* when the context defers rather than what is missing), decide the
`other` vs `unknown` boundary with anchors per kind, re-label, re-record.

### support-triage — queue and urgency edges (6 both-wrong, p = 0.012 for the pack)

Queue: "audit log" → gold `other` (models account/technical); "data region"
→ gold `other` (models technical/account); "shipping cost double the rate" →
gold `shipping` (models billing/technical); "trial started on wrong date" →
gold `account` (models unknown/billing). Urgency: "lost my 2FA device" →
gold `high`, models `critical`/`normal`.

**Proposal.** Queue option descriptions need one worked example each (the
boundaries are team-routing conventions, not semantics). For urgency, extend
the critical/high rule with self-inflicted lockouts ("access lost through a
lost/expired device is high, not critical"). This is the one pack where
Sonnet is reliably ahead — worth a careful pass.

### rag-passage-relevance — quality anchors (2 both-wrong)

"Library open Mon–Sat" vs question about Sundays → gold `weak`, models
`strong`/`ok`. Low priority; add one anchor per level if revisited.

### banking-intent — dataset noise (2 both-wrong)

Gold comes from Banking77; confusion between near-synonymous intents is
upstream noise, documented in the pack README. No action.

## Suggested order

1. moderation severity (biggest cluster, highest use)
2. rag-answerability missing_info (option meanings)
3. support-triage queue/urgency (only significant pack gap)
4. rag-passage-quality anchors (optional)

Each pass = criteria wording + gold realignment + re-record (Jev ~$0.02,
Sonnet ~$1) + re-run this harvest; success criterion is both_wrong → 0 and
the pack separating models on merit.
