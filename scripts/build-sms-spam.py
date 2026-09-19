#!/usr/bin/env python3
"""Build packs/sms-spam/cases.jsonl from the UCI SMS Spam Collection.

Source: SMS Spam Collection v.1 (Almeida, Gomez Hidalgo, Yamakami), UCI ML
Repository, https://doi.org/10.24432/C5CC84, CC BY 4.0.
Raw data is downloaded to a temp dir and never committed.

Run: python scripts/build-sms-spam.py
"""

from __future__ import annotations

import csv
import io
import json
import random
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
PACK = Path(__file__).resolve().parent.parent / "packs" / "sms-spam"
PER_CLASS = 75
SEED = 42


def fetch() -> list[tuple[str, str]]:
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "sms.zip"
        urllib.request.urlretrieve(URL, archive)
        with zipfile.ZipFile(archive) as zf:
            raw = zf.read("SMSSpamCollection").decode("utf-8")
    rows = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        label, _, text = line.partition("\t")
        rows.append((label.strip(), " ".join(text.split())))
    return rows


def main() -> None:
    rows = fetch()
    rng = random.Random(SEED)
    spam = [r for r in rows if r[0] == "spam"]
    ham = [r for r in rows if r[0] == "ham"]
    picked = rng.sample(spam, min(PER_CLASS, len(spam))) + rng.sample(ham, min(PER_CLASS, len(ham)))
    rng.shuffle(picked)

    cases = []
    for i, (label, text) in enumerate(picked, 1):
        cases.append(
            {
                "id": f"sms-{i:04d}",
                "state": {"message": text},
                "expect": {"spam": label == "spam"},
            }
        )
    PACK.mkdir(parents=True, exist_ok=True)
    out = PACK / "cases.jsonl"
    out.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in cases) + "\n")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()
