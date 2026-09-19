# Disagreement harvest — Jev 1.13.0 vs Claude Sonnet 5 (2026-09-19)

Tool: `scripts/disagreements.py`. Raw dumps: `review/<a>-vs-<b>/<pack>.jsonl`
(gitignored); machine summary: `summary.json` next to this file.

6427 items, 491 case-level disagreements (7.6%): 241 Jev-only correct,
222 Sonnet-only correct, 28 both-wrong, 3 missing (one Sonnet case error on
moderation). Two packs separate the models on accuracy after the fixes below:
`citation-support` (Jev ahead, p < 0.001) and `support-triage` (Sonnet ahead,
p = 0.012).

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

## Fixed: moderation v0.8.0 — severity rules contradicted the labels

**Finding.** All 12 both-wrong cases were `severity`. The rule sent every
targeted insult to `medium`, while the labels (and reviewers) treat sarcasm,
light mockery, third-party/role insults and **reporting threats**
("I will report you") as `low`; protected-group hate and collective insults
had no explicit home either.

**Iterations.** v0.7.0 made reporting threats and mockery explicit but
over-broadened `low` (protected hate dropped high→medium; 46 regressions vs
35 improvements on Jev — data rejected it). v0.8.0 separates the tiers by
policy: criminalizing/dehumanizing/exclusionary protected-group statements and
threats against a person **or their livelihood** = high; harsh insults and
hostile dismissals of the reader/author/collective, stereotypes,
spam, "wish the brand fails" = medium; profanity, light mockery, third-party
and role insults, reporting threats = low; criticism without an insult = none.

**Verified result.** Jev 0.906 → **0.917** (McNemar p = 0.044), ECE
0.027 → **0.013**; both-wrong 12 → 7. Remaining 7 need policy decisions, not
wording: veiled menace with no named act (mod-0050), the gold inconsistency
between "my boss is an idiot" (low) and "whoever wrote this is an absolute
moron" (medium) (mod-0017 vs mod-0133), opinion-vs-hate boundary (mod-0166),
and business threats (mod-0442). **Sonnet's moderation row is stale**
(recorded against v0.7.0); refreshing it needs ~$2 of API credit.

## Remaining clusters (proposals, not yet applied)

### rag-answerability — missing_info kind boundaries (11 both-wrong)

Gold expects `other`/`unknown` where models pick a specific kind
("Which payment methods are accepted?" + "Billing is handled by an external
payment processor" → gold `unknown`, models `other`/`entity`). The
first-matching-kind rule does not settle deferrals that name a source.
Deep-dive: "other" is the catch-all and both models avoid it, preferring a
specific kind; `procedure` is over-applied to any "how does X work" context.

**Proposal (drafted, not applied).** Give each option a one-line
description that defines it *operationally* and states when it wins:
`entity` (a named thing/person/source is missing), `date` (a time, duration
or deadline), `number` (a quantity, cap or price), `procedure` (the steps to
perform an action), `other` (a policy, clause, term or fact that is not
entity/date/number/procedure — the catch-all when the context names a topic
but not the fact), `unknown` (the context only defers — "depends", "varies",
"handled elsewhere" — and even the kind cannot be named). Preview against the
11 both-wrong cases before recording.

### support-triage — queue and urgency edges (6 both-wrong, p = 0.012 for the pack)

Queue: "audit log" → gold `other` (models account/technical); "data region"
→ gold `other` (models technical/account); "shipping cost double the rate" →
gold `shipping` (models billing/technical); "trial started on wrong date" →
gold `account` (models unknown/billing). Urgency: "lost my 2FA device" →
gold `high`, models `critical`/`normal`.

Deep-dive on the 31 Sonnet-only queue wins: Jev sends account-flavoured
requests (data export, notification settings, project transfers, teammate
offboarding) to `technical`, and pre-sales/evaluation questions ("SSO with
Okta, evaluating tools") to `technical` where gold says `other`. Urgency:
Jev over-escalates recoverable access problems ("reset my password", "restore
my project from backup") to `critical`; gold keeps them `high`.

**Proposal (drafted, not applied).** Queue option descriptions with one
worked example each — `account` = user/workspace/team/settings management,
`technical` = product behaviour and how-to, `billing` = invoices, charges and
tax forms, `shipping` = physical delivery, `other` = pre-sales, evaluations
and anything that fits no queue. Urgency: explicit clause that access
problems a support action can restore (password resets, restores from
backup, re-invites) are `high`, not `critical`; `critical` is reserved for
outages and data loss in progress.

### rag-passage-relevance — quality anchors (2 both-wrong)

"Library open Mon–Sat" vs question about Sundays → gold `weak`, models
`strong`/`ok`. Low priority; add one anchor per level if revisited.

### banking-intent — dataset noise (2 both-wrong)

Gold comes from Banking77; confusion between near-synonymous intents is
upstream noise, documented in the pack README. No action.

## Suggested order

1. ~~moderation severity~~ done (v0.8.0; Jev +0.011, both-wrong 12 → 7;
   Sonnet row awaits a ~$2 refresh)
2. rag-answerability missing_info (option meanings)
3. support-triage queue/urgency (only significant pack gap)
4. rag-passage-quality anchors (optional)

Each pass = criteria wording + gold realignment + re-record (Jev ~$0.02,
Sonnet ~$1) + re-run this harvest; success criterion is both_wrong → 0 and
the pack separating models on merit.
