#!/usr/bin/env python3
"""Replay every committed benchmark result and fail if a report drifted.

For each results/<backend>/<pack>.json, re-runs ``jevassert check`` offline on
the committed recording with the backend's declared pricing and diffs the
regenerated report against results/<backend>/<pack>.md. Requires the
``jevassert`` CLI on PATH (same version series that recorded the results).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
INDEX = ROOT / "index.json"


def current_versions() -> dict[str, str]:
    index = json.loads(INDEX.read_text())
    return {entry["id"]: entry["version"] for entry in index["packs"]}


def gate_free_pack(pack: str, tmp: str) -> Path:
    """A view of the pack without gates.yaml.

    Gates are the reference recording's contract; benchmark replays of other
    backends must reproduce their reports without being judged by it.
    """
    dst = Path(tmp) / pack  # jevassert requires id == directory name
    if not dst.exists():
        dst.mkdir()
        for item in (ROOT / "packs" / pack).iterdir():
            if item.name != "gates.yaml":
                (dst / item.name).symlink_to(item)
    return dst


def main() -> int:
    if not RESULTS_DIR.is_dir():
        print("no results/ directory — nothing to verify")
        return 0
    versions = current_versions()
    failures: list[str] = []
    checked = skipped = 0
    with tempfile.TemporaryDirectory() as tmp:
        for backend_dir in sorted(p for p in RESULTS_DIR.iterdir() if p.is_dir()):
            backend = json.loads((backend_dir / "backend.json").read_text())
            pricing = backend.get("pricing_usd_per_mtok", {})
            for result_path in sorted(backend_dir.glob("*.json")):
                if result_path.name == "backend.json":
                    continue
                result = json.loads(result_path.read_text())
                pack = result["pack"]
                if result.get("pack_version") and result["pack_version"] != versions.get(pack):
                    print(
                        f"skip {backend_dir.name}/{pack}: recorded on pack "
                        f"v{result['pack_version']}, now v{versions.get(pack)} (stale history)"
                    )
                    skipped += 1
                    continue
                predictions = ROOT / result["predictions"]
                report = (
                    ROOT / str(result["report"])
                    if result.get("report")
                    else backend_dir / f"{pack}.md"
                )
                regenerated = Path(tmp) / f"{backend_dir.name}-{pack}.md"
                # The reference backend's report IS the pack's evidence.md, so
                # it must see gates.yaml; other backends replay gate-free.
                pack_dir = (
                    ROOT / "packs" / pack
                    if result.get("report")
                    else gate_free_pack(pack, tmp)
                )
                cmd = [
                    "jevassert",
                    "check",
                    str(pack_dir),
                    "-p",
                    str(predictions),
                    "--report",
                    str(regenerated),
                    "--input-price",
                    str(pricing.get("input", 0.0)),
                    "--output-price",
                    str(pricing.get("output", 0.0)),
                ]
                print("$ " + " ".join(cmd), flush=True)
                completed = subprocess.run(cmd, text=True, capture_output=True)
                if completed.returncode != 0:
                    failures.append(f"{backend_dir.name}/{pack}: check exited {completed.returncode}")
                    continue
                if regenerated.read_text(encoding="utf-8") != report.read_text(encoding="utf-8"):
                    failures.append(
                        f"{backend_dir.name}/{pack}: report is stale — re-record with scripts/record-backend.py"
                    )
                checked += 1

    if failures:
        for failure in failures:
            print(f"ERROR {failure}", file=sys.stderr)
        return 1
    print(f"OK: {checked} result report(s) reproduce" + (f", {skipped} stale skipped" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
