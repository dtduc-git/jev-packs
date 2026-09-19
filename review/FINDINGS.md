# Disagreement harvest — Jev 1.13.0 vs Claude Sonnet 5 (2026-09-19)

Tool: `scripts/disagreements.py`. Raw dumps: `review/<a>-vs-<b>/<pack>.jsonl`
(gitignored); machine summary: `summary.json` next to this file.

6427 items, 445 case-level disagreements (6.9%): 222 Jev-only correct,
205 Sonnet-only correct, 18 both-wrong, 3 missing (one Sonnet case error on
moderation). After five criteria passes: Jev ahead on `citation-support`
(p < 0.001) and `rag-passage-relevance` (p = 0.041); Sonnet ahead on
`support-triage` (p = 0.019); six packs tie. Both-wrong went 55 → 18.

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

## Fixed: rag-answerability v0.6.0 — missing_info other/unknown boundary

**Finding.** All 11 both-wrong cases sat on `other` vs `unknown` and on
specific kinds: gold says "process/review/varies with no source" = `unknown`
(e.g. "Billing is handled by an external payment processor") while "points to
where the answer lives or gives a related fact" = `other` (e.g. "the license
terms are in the EULA"). Neither model could see the rule; `other` had no
operational definition at all.

**Iterations.** The first rewrite lured both models into over-using `other`
(Jev −0.020 with 44 regressions). The second states that the *missing
element* decides the kind and prefaces the ordered list, so specific kinds win
whenever they fit.

**Verified result.** Jev 0.908 → **0.930** (p = 0.004), both-wrong 11 → 1;
Sonnet 0.927, tie (p = 0.894).

## Fixed: support-triage v0.7.0 — queue scope and recoverable access

**Finding.** Sonnet led 54–30 (p = 0.012): Jev sent account-flavoured
requests (data export, notification settings, project transfers) to
`technical`, pre-sales/compliance to `technical` where gold says `other`, and
over-escalated recoverable access loss ("reset my password", "restore my
project") to `critical`.

**Fix.** Queue options carry their scope (account = user/workspace/team/
settings/data export; other = pre-sales, evaluations, compliance checks);
urgency states recoverable access is `high`, not `critical`; refunds include
charge reversals.

**Verified result.** Jev 0.887 → 0.898 (p = 0.093); both-wrong 6 → 5. Sonnet
also improved (0.905 → 0.913) and still leads (p = 0.019): the remaining gap
is real model behaviour on routing conventions, not a data defect — leave it
visible rather than tune until it flatters Jev.

## Fixed: rag-passage-relevance v0.5.0 — stated vs inferred

**Finding.** The two both-wrong cases were inference traps ("library open
Mon–Sat" for a Sunday question; "password printed on the router" for a
how-to-join question): the asked fact is never stated, only related facts
that let a human infer. Models rated them `ok`/`strong`.

**Fix.** Judge what the passage states, not what can be inferred; `weak`
anchor now says "asked fact not stated"; `ok` names its usable pieces.

**Verified result.** Jev 0.899 → **0.921** (p = 0.0005), and the pack now
separates the models in Jev's favour (0.921 vs 0.899, p = 0.041).

## Remaining ideas

- `banking-intent` (2 both-wrong): upstream Banking77 label noise between
  near-synonymous intents; documented in the pack README, no action.
- `support-triage`: Sonnet's genuine lead (p = 0.019) — keep as a finding;
  a further pass should start from the remaining 47 Sonnet-only cases and
  only if policy (not wording) can be made clearer.
- The next frontier of resolution is harder cases, not more backends: sample
  disagreements with p < 0.7, label them by hand, and add them as a pack
  version once the budget allows another recording round.

