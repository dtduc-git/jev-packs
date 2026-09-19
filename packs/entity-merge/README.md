# entity-merge

Decide if two records are the same entity, and route the pair to merge,
keep-separate, or a human curator when the evidence conflicts.

## Questions

| question | type | labels |
|---|---|---|
| `same_entity` | noul | true / false |
| `action` | choice | merge, keep_separate, curator, unknown |

### Labeling rules

- `same_entity` — would a careful data engineer, seeing only these two record
  lines, bet on the same real-world entity? Matching name plus matching key
  facts (city, founding year, registration number, badge number) is `true`;
  a name clash with conflicting key facts is `false`.
- `action` — the pipeline step:
  - `merge` — same entity, facts agree (detail level may differ).
  - `keep_separate` — clearly different entities.
  - `curator` — plausible match but a key fact conflicts, or the records are
    too thin to decide; a human resolves it.
  - `unknown` — the records themselves are unusable.
- Expected consistency: `same_entity: true` pairs with `merge` or `curator`;
  `false` pairs with `keep_separate` or `curator`. Gold uses `curator` — not
  `unknown` — for thin or corrupted records: the pipeline can still ask a human.
- Name variants (abbreviations, `&`/`and`, accented vs plain characters) do not
  make two records different; conflicting identifiers do.

## Provenance

All 105 cases were written for this pack (CC0-1.0). Names and organizations are
fictional.

## Thresholds

0.85 on both `same_entity` labels: a false merge corrupts data silently, so
merge decisions need confidence. 0.8 for `merge`/`keep_separate`, 0.6 for
`curator` (cheap to ask a human).

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.890**, ECE 0.050,
$0.000018/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
