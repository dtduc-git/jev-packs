# Contributing to jev-packs

Packs are data. Contributions are new packs, more/better cases for existing
packs, or spec changes (rare, discussed in an issue first).

## Adding a pack

1. Create `packs/<id>/` with `pack.yaml`, `cases.jsonl`, `README.md`,
   `CHANGELOG.md`. Start from an existing pack — the schema is
   [SPEC.md](SPEC.md).
2. Write 50+ cases: gold labels decided from the state only, hard and realistic
   first, boundary cases included, `unknown` for genuinely ambiguous ones.
   Prefer self-authored cases (CC0). If you derive cases from a public dataset,
   keep its license, attribute it in the pack README, and add a reproducible
   `scripts/build-<id>.py`.
3. Add the entry to `index.json` with `"status": "provisional"`.
4. Run the validator:

   ```bash
   uv run --no-project --with pyyaml python scripts/validate.py
   ```

5. Open a PR. CI runs the validator; a maintainer reviews question wording and
   label quality.

## Question quality bar

- One question, one decision. If an answer depends on two criteria, split it.
- Criteria-first wording: describe what the answer means, never imply it.
- Every Choice/Score includes `unknown` — Jev has no native abstention.
- If a case cannot be labeled from its state, fix the case, not the question.
- Never add a question the state can't answer.

## Adding a benchmark backend

Any reachable backend that can answer SPEC v0 packs is welcome as a results
column — a local open-weight model, a hosted API, a Jev-compatible replica.

1. Record with `jevassert` (see [METHODOLOGY.md](METHODOLOGY.md)). For an
   LLM through the official adapter:

   ```bash
   uv run --no-project --with pyyaml --with '../jevassert[adapter]' \
     python scripts/record-backend.py \
       --slug qwen2.5-7b-ollama \
       --name "Qwen2.5 7B Instruct (Ollama, local)" \
       --backend openai --model qwen2.5:7b \
       --base-url http://localhost:11434/v1 \
       --license Apache-2.0 --packs sms-spam
   ```

2. Commit `results/<slug>/` — including the `.predictions.jsonl` recordings;
   results without recordings are not merged.
3. State honest, current pricing in `backend.json` (`$0` for local models),
   the model license, and any deviation from the standard recording protocol.
4. Run `python scripts/validate.py` and open a PR. CI checks structure, hashes
   and the scoreboard; a maintainer spots-checks a sample of the recording
   against the cases before merging.

## Evidence

Packs stay `provisional` until someone records `evidence.md` with
[`jevassert`](https://github.com/dtduc-git/jevassert) against a live
Jev-compatible endpoint and sets `tested` in `pack.yaml`. Evidence runs are
cheap; a maintainer does this on merge for accepted packs. No evidence, no
`verified` status — that rule is the point of this repo.

## What we don't accept

- Private or production data, even anonymized.
- Auto-generated question sets with no human review.
- Packs without `unknown` labels, or with compound/vague questions.
- Vendor-specific assumptions (any Jev-compatible endpoint must run the pack).
