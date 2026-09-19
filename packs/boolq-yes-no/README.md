# boolq-yes-no

Yes/no reading comprehension over real questions and Wikipedia passages. Tests
whether a decision model actually reads the passage, including the `false`
cases where the passage looks on-topic but does not support a yes.

## Question

| question | type | labels |
|---|---|---|
| `answer_yes` | noul | true / false |

Cases are drawn 75 yes / 75 no. Floors of 0.85 on both labels.

## Provenance

- Source: **BoolQ** — C. Clark et al., *BoolQ: Exploring the Surprising
  Difficulty of Natural Yes/No Questions* (Google, 2019),
  <https://arxiv.org/abs/1905.10044>.
- License: **CC BY-SA 3.0**. This pack is a derived subset and stays under the
  same license — **share-alike applies to these cases**; attribution above.
- Sample: 150 items — 75 `answer: true`, 75 `answer: false` — deterministic via
  `scripts/build-boolq.py` (seed 42). Question and passage are
  whitespace-normalized; no other edits. Gold is the dataset's `answer` field.

Regenerate:
`uv run --no-project --with pyarrow python scripts/build-boolq.py`.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.887**, ECE 0.063,
$0.000018/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
