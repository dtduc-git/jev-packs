"""Derive packs/<id>/gates.yaml from each pack's committed evidence.md.

The gates are a quality contract, not a target: they must pass on the
recorded baseline and fail when a re-record regresses it. Because
`jevassert check` replays committed predictions offline, the metrics are
deterministic — a tight gate cannot flap.

Rules (documented in README, keep in sync):

  min_accuracy            CI lower bound - 1pp (the 95% bootstrap CI of the
                          recorded baseline), rounded down to 2 decimals
  max_ece                 baseline ECE + 3pp, never below 0.05
  max_cost_per_case_usd   baseline cost x 2 (guards a swap to a pricier model)
  max_p95_latency_ms      baseline p95 x 1.5

Usage:  uv run --no-project python scripts/derive_gates.py
"""

from __future__ import annotations

import re
from pathlib import Path

PACKS = Path(__file__).resolve().parent.parent / "packs"

HEADER = """# Quality gates for this pack (format owned by jevassert).
# Derived from evidence.md by scripts/derive_gates.py — re-run after a
# re-record, review the diff, and keep the baseline honest.
"""


def derive(text: str) -> dict[str, float]:
    acc_ci = re.search(r"accuracy CI ([\d.]+)–([\d.]+)", text)
    acc = float(re.search(r"accuracy \*\*([\d.]+)\*\*", text).group(1))
    ece = float(re.search(r"ECE \*\*([\d.]+)\*\*", text).group(1))
    cost = float(re.search(r"cost: \$([\d.]+)/case", text).group(1))
    p95 = float(re.search(r"p95 ([\d]+)ms", text).group(1))
    min_accuracy = round(float(acc_ci.group(1)) - 0.01, 2) if acc_ci else round(acc - 0.05, 2)
    return {
        "min_accuracy": min_accuracy,
        "max_ece": max(0.05, round(ece + 0.03, 2)),
        "max_cost_per_case_usd": round(cost * 2, 6),
        "max_p95_latency_ms": round(p95 * 1.5),
    }


def main() -> None:
    for evidence in sorted(PACKS.glob("*/evidence.md")):
        gates = derive(evidence.read_text(encoding="utf-8"))
        lines = [HEADER]
        for key, value in gates.items():
            lines.append(f"{key}: {value:.6f}\n" if isinstance(value, float) else f"{key}: {value}\n")
        out = evidence.parent / "gates.yaml"
        out.write_text("".join(lines), encoding="utf-8")
        print(f"{out}  {gates}")


if __name__ == "__main__":
    main()
