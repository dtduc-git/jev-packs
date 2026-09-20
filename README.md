# jev-packs — golden-set benchmark and registry of Jev question packs

Questions-as-data for [Jev](https://docs.typesafe.ai)-compatible decision
endpoints: curated question sets, golden cases, pinned model versions, measured
evidence — and an independent benchmark ([**Jev Bench**](docs/index.html))
scoring several backends on the same ground truth.

A *pack* is a folder: questions in `pack.yaml`, labeled cases in `cases.jsonl`,
and — once measured — an `evidence.md` produced by
[`jevassert`](https://github.com/dtduc-git/jevassert), the record/replay test
runner for Jev. Any Jev-compatible client can load a pack; the canonical loader
is `jevassert.packs`.

> Suite: [`jevassert`](https://github.com/dtduc-git/jevassert) (runner) →
> **`jev-packs`** (data + spec + benchmark) → [`jev-table`](https://github.com/dtduc-git/jev-table) (app).

## Benchmark

Vendor evals are vendor-run. This repo runs the other direction: the same
questions and the same labels, several backends, recorded predictions
committed, every number reproducible offline.

- Results live in [`results/`](results/) — one directory per backend with its
  raw recording, per-pack metrics (accuracy, ECE, cost, latency) and the exact
  command to reproduce the column.
- The scoreboard is [`docs/index.html`](docs/index.html), generated from
  `results/`; CI fails when it is stale.
- Backends so far: `jev-1.13.0` (TypeSafe API), `claude-sonnet-5` (Anthropic
  API) and `qwen2.5-7b-ollama` (local open weights), all through the same
  questions, cases and recording protocol.
- Disagreement harvest → five criteria passes (citation-support v0.5.0,
  moderation v0.8.0, rag-answerability v0.6.0, support-triage v0.7.0,
  rag-passage-relevance v0.5.0) removed systematic gold noise: both-wrong
  cases fell **55 → 18** and Jev gained 0.4–6.0pp on those packs. Latest
  matrix: Jev ahead on `citation-support` (0.979 vs 0.941, p < 0.001) and
  `rag-passage-relevance` (0.921 vs 0.899, p = 0.041); Sonnet ahead on
  `support-triage` (0.913 vs 0.898, p = 0.019); six packs are statistical
  ties. Jev is **better calibrated on 8/9 packs** and **~250× cheaper per
  case** ($0.000014–0.000044 vs ~$0.0036); the local 7B trails far behind
  (0.533–0.813). Numbers in [`results/`](results/); the full flywheel —
  harvest, review, criteria fixes, verification — is written up in
  [review/FINDINGS.md](review/FINDINGS.md).
- Rules, caveats and how to add a backend: [METHODOLOGY.md](METHODOLOGY.md).

## Why a registry

Every Jev cookbook and MCP server ships its own criteria once and never measures
them. Nobody can answer "which question set for support triage is any good, and
on which model version?" This repo is the place that answers with numbers:

- **Evidence-gated** — a pack is only `verified` in `index.json` when
  `jevassert` has recorded accuracy / ECE / cost / latency for it, on a pinned
  Jev version. No numbers, no endorsement.
- **Abstention mandatory** — Jev cannot abstain, so every Choice and Score in
  every pack must offer an `unknown` label. The spec enforces it; CI checks it.
- **Backend-neutral** — packs are plain YAML/JSONL. Jev API, Vercel AI Gateway,
  local replicas — anything Jev-compatible runs them.

## Packs

All nine packs are **verified**: recorded against `jev-1.13.0` with
[`jevassert`](https://github.com/dtduc-git/jevassert). Numbers are single-run
measurements over each pack's golden cases — see each pack's `evidence.md` for
the full report and `predictions.jsonl` for the raw recording.

### Hand-written packs (CC0-1.0)

| Pack | Questions | Items | Accuracy | ECE | Cost/case |
|---|---|---|---|---|---|
| [`citation-support`](packs/citation-support) | supports, coverage | 800 | **0.979** | 0.034 | $0.000019 |
| [`rag-answerability`](packs/rag-answerability) | answerable-from-context, missing info | 840 | **0.930** | 0.027 | $0.000032 |
| [`moderation`](packs/moderation) | action, severity, targeted group | 1,350 | **0.917** | 0.013 | $0.000044 |
| [`rag-passage-relevance`](packs/rag-passage-relevance) | relevance, passage quality | 800 | **0.921** | 0.021 | $0.000020 |
| [`entity-merge`](packs/entity-merge) | same entity?, resolution action | 840 | **0.857** | 0.017 | $0.000018 |
| [`support-triage`](packs/support-triage) | refund intent, queue, urgency | 1,350 | **0.898** | 0.057 | $0.000031 |

### Dataset-derived packs (upstream license, attribution in each README)

| Pack | Source | Items | Accuracy | ECE | Cost/case |
|---|---|---|---|---|---|
| [`sms-spam`](packs/sms-spam) | SMS Spam Collection (CC BY 4.0) | 150 | **0.953** | 0.040 | $0.000014 |
| [`boolq-yes-no`](packs/boolq-yes-no) | BoolQ (CC BY-SA 3.0) | 150 | **0.887** | 0.063 | $0.000018 |
| [`banking-intent`](packs/banking-intent) | Banking77 (CC BY 4.0) | 150 | **0.840** | 0.090 | $0.000029 |

`provisional` = cases are curated but no `jevassert` evidence exists yet;
`verified` requires a recorded `evidence.md`. See [index.json](index.json).

## Format v0

```yaml
# packs/rag-passage-relevance/pack.yaml
spec: 0
id: rag-passage-relevance
version: 0.1.0
license: CC0-1.0
tested: null                 # "jev-<version>" once evidence exists
description: One-line purpose + non-goals.
state:
  description: What the state is and its fields.
  fields: [question, passage]
questions:
  relevant:
    type: noul
    instructions: "Does `passage` contain information that helps answer `question`?"
  quality:
    type: score
    instructions: "..."
    levels: [junk, weak, ok, strong, unknown]
thresholds:
  relevant: {true: 0.85, false: 0.85}
```

```jsonl
# packs/rag-passage-relevance/cases.jsonl
{"id": "rpr-0001", "state": {"question": "...", "passage": "..."}, "expect": {"relevant": true, "quality": "ok"}}
```

Full schema and rules: [SPEC.md](SPEC.md). Writing a pack:
[CONTRIBUTING.md](CONTRIBUTING.md).

## Consuming a pack

```bash
# replay committed evidence offline (deterministic, free)
uvx jevassert check packs/rag-passage-relevance -p packs/rag-passage-relevance/predictions.jsonl

# record fresh predictions for any Jev-compatible endpoint
TYPESAFE_API_KEY=... uvx jevassert record packs/rag-passage-relevance -o new.jsonl
# or, for the same pack against a local Jev-compatible replica:
uvx jevassert record packs/rag-passage-relevance -o new.jsonl --base-url http://localhost:8000
```

Structure is validated in CI by `scripts/validate.py`; any YAML/JSONL parser can
also load a pack.

## Gates

Every pack ships a `gates.yaml` — a quality contract the runner enforces on
every replay (exit 1 when a gate fails). They are derived from the committed
evidence, not hand-tuned, so the contract can only move when a re-record moves
the baseline:

| Gate | Rule |
| --- | --- |
| `min_accuracy` | 95% bootstrap CI lower bound of the recorded baseline, minus 1pp |
| `max_ece` | baseline ECE + 3pp, never below 0.05 |
| `max_cost_per_case_usd` | baseline cost per case × 2 |
| `max_p95_latency_ms` | baseline p95 × 1.5 |

```bash
# the same check CI runs, gates included
uvx jevassert check packs/entity-merge -p packs/entity-merge/predictions.jsonl
```

Re-derive after a re-record with `python scripts/derive_gates.py`, review the
diff, and treat a gate failure as a regression to explain — not a number to
lower.

## Non-goals

- No hosted registry or API — this repo *is* the registry.
- No CLI of its own; the runner is `jevassert`.
- No auto-generated questions, no private/proprietary cases.

## License

[CC0-1.0](LICENSE) for hand-written content (spec, cases, docs). Dataset-derived
packs keep their upstream license — SMS Spam and Banking77 are CC BY 4.0,
BoolQ is CC BY-SA 3.0 (share-alike) — with attribution and a reproducible
`scripts/build-<pack>.py`. Raw source data is never committed.
