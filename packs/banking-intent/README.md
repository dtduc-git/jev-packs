# banking-intent

Route real retail-banking support questions to one of 15 fine-grained intents.
Unlike the hand-written packs, these labels come from a published benchmark —
useful as an external yardstick for routing quality.

## Question

| question | type | labels |
|---|---|---|
| `intent` | choice | 15 banking77 intents + `unknown` |

Cases are genuine customer phrasings for one of the 15 intents, 10 per intent
(150 total, balanced by construction). Gold is the dataset's own annotation.
Floors are 0.7 per intent; anything less routes to review.

## Provenance

- Source: **Banking77** — I. Casanueva et al., *Efficient Intent Detection
  with Dual Sentence Encoders* (PolyAI, 2020),
  <https://arxiv.org/abs/2003.04807>. Data:
  <https://github.com/PolyAI-LDN/task-specific-datasets>.
- License: **CC BY 4.0**. This pack is a derived subset; attribution above.
- Sample: 15 of the 77 intents (chosen for practical routing coverage), 10
  cases each, deterministic via `scripts/build-banking-intent.py` (seed 42).
  Messages are whitespace-normalized; no other edits.

Regenerate: `python scripts/build-banking-intent.py`.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.840**, ECE 0.090,
$0.000029/case. (150 cases: run-to-run swings of ±4pp are expected; the
confusable trio transfer_timing / transfer_not_received /
balance_not_updated is deliberately kept.) Full report:
[evidence.md](evidence.md); raw recording: [predictions.jsonl](predictions.jsonl).
