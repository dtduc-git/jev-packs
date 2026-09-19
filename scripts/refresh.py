#!/usr/bin/env python3
"""Re-record selected packs and refresh evidence + registry status.

Used by the "Refresh evidence" workflow (workflow_dispatch) when Jev releases
a new version. Requires ``TYPESAFE_API_KEY`` and the ``jevassert`` CLI on PATH.

Per pack:
  1. ``jevassert record`` -> packs/<id>/predictions.jsonl (live calls)
  2. ``jevassert check``  -> packs/<id>/evidence.md (replay, offline)
  3. set pack.yaml ``tested:`` to the model version the server reported
  4. mark the pack verified in index.json
  5. validate the whole registry

Exit codes: 0 all gates passed, 1 a gate failed, 2 usage/IO error.
The workflow opens a PR with the result; nothing is pushed to master.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
INDEX = ROOT / "index.json"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, text=True)


def load_models(predictions: Path) -> set[str]:
    models: set[str] = set()
    for line in predictions.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if record.get("model"):
            models.add(record["model"])
    return models


def set_tested(pack_file: Path, tested: str) -> None:
    text = pack_file.read_text(encoding="utf-8")
    updated, count = re.subn(r"(?m)^tested:.*$", f"tested: {tested}", text, count=1)
    if count != 1:
        raise RuntimeError(f"{pack_file}: no `tested:` line to update")
    pack_file.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packs", default="all", help="comma-separated pack ids, or 'all'")
    parser.add_argument("--model", default="jev-latest", help="TypeSafe model to record against")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--rpm", type=int, default=0, help="requests per minute cap (0 = none)")
    args = parser.parse_args()

    if args.packs == "all":
        pack_ids = sorted(p.name for p in PACKS_DIR.iterdir() if p.is_dir())
    else:
        pack_ids = [item.strip() for item in args.packs.split(",") if item.strip()]
    if not pack_ids:
        print("no packs selected", file=sys.stderr)
        return 2

    refreshed: list[str] = []
    gate_failures: list[str] = []
    for pack_id in pack_ids:
        pack_dir = PACKS_DIR / pack_id
        if not pack_dir.is_dir():
            print(f"unknown pack: {pack_id}", file=sys.stderr)
            return 2

        record_cmd = [
            "jevassert",
            "record",
            str(pack_dir),
            "-o",
            str(pack_dir / "predictions.jsonl"),
            "--model",
            args.model,
            "--concurrency",
            str(args.concurrency),
        ]
        if args.rpm:
            record_cmd += ["--rpm", str(args.rpm)]
        run(record_cmd)

        models = load_models(pack_dir / "predictions.jsonl")
        if len(models) != 1:
            print(f"{pack_id}: expected exactly one recorded model, got {sorted(models)}", file=sys.stderr)
            return 2
        recorded = models.pop()

        check = subprocess.run(
            [
                "jevassert",
                "check",
                str(pack_dir),
                "-p",
                str(pack_dir / "predictions.jsonl"),
                "--report",
                str(pack_dir / "evidence.md"),
            ],
            text=True,
            capture_output=True,
        )
        sys.stdout.write(check.stdout)
        if check.returncode == 2:
            print(check.stderr, file=sys.stderr)
            return 2
        if check.returncode == 1:
            gate_failures.append(pack_id)

        set_tested(pack_dir / "pack.yaml", recorded)
        refreshed.append(pack_id)
        print(f"{pack_id}: recorded {recorded}, gates {'PASS' if check.returncode == 0 else 'FAIL'}")

    index = json.loads(INDEX.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in index["packs"]}
    for pack_id in refreshed:
        entries[pack_id]["status"] = "verified"
        entries[pack_id]["evidence"] = f"packs/{pack_id}/evidence.md"
    index["updated"] = dt.date.today().isoformat()
    INDEX.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    run([sys.executable, str(ROOT / "scripts" / "validate.py")])
    print("refreshed: " + ", ".join(refreshed))
    if gate_failures:
        print("gate failures: " + ", ".join(gate_failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
