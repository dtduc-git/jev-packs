#!/usr/bin/env python3
"""Harvest case-level disagreements between two recorded backends.

The flywheel tool: every disagreement between two credible backends is a
boundary case worth reviewing. Groups them in three buckets:

  a_only    Jev correct, other wrong   -> review Jev's edge
  b_only    other correct, Jev wrong   -> review the other backend's edge
  both_wrong                           -> the highest-value review pile:
                                          gold may be wrong, or the case is
                                          genuinely ambiguous

Writes ``review/<a>-vs-<b>/<pack>.jsonl`` (one line per disagreeing item,
with both answers, probabilities and the state) and ``summary.json``; prints
a per-pack table with the exact McNemar p-value.

Usage:
  uv run --no-project --with pyyaml --with '../jevassert[adapter]' \\
    python scripts/disagreements.py --a jev-1.13.0 --b claude-sonnet-5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jevassert.compare import compare
from jevassert.metrics import build_items
from jevassert.packs import load_pack
from jevassert.runner import load_predictions

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
RESULTS_DIR = ROOT / "results"


def predictions_for(slug: str, pack_id: str) -> Path:
    """Resolve the committed recording behind results/<slug>/<pack>.json."""
    result_file = RESULTS_DIR / slug / f"{pack_id}.json"
    if not result_file.is_file():
        raise FileNotFoundError(f"no result for backend {slug!r} and pack {pack_id!r}")
    result = json.loads(result_file.read_text())
    return ROOT / str(result["predictions"])


def write_summary(out_dir: Path, summary: dict[str, Any]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", required=True, help="baseline backend slug (the reference)")
    parser.add_argument("--b", required=True, help="candidate backend slug")
    parser.add_argument("--packs", default="all", help="comma-separated pack ids, or 'all'")
    parser.add_argument("--out", default=None, help="output dir (default review/<a>-vs-<b>)")
    parser.add_argument("--intent", action="store_true", help="pretty-print parsed JSON")
    args = parser.parse_args()

    if args.packs == "all":
        pack_ids = sorted(p.name for p in PACKS_DIR.iterdir() if p.is_dir())
    else:
        pack_ids = [item.strip() for item in args.packs.split(",") if item.strip()]

    out_dir = Path(args.out) if args.out else ROOT / "review" / f"{args.a}-vs-{args.b}"
    summary: dict[str, Any] = {"a": args.a, "b": args.b, "packs": {}}
    totals = {"items": 0, "a_only": 0, "b_only": 0, "both_wrong": 0, "missing_b": 0}

    print(f"{'pack':24} {'n':>5} {'acc A':>6} {'acc B':>6} {'A-only':>6} {'B-only':>6} {'both-w':>6} {'p':>7}")
    for pack_id in pack_ids:
        pack = load_pack(PACKS_DIR / pack_id)
        try:
            a_path = predictions_for(args.a, pack_id)
            b_path = predictions_for(args.b, pack_id)
        except FileNotFoundError as exc:
            print(f"{pack_id:24} skipped: {exc}")
            continue
        a_pred, b_pred = load_predictions(a_path), load_predictions(b_path)
        result = compare(pack, a_pred, b_pred)
        items_a, _, _ = build_items(pack, a_pred)
        items_b, _, _ = build_items(pack, b_pred)
        by_b = {(item.case_id, item.qid): item for item in items_b}
        states = {case.id: case.state for case in pack.cases}

        disagreements: list[dict[str, Any]] = []
        missing_b = 0
        for item in items_a:
            other = by_b.get((item.case_id, item.qid))
            if other is None:
                missing_b += 1
                continue
            if item.got == other.got:
                continue
            kind = (
                "a_only" if item.correct and not other.correct
                else "b_only" if other.correct and not item.correct
                else "both_wrong"
            )
            disagreements.append(
                {
                    "case_id": item.case_id,
                    "qid": item.qid,
                    "kind": kind,
                    "expected": item.expected,
                    "a": {"answer": item.got, "p": round(item.decision_prob, 4)},
                    "b": {"answer": other.got, "p": round(other.decision_prob, 4)},
                    "state": states[item.case_id],
                }
            )

        counts = {kind: sum(1 for d in disagreements if d["kind"] == kind) for kind in ("a_only", "b_only", "both_wrong")}
        out_dir.mkdir(parents=True, exist_ok=True)
        with (out_dir / f"{pack_id}.jsonl").open("w", encoding="utf-8") as handle:
            for row in disagreements:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

        summary["packs"][pack_id] = {
            "n_items": result.n_items,
            "accuracy_a": result.accuracy_a,
            "accuracy_b": result.accuracy_b,
            "a_only": result.wins,
            "b_only": result.losses,
            "both_wrong": counts["both_wrong"],
            "missing_b": missing_b,
            "mcnemar_p": result.p_value,
            "disagreement_file": str((out_dir / f"{pack_id}.jsonl").relative_to(ROOT)),
        }
        for key in ("items", "a_only", "b_only", "both_wrong", "missing_b"):
            if key == "items":
                totals["items"] += result.n_items
            else:
                totals[key] += summary["packs"][pack_id][key]
        print(
            f"{pack_id:24} {result.n_items:>5} {result.accuracy_a:>6.3f} {result.accuracy_b:>6.3f} "
            f"{result.wins:>6} {result.losses:>6} {counts['both_wrong']:>6} {result.p_value:>7.3f}"
        )

    summary["totals"] = totals
    write_summary(out_dir, summary)
    print()
    print(f"totals: {totals}")
    print(f"written: {out_dir.relative_to(ROOT)}/  (per-pack jsonl + summary.json)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
