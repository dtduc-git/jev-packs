# Changelog

Repo-level changes; per-pack history lives in each pack's `CHANGELOG.md`.

## 2026-09-19

- Initial release: spec v0 ([SPEC.md](SPEC.md)), validator, CI, and six seed
  packs (`support-triage`, `rag-passage-relevance`, `rag-answerability`,
  `citation-support`, `moderation`, `entity-merge`) — all `provisional`.
- Spec v0 clarified to match the jevassert loader: `choice` needs ≥2 options,
  `score` needs 2–10 levels, and `score` questions may carry optional
  `level_descriptions` (label → situational text). Additive; no `spec` bump.
