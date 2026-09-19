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

- Spec v0 + validator + CI + 6 seed packs (50 cases each, all self-authored,
  CC0-1.0): support-triage, rag-passage-relevance, rag-answerability,
  citation-support, moderation, entity-merge.
- All packs `provisional` (`tested: null`, no `evidence.md`) — `jevassert`
  does not exist yet, so no evidence can be recorded. That is the honest state;
  do not set `tested` by hand.
- index.json has a strict invariant: `verified` requires `evidence.md`; CI
  fails otherwise.

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
