# Changelog

## 0.5.0 — 2026-09-19

- `coverage` instruction and level descriptions now state the polarity-blind
  rule explicitly ("a quote that states the opposite of a claim detail still
  addresses that detail"). Motivation: a Jev-vs-Claude disagreement harvest
  found all 22 contradiction cases double-missed by both models — they read
  `coverage` as support-coverage. Labels unchanged; the semantics was always
  this, the prompt now says it.

## 0.4.0 — 2026-09-19

- Doubled from 200 to 400 cases; evidence re-recorded.

## 0.3.0 — 2026-09-19

- Expanded from 100 to 200 cases; evidence re-recorded.

## 0.2.0 — 2026-09-19

- Expanded from 50 to 100 cases; evidence re-recorded.

## 0.1.0 — 2026-09-19

- Initial pack: 50 cases; `supports`, `coverage`.
- Pre-evidence revision: `level_descriptions` anchors for `coverage`.
- Evidence recorded against `jev-1.13.0`: accuracy 0.910, ECE 0.054.
