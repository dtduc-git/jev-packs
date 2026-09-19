# Changelog

Repo-level changes; per-pack history lives in each pack's `CHANGELOG.md`.

## 2026-09-19 (disagreement harvest)

- `scripts/disagreements.py` — harvest case-level disagreements between two
  recorded backends into `review/<a>-vs-<b>/` (three buckets: backend-A-only
  correct, backend-B-only correct, both-wrong) with McNemar p per pack.
- First harvest (Jev 1.13.0 vs Claude Sonnet 5, 6,427 items): 458
  disagreements, 33 both-wrong. Full analysis: `review/FINDINGS.md`.
- **`citation-support` v0.5.0**: the harvest showed all 22 both-wrong cases
  were contradictions double-missed because `coverage`'s polarity-blind rule
  lived only in the README. The instruction now states it. Verified: both-wrong
  22 → 0, Jev 0.919 → 0.979, Sonnet 0.910 → 0.941, and the pack now separates
  the models (McNemar p < 0.001).
- `refresh.py` now also syncs `index.json` `version` with `pack.yaml` when a
  refresh follows a pack bump.
- Remaining clusters (answerability missing_info, triage queue/urgency,
  rag-passage anchors) are proposed in `review/FINDINGS.md`, not yet applied.
- **`moderation` v0.8.0**: severity rules rewritten in two data-checked
  iterations (v0.7.0 fixed reporting threats/mockery but was rejected by a
  46-vs-35 regression comparison; v0.8.0 splits protected-hate, collective
  insults and livelihood threats correctly). Jev 0.906 → 0.917 (p = 0.044),
  ECE 0.027 → 0.013, both-wrong 12 → 7.
- **`rag-answerability` v0.6.0**: `other`/`unknown` boundary defined
  operationally (process deferral vs pointer to where the answer lives).
  Jev 0.908 → 0.930 (p = 0.004), both-wrong 11 → 1. A rejected first rewrite
  (over-using `other`, −0.020) is documented in review/FINDINGS.md.
- **`support-triage` v0.7.0**: queue scopes and recoverable-access urgency
  made explicit. Jev 0.887 → 0.898; Sonnet still leads (p = 0.019), kept
  visible as a model finding.
- **`rag-passage-relevance` v0.5.0**: judge stated, not inferred. Jev
  0.899 → 0.921 (p = 0.0005) and the pack now separates the models (p = 0.041).
- **Totals after five passes**: both-wrong cases 55 → 18 across the matrix.
- `build_scoreboard.py` and `verify_results.py` now mark and skip stale rows
  (result `pack_version` behind the current pack) instead of failing or
  silently mixing versions.

## 2026-09-19 (benchmark)

- **`results/` introduced** — independent benchmark columns recorded on the
  same packs. Additive extension: no pack field or `spec` change; existing
  consumers ignore unknown paths.
- `scripts/record-backend.py` records a backend (TypeSafe API or any LLM via
  TypeSafe's official `system-one-adapter`) and writes
  `results/<backend>/{backend.json,<pack>.json,<pack>.md,<pack>.predictions.jsonl}`.
  Predictions are committed; every published number replays offline
  (`scripts/verify_results.py`).
- `scripts/validate.py` now validates `results/` (structure, prediction hashes,
  recorded models match the recording).
- `scripts/build_scoreboard.py` generates `docs/index.html` (Jev Bench) from
  `results/`; CI fails when it is stale.
- `jevassert` 0.2.0: `record --backend openai|anthropic` (via system-one-adapter),
  `check --input-price/--output-price`, reports the actual recorded models.
- METHODOLOGY.md added — what is measured, backend protocol, caveats, and how
  to contribute a column.

## 2026-09-19

- Initial release: spec v0 ([SPEC.md](SPEC.md)), validator, CI, and six seed
  packs (`support-triage`, `rag-passage-relevance`, `rag-answerability`,
  `citation-support`, `moderation`, `entity-merge`) — all `provisional`.
- Spec v0 clarified to match the jevassert loader: `choice` needs ≥2 options,
  `score` needs 2–10 levels, and `score` questions may carry optional
  `level_descriptions` (label → situational text). Additive; no `spec` bump.
- All six packs recorded against `jev-1.13.0` with jevassert (accuracy
  0.787–0.940, ECE 0.044–0.095, ~$0.00002/case); `evidence.md` +
  `predictions.jsonl` committed, `index.json` flipped to `verified`.
- Pre-evidence quality pass: `level_descriptions` anchors added to all ordinal
  questions; 14 `support-triage` urgency labels realigned to the anchors;
  5 `moderation` unknown cases rewritten as unreadable input. Stability
  spot-check: two independent recordings of `support-triage` were identical
  (0 discordant of 150 items).
- **All packs expanded to 100+ cases (v0.2.0; 605 cases, 1,410 items total)**
  and re-recorded against `jev-1.13.0`: accuracy 0.793–0.905, ECE 0.040–0.088,
  ~$0.00002/case. Larger, harder sets replaced the seed evidence — numbers are
  lower and more trustworthy (e.g. `rag-answerability` 0.940 → 0.905).
- **Packs doubled again to 200+ cases (v0.3.0; 1,210 cases, 2,820 items
  total)** and re-recorded: accuracy 0.795–0.905, ECE 0.032–0.089,
  ~$0.00002/case. Ordinal questions remain the weak spot (`urgency` 0.59,
  `severity` 0.69, `missing_info` 0.82, `quality` 0.82).
- **Packs doubled to 400+ cases (v0.4.0; 2,420 cases, 5,640 items total)**
  and re-recorded: accuracy 0.791–0.919, ECE 0.017–0.095. Citation-support
  climbed to 0.919; triage urgency (0.56), moderation action (0.68) and
  answerability missing-info (0.78) are now the clearest improvement targets.
  Statistical margin at this size: CI95 ≈ ±5pp per question.
- **Dataset-derived packs**: `sms-spam` (SMS Spam Collection, CC BY 4.0;
  0.967), `boolq-yes-no` (BoolQ, CC BY-SA 3.0; 0.887) and `banking-intent`
  (Banking77, CC BY 4.0; 0.853) — 150 cases each, built by reproducible
  `scripts/build-*.py`, raw data never committed.
- **Ordered-rule criteria rewrite (v0.5.0)** for `support-triage` urgency and
  `moderation` action/severity, plus 30 boundary cases each: triage accuracy
  0.797 → 0.843 (`urgency` 0.56 → 0.69), moderation 0.791 → 0.872 (`action`
  0.68 → 0.93). Criteria wording moved the numbers more than 2,420 extra
  cases did.
- **Second criteria pass (v0.5.0/v0.6.0)**: `rag-answerability` 0.861 → 0.908
  (`missing_info` 0.78 → 0.86, McNemar p < 0.0001 — concise-but-sufficient
  rule, cross-question consistency, procedure-vs-availability); `moderation`
  severity criteria tightened, 41 mislabeled complaint cases reclassified
  (`severity` 0.70 → 0.81, overall 0.906).
- **Third pass**: `support-triage` urgency redesigned to three operational
  levels (dropping `low`), 92 labels realigned, 20 boundary cases — accuracy
  0.843 → 0.887 (`urgency` 0.69 → 0.83). `banking-intent` option descriptions
  sharpened (0.840; ±4pp run-to-run noise at n=150). Running total: 9 packs,
  2,990 cases, 6,370 items, all verified against `jev-1.13.0`.
