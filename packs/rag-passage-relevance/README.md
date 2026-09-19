# rag-passage-relevance

Pass/fail a retrieved passage against a question, plus a usefulness grade. The
binary gate decides whether to keep a passage; the grade decides how to weigh
or truncate it.

## Questions

| question | type | labels |
|---|---|---|
| `relevant` | noul | true / false |
| `quality` | score | junk, weak, ok, strong, unknown |

### Labeling rules

- `relevant` is about usefulness, not topic: a passage that merely shares the
  subject but helps answer nothing is `false`.
- `quality`:
  - `strong` — contains the answer or everything needed to answer.
  - `ok` — contains usable partial information (a piece, a pointer, a range).
  - `weak` — same subject, nothing usable.
  - `junk` — different subject.
  - `unknown` — passage unusable or unreadable (empty, garbled, encoding
    damage), so usefulness cannot be judged.
- Expected consistency: `relevant` is `true` exactly when `quality` is `ok` or
  `strong`. Gold cases include the awkward middle on purpose.
- Labeled from the pair alone; the passage is not assumed to come from any
  particular corpus.

## Provenance

All 400 cases were written for this pack (CC0-1.0). Passages are synthetic and
do not quote any real source.

## Thresholds

0.85 on both `relevant` labels — this gate decides what reaches the generator,
so it is deliberately strict. 0.7 per `quality` level; `unknown` has no floor.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.899**, ECE 0.035,
$0.000018/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
