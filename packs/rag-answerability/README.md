# rag-answerability

Guard against answering from insufficient context, and say what is missing.
Pairs with `rag-passage-relevance`: relevance filters passages, answerability
decides whether the surviving context is enough.

## Questions

| question | type | labels |
|---|---|---|
| `answerable` | noul | true / false |
| `missing_info` | choice | none, entity, date, number, procedure, other, unknown |

### Labeling rules

- `answerable` is **complete answerability**: every part of the question can be
  answered from `context` alone, with no outside knowledge and no guessing.
- Expected consistency: `answerable` is `true` exactly when `missing_info` is
  `none`.
- `missing_info` classifies the first blocking gap, not every gap:
  - `entity` — who/which/where: a named person, company, product or place.
  - `date` — when/how long: a date, deadline, duration or period.
  - `number` — how much/many: a quantity, price, rate or count.
  - `procedure` — how: steps, conditions or rules (context says something
    exists but not how to do it).
  - `other` — real gaps that fit none of the above (e.g. encryption at rest vs
    in transit, policy questions).
  - `unknown` — the context is too vague to say what is missing.
- Context is exactly what retrieval returned; a question answerable only with
  world knowledge is `false`.

## Provenance

All 100 cases were written for this pack (CC0-1.0). Contexts are synthetic.

## Thresholds

0.85 on both `answerable` labels: a false `true` means answering from thin air,
the worst RAG failure. 0.7+ per missing-info class; `unknown` has no floor.

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.905**, ECE 0.040,
$0.000020/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
