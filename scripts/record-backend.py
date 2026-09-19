#!/usr/bin/env python3
"""Record a backend's predictions on jev-packs and write benchmark results.

For each selected pack:
  1. ``jevassert record --backend openai|anthropic`` -> live calls to the
     backend (LLM via system-one-adapter, or TypeSafe API for --backend typesafe)
  2. ``jevassert check --json --report`` -> results/<slug>/<pack>.json + .md
  3. results/<slug>/<pack>.predictions.jsonl -> the raw recording (committed)

``results/<slug>/backend.json`` documents how to reproduce the column.

The backend must be installed in the running environment:
``uv run --no-project --with pyyaml --with '../jevassert[adapter]' python
scripts/record-backend.py ...`` (a server such as Ollama must be reachable for
--backend openai).

Exit codes: 0 all packs recorded and valid, 1 a record/check failed, 2 usage/IO.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
RESULTS_DIR = ROOT / "results"
INDEX = ROOT / "index.json"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
SCHEMA = 0
SETTINGS = {
    "structured_outputs": True,
    "llm_answer_mode": "probabilities",
    "normalize_probabilities": True,
    "n_retry_malformed_structure": 2,
}


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, text=True, **kwargs)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jevassert_version() -> str:
    import jevassert

    return jevassert.__version__


def write_backend_metadata(slug_dir: Path, args: argparse.Namespace, created: str) -> None:
    metadata = {
        "schema": SCHEMA,
        "id": slug_dir.name,
        "name": args.name,
        "provider": args.backend,
        "model": args.model,
        "endpoint": args.base_url or "https://api.typesafe.ai",
        "license": args.license,
        "submitted_by": args.submitted_by,
        "created": created,
        "tool": {"name": "jevassert", "version": jevassert_version()},
        "adapter": "system-one-adapter" if args.backend != "typesafe" else None,
        "settings": SETTINGS if args.backend != "typesafe" else None,
        "pricing_usd_per_mtok": {"input": args.input_price, "output": args.output_price},
        "notes": args.notes,
    }
    path = slug_dir / "backend.json"
    previous = json.loads(path.read_text()) if path.is_file() else {}
    metadata["created"] = previous.get("created", created)
    metadata["updated"] = created
    path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True, help="directory name under results/ (kebab-case)")
    parser.add_argument("--name", required=True, help="human-readable backend name")
    parser.add_argument(
        "--backend",
        default="openai",
        choices=("openai", "anthropic", "bedrock", "typesafe"),
        help="jevassert record backend (default openai = OpenAI-compatible endpoint; "
        "bedrock = Claude via AWS Bedrock with AWS_PROFILE/AWS_REGION)",
    )
    parser.add_argument("--model", required=True, help="model to record (e.g. qwen2.5:7b)")
    parser.add_argument("--base-url", default=None, help="endpoint for --backend openai")
    parser.add_argument("--license", required=True, help="license of the model weights/endpoint")
    parser.add_argument("--packs", default="all", help="comma-separated pack ids, or 'all'")
    parser.add_argument("--limit", type=int, default=None, help="record only the first N cases per pack")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--input-price", type=float, default=0.0, help="USD per million input tokens")
    parser.add_argument("--output-price", type=float, default=0.0, help="USD per million output tokens")
    parser.add_argument("--submitted-by", default="dtduc-git")
    parser.add_argument("--notes", default="")
    parser.add_argument("--force", action="store_true", help="overwrite an existing results/<slug>")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="keep existing recordings and retry only errored/missing cases per pack",
    )
    parser.add_argument("--skip-validate", action="store_true")
    args = parser.parse_args()

    if not SLUG_RE.match(args.slug):
        print(f"--slug must be lowercase letters/digits with - or .: {args.slug!r}", file=sys.stderr)
        return 2

    slug_dir = RESULTS_DIR / args.slug
    if slug_dir.exists() and not (args.force or args.resume):
        print(f"{slug_dir} exists — pass --force to overwrite or --resume to retry errors", file=sys.stderr)
        return 2

    if args.packs == "all":
        pack_ids = sorted(p.name for p in PACKS_DIR.iterdir() if p.is_dir())
    else:
        pack_ids = [item.strip() for item in args.packs.split(",") if item.strip()]
    if not pack_ids:
        print("no packs selected", file=sys.stderr)
        return 2

    slug_dir.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().isoformat()
    recorded: list[str] = []

    for pack_id in pack_ids:
        pack_dir = PACKS_DIR / pack_id
        if not pack_dir.is_dir():
            print(f"unknown pack: {pack_id}", file=sys.stderr)
            return 2
        predictions = slug_dir / f"{pack_id}.predictions.jsonl"

        record_cmd = [
            sys.executable,
            "-m",
            "jevassert",
            "record",
            str(pack_dir),
            "-o",
            str(predictions),
            "--backend",
            args.backend,
            "--model",
            args.model,
            "--concurrency",
            str(args.concurrency),
        ]
        if args.base_url:
            record_cmd += ["--base-url", args.base_url]
        if args.limit:
            record_cmd += ["--limit", str(args.limit)]
        if args.resume:
            record_cmd += ["--resume"]
        record_proc = subprocess.run(record_cmd, text=True)
        if record_proc.returncode == 2:
            print(f"{pack_id}: recording aborted (exit 2 — usage/auth error)", file=sys.stderr)
            return 2
        if record_proc.returncode == 1:
            print(
                f"{pack_id}: warning — some cases errored; they stay visible as case_errors "
                "in the report (re-run with --resume to retry them)",
                file=sys.stderr,
            )

        report = slug_dir / f"{pack_id}.md"
        check_cmd = [
            sys.executable,
            "-m",
            "jevassert",
            "check",
            str(pack_dir),
            "-p",
            str(predictions),
            "--json",
            "--report",
            str(report),
            "--input-price",
            str(args.input_price),
            "--output-price",
            str(args.output_price),
        ]
        check = subprocess.run(check_cmd, text=True, capture_output=True)
        sys.stderr.write(check.stderr)
        if check.returncode == 2:
            return 2
        if check.returncode == 1:
            print(f"{pack_id}: a gate failed — baselines must not ship red", file=sys.stderr)
            return 1
        payload = json.loads(check.stdout)
        payload["pack_version"] = payload.pop("version", None)
        payload.update(
            {
                "backend": args.slug,
                "predictions": str(predictions.relative_to(ROOT)),
                "predictions_sha256": sha256(predictions),
                "recorded_at": today,
            }
        )
        (slug_dir / f"{pack_id}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        recorded.append(pack_id)
        print(f"{pack_id}: recorded with {args.model}")

    write_backend_metadata(slug_dir, args, today)

    if not args.skip_validate:
        try:
            run([sys.executable, str(ROOT / "scripts" / "validate.py")])
            scoreboard = ROOT / "scripts" / "build_scoreboard.py"
            if scoreboard.is_file():
                run([sys.executable, str(scoreboard)])
        except subprocess.CalledProcessError:
            print("validation failed — results written but not consistent", file=sys.stderr)
            return 1

    print(f"results/{args.slug}: {len(recorded)} pack(s) -> {', '.join(recorded)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
