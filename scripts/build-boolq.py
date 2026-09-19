#!/usr/bin/env python3
"""Build packs/boolq-yes-no/cases.jsonl from BoolQ.

Source: BoolQ (Clark et al., Google), https://arxiv.org/abs/1905.10044,
CC BY-SA 3.0. Raw parquet is streamed to a temp dir and never committed.

Run: uv run --no-project --with pyarrow python scripts/build-boolq.py
"""

from __future__ import annotations

import io
import json
import random
import tempfile
import urllib.request
from pathlib import Path

PARQUET = "https://huggingface.co/api/datasets/google/boolq/parquet/default/train/0.parquet"
PACK = Path(__file__).resolve().parent.parent / "packs" / "boolq-yes-no"
PER_LABEL = 75
SEED = 42


def fetch(limit: int) -> list[dict]:
    import pyarrow.parquet as pq

    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "train.parquet"
        urllib.request.urlretrieve(PARQUET, archive)
        table = pq.read_table(archive, columns=["question", "passage", "answer"]).slice(0, limit * 20)
    return table.to_pylist()


def main() -> None:
    rows = [r for r in fetch(PER_LABEL) if r.get("answer") is not None]
    rng = random.Random(SEED)
    yes = [r for r in rows if r["answer"] is True]
    no = [r for r in rows if r["answer"] is False]
    picked = rng.sample(yes, PER_LABEL) + rng.sample(no, PER_LABEL)
    rng.shuffle(picked)

    cases = [
        {
            "id": f"bq-{i:04d}",
            "state": {
                "question": " ".join(r["question"].split()),
                "passage": " ".join(r["passage"].split()),
            },
            "expect": {"answer_yes": bool(r["answer"])},
        }
        for i, r in enumerate(picked, 1)
    ]
    PACK.mkdir(parents=True, exist_ok=True)
    out = PACK / "cases.jsonl"
    out.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in cases) + "\n")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()
