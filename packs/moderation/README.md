# moderation

Triage user-generated text: act now, flag for a human, or leave it alone — with
a severity grade and a protected-group check.

## Policy assumptions

Labels follow a "standard platform" policy, stated here and encoded as ordered
decision rules in `pack.yaml` (the first matching level wins). This pack is not
legal advice; consumers can fork it with their own policy text.

- `allow` — criticism, profanity not aimed at a person, disagreement, satire
  that no reasonable reader takes as a call to harm. Rudeness alone can still
  be `allow` with `severity: low`.
- `review` — insults toward individuals, harassment without explicit targeting
  of a protected group, commercial spam, ambiguous or veiled threats, coded
  references a human should read in context.
- `remove` — credible threats, calls for violence, doxxing, sextortion,
  scams, hate speech or demeaning generalizations targeting a protected group,
  sexual content involving minors (none in this pack).
- `targeted_group` is `true` only when the demeaning or attacking quality is
  *because of* a protected characteristic. Insults aimed at a person's
  politics, job or behavior are `false` even when harsh.
- `severity`: `none` (criticism, complaints, disagreement), `low` (profanity
  or mild hostility without a target), `medium` (targeted insult/harassment,
  demeaning generalization), `high` (threats or veiled threats, doxxing, hate
  with protected targeting, fraud, wishes of serious harm). Unreadable input,
  and any text whose action is `unknown`, has `severity: unknown`. The
  pack.yaml `level_descriptions` mirror these anchors.
- `unknown` action is for input that cannot be classified at all: empty,
  garbled, redacted or encoding-damaged text. Ambiguity elsewhere resolves to
  `review`, which is what `review` is for.
- Expected consistency: `allow` pairs with `severity: none` or `low`; `remove`
  pairs with `medium` or `high`; `unknown` action pairs with `unknown` severity.

## Provenance

All 400 cases were written for this pack (CC0-1.0). All texts are synthetic;
none quotes a real user or a real slur. Sensitive scenarios are abstracted on
purpose.

## Thresholds

`targeted_group` is the strictest gate (0.9) because a false `true` suppresses
legitimate criticism. `allow`/`remove` need 0.8, `review` 0.6. `unknown` has no
floor.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.906**, ECE 0.027,
$0.000031/case. The 0.6.0 severity rewrite lifted `severity` from 0.70 to
0.81; `action` (0.92) and `targeted_group` (0.99) remain the strong questions.
Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
