# Changelog

Repo-level changes; per-pack history lives in each pack's `CHANGELOG.md`.

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
