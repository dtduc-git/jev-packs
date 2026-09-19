# Changelog

## 0.8.0 — 2026-09-19

- Second wording iteration after v0.7.0's data check: v0.7.0 fixed reporting
  threats and mockery but over-broadened `low`, so protected-group hate fell
  from `high` to `medium` (46 regressions vs 35 improvements on Jev). v0.8.0
  splits the tiers by policy: criminalizing/dehumanizing/exclusionary
  protected-group statements and threats against a person **or their
  livelihood** = `high`; harsh insults and hostile dismissals of the
  reader/author/a collective, stereotypes, spam, "wish the brand fails" =
  `medium`; profanity, light mockery, third-party and role insults, reporting
  threats = `low`. Jev 0.906 → 0.917 (p = 0.044 vs v0.6.0), ECE 0.027 → 0.013,
  both-wrong cases 12 → 7. No labels changed.

## 0.7.0 — 2026-09-19

- `severity` operational rules rewritten after a Jev-vs-Claude disagreement
  harvest found the wording contradicted the labels: the old rule sent every
  targeted insult to `medium`, but the labels (and reviewers) treat mild
  mockery, sarcasm, third-party insults and **reporting threats** ("I will
  report you") as `low`. Wishes that a channel/brand/project fail are now
  explicitly `medium`; wishes of serious harm to a person stay `high`.
  No labels changed — the rule now says what the pack always meant.

## 0.6.0 — 2026-09-19

- 0.6.0: severity criteria tightened (criticism/complaints -> none; unreadable -> unknown); 41 complaint cases reclassified low -> none; 20 boundary cases added; evidence re-recorded.

## 0.5.0 — 2026-09-19

- `action` and `severity` criteria rewritten as ordered decision rules
  (first matching level wins); added 30 boundary cases (veiled threats,
  demeaning generalizations vs simple insults, wishes of harm, self-harm
  instructions); evidence re-recorded.

## 0.4.0 — 2026-09-19

- Doubled from 200 to 400 cases; evidence re-recorded.

## 0.3.0 — 2026-09-19

- Expanded from 100 to 200 cases; evidence re-recorded.

## 0.2.0 — 2026-09-19

- Expanded from 50 to 100 cases; evidence re-recorded.

## 0.1.0 — 2026-09-19

- Initial pack: 50 cases; `action`, `severity`, `targeted_group`.
- Pre-evidence revision: `level_descriptions` anchors for `severity`; the five
  `unknown` cases rewritten as unreadable input (empty, garbled, redacted) —
  the earlier texts were classifiable as allow, not ambiguous.
- Evidence recorded against `jev-1.13.0`: accuracy 0.787, ECE 0.095.
