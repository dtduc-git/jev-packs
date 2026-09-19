# jev-packs — agent notes

## What this is

Evidence-gated registry of Jev question packs: canonical pack format spec v0,
curated question sets with golden cases, and `index.json`. No code ships from
this repo except the CI validator.

- GitHub: https://github.com/dtduc-git/jev-packs
- Suite: `jevassert` (runner, owns loader + gates) → **jev-packs** (data +
  spec) → `jev-table` (app).
- The canonical spec is [SPEC.md](SPEC.md); `ideas/jev-packs.md` in the private
  brainstorm repo is the strategy doc and must stay in sync with SPEC.md.

## Current state (2026-09-19)

- Spec v0 + validator + CI + 6 seed packs (50–55 cases each, self-authored,
  CC0-1.0): support-triage, rag-passage-relevance, rag-answerability,
  citation-support, moderation, entity-merge.
- **9 packs · 2,990 cases / 6,370 items, all `verified` against `jev-1.13.0`**
  (accuracy 0.840–0.967, ECE 0.017–0.090). Six hand-written packs (support-triage
  v0.6.0 three-level urgency, moderation v0.6.0, rag-answerability v0.5.0 with
  ordered-rule criteria) plus three dataset-derived packs (sms-spam, banking-intent,
  boolq-yes-no v0.1.0). Each pack has `tested`, `evidence.md` and
  `predictions.jsonl`.
- Stability spot-check: `support-triage` recorded twice, identical (0/150
  discordant). Full `--repeat` stability runs are P1.
- No gates.yaml yet — packs pass no declared minimum. Add gates from measured
  baselines when the numbers are stable enough to gate (see Next steps).
- Recordings are single-run; re-record with
  `uvx jevassert record packs/<id> -o /tmp/p.jsonl` (needs `TYPESAFE_API_KEY`)
  then regenerate `evidence.md` with `check --report`.

## Layout

- `packs/<id>/pack.yaml` — questions (noul | choice | score) + thresholds.
- `packs/<id>/cases.jsonl` — golden cases; `expect` covers every question.
- `packs/<id>/README.md` — purpose, provenance, rationale.
- `scripts/validate.py` — the only executable; stdlib + PyYAML.
- `index.json` — registry listing; must exactly match `packs/`.

## Conventions

- Verify before claiming done:
  `uv run --no-project --with pyyaml python scripts/validate.py`
- Every Choice/Score closed set must include `unknown` (Jev cannot abstain).
- Gold labels come from the state alone; no outside context.
- Never hand-edit `evidence.md` or set `tested` without a real jevassert run.
- Cases stay CC0; dataset-derived packs keep upstream license + attribution.
- Keep pack ids stable once listed; breaking question changes bump the pack
  minor version and are noted in its CHANGELOG.

## Next steps

- Gates: add `gates.yaml` per pack from the recorded baselines (e.g.
  `min_accuracy`, `max_ece`, `max_cost_per_case_usd`) once another recording
  confirms stability, so CI can fail on regressions.
- When `jevassert` is published: add an evidence workflow
  (`workflow_dispatch`) that runs `jevassert record`, regenerates `evidence.md`,
  flips `index.json` to `verified`, and opens a PR (never pushes to master).
- Then: scheduled re-record on new Jev versions → publish the pack × version
  table (content flywheel).
- Candidate pack 7: table column recipes for jev-table (spec reuse, needs
  cases before listing).
- Dataset-derived packs (SMS Spam, BoolQ, AG News, banking77) are P1 — only
  with `scripts/build-*.py` provenance and license checks.
- No external promotion without explicit user approval; directory listings and
  repo docs only.
