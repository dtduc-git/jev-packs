# Methodology

Jev Bench is an independent, reproducible benchmark of **Jev-compatible
decision backends** on the golden cases in this repository. It is community-run
and not affiliated with TypeSafe AI.

The goal is narrow: anyone can check any backend on identical questions and
identical labels, and anyone can reproduce every published number offline.

## Layout

```
packs/<id>/                   ground truth: questions + labeled cases (SPEC.md)
results/<backend>/backend.json        how to reproduce the column
results/<backend>/<pack>.json         metrics for one (backend, pack) pair
results/<backend>/<pack>.md           human-readable report
results/<backend>/<pack>.predictions.jsonl   the raw recording
```

The scoreboard ([docs/index.html](../docs/index.html)) is generated from
`results/`; CI fails if it is stale. The validator checks structure, that the
predictions file exists, that its SHA-256 matches `predictions_sha256`, and
that `recorded_models` matches the models actually present in the recording.

## What is measured

Per pack, via [`jevassert check`](https://github.com/dtduc-git/jevassert):

- **Accuracy** over every labeled item, overall and per question. `unknown` is
  a normal label — abstention is scored like any other answer.
- **Bootstrap 95% CI** on accuracy (percentile bootstrap, 1000 resamples,
  fixed seed). Packs are 150–450 items; treat differences inside overlapping
  CIs as noise.
- **ECE** (expected calibration error) of the decision probability, equal-mass
  bins. Coarse below a few hundred items.
- **Brier** score for Noul questions, **coverage/precision** curves at
  thresholds, and coverage under the pack author's own floors.
- **Cost per case** — tokens from the recording priced at the list price
  declared in `backend.json` (`pricing_usd_per_mtok`). It excludes retries if
  the provider's SDK does not report them, and excludes hardware/electricity
  for self-hosted backends (recorded as `$0`).
- **Latency** p50/p95 — wall-clock in the recording session, network and queue
  included. Useful for order of magnitude, not a controlled measurement.

We publish one table per pack and **no blended score**: averaging across
unrelated tasks hides exactly the jaggedness a decision benchmark exists to
show.

## Backend protocol

- **TypeSafe Jev**: `jevassert record` against the API, pinned to the exact
  version the server returns (e.g. `jev-1.13.0`). Each version is its own
  backend column; new versions never overwrite old results.
- **LLM backends**: recorded through TypeSafe's official
  [`system-one-adapter`](https://github.com/typesafe-ai/system-one-adapter-python)
  with identical settings for every model: structured outputs, probabilities
  answer mode, probability normalization, two corrective retries on malformed
  output. The prompt scaffolding is the adapter's; it is not tuned per model.
- Questions and cases come from the pack; a backend never sees a case's label.

## Reproducing

Checking a committed recording is offline, free and deterministic:

```sh
uvx jevassert check packs/sms-spam -p results/<backend>/sms-spam.predictions.jsonl \
  --input-price <in> --output-price <out>   # prices from backend.json
```

Re-recording needs the backend itself: a local server (e.g. Ollama), an API
key, or a TypeSafe key. The exact command is in each `backend.json` (fields
`provider`, `model`, `endpoint`) and in the PR that added the column.

## Adding a backend

1. Run `scripts/record-backend.py` (see CONTRIBUTING.md) against a reachable
   endpoint. Start with one pack (`--packs sms-spam`) to validate, then extend
   to the full set.
2. Commit `results/<backend>/` — predictions included. A result without its
   recording is not accepted.
3. State the model license, the endpoint, and honest pricing in
   `backend.json`. Local models are `$0`; hosted models use current list
   prices.
4. Open a PR. CI validates structure and hashes; a maintainer spot-checks the
   recording before merging.

## Harvesting disagreements

Two credible backends disagreeing is the cheapest source of boundary cases:

```sh
uv run --no-project --with pyyaml --with '../jevassert[adapter]' \
  python scripts/disagreements.py --a jev-1.13.0 --b claude-sonnet-5
```

Writes `review/<a>-vs-<b>/<pack>.jsonl` — every disagreeing item with both
answers, probabilities and the state — plus a `summary.json` with McNemar p
per pack, and prints the table. Items fall into three buckets: A-only correct,
B-only correct, both-wrong. The **both-wrong** pile is reviewed first: each
case is either a gold error, a criteria ambiguity, or a genuinely ambiguous
case that should become `unknown`. Fixes that change criteria or labels bump
the pack version and invalidate that pack's rows; re-record the affected
backends and re-run the harvest — success is both-wrong → 0 and the pack
separating models on merit. The first harvest and its outcomes are written up
in `review/FINDINGS.md`.

## Caveats

- Single run per (backend, pack), at the provider's default sampling settings.
  Run-to-run stability is measurable with `jevassert record --repeat N`; a
  column with a stability note says so in its `backend.json`.
- Results are tied to a pack **version** and a model **version**. When either
  moves, the old row is history, not the current claim.
- Small packs mean wide CIs; do not rank backends on fractions of a point.
- The benchmark measures decisions against labels we wrote. Label quality is
  the real ceiling; disputes about a label should become issues against the
  pack, with the case id.

## Changes

Methodology changes are PRs against this file and are called out in
`CHANGELOG.md`.
