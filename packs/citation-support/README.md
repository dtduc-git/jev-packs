# citation-support

Verify that a citation backs the sentence it was attached to. Catches the two
classic generation failures: contradicted quotes and quotes that cover only
part of an overreaching claim.

## Questions

| question | type | labels |
|---|---|---|
| `supports` | noul | true / false |
| `coverage` | score | none, partial, full, unknown |

### Labeling rules

- `supports` is strict: the quote must back **every** assertion in the claim,
  with no stronger wording than the quote allows (no `proves` from
  `associated with`, no `all` from `some`), and no contradiction.
- `coverage` is polarity-blind: how much of the claim's key content appears in
  the quote at all.
  - `full` — every key detail (numbers, names, direction) appears.
  - `partial` — some key details appear; others are absent.
  - `none` — none appear.
  - `unknown` — quote is empty, garbled or redacted beyond use.
- Expected consistency: `supports` is `true` exactly when `coverage` is `full`
  **and** there is no contradiction or overreach. A full-coverage contradiction
  is `supports: false, coverage: full` on purpose — the pair is what tells a
  reviewer whether the generator invented or misread.
- Truth in the world is irrelevant; judge only claim vs quote.

## Provenance

All 50 cases were written for this pack (CC0-1.0). Claims and quotes are
synthetic.

## Thresholds

0.85 on both `supports` labels; 0.7 per coverage level. `unknown` has no floor.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.910**, ECE 0.054,
$0.000017/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
