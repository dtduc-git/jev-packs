#!/usr/bin/env python3
"""Build packs/banking-intent/cases.jsonl from the Banking77 dataset.

Source: Banking77 (Casanueva et al., PolyAI), https://arxiv.org/abs/2003.04807,
CC BY 4.0. Data: https://github.com/PolyAI-LDN/task-specific-datasets
Raw data is downloaded to a temp dir and never committed.

We keep 15 intents (each self-describing) instead of all 77 and label a
balanced sample, so the pack measures routing on a practical subset.

Run: python scripts/build-banking-intent.py
"""

from __future__ import annotations

import csv
import io
import json
import random
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"
PACK = Path(__file__).resolve().parent.parent / "packs" / "banking-intent"
PER_INTENT = 10
SEED = 42
INTENTS = [
    "card_arrival",
    "card_not_working",
    "lost_or_stolen_card",
    "pending_card_payment",
    "transaction_charged_twice",
    "transfer_timing",
    "transfer_not_received_by_recipient",
    "declined_transfer",
    "topping_up_by_card",
    "exchange_rate",
    "cash_withdrawal_not_recognised",
    "balance_not_updated_after_bank_transfer",
    "pin_blocked",
    "extra_charge_on_statement",
    "request_refund",
]


def fetch() -> list[tuple[str, str]]:
    raw = urllib.request.urlopen(URL).read().decode("utf-8")
    return [(r["text"].strip(), r["category"].strip()) for r in csv.DictReader(io.StringIO(raw))]


def main() -> None:
    rows = fetch()
    rng = random.Random(SEED)
    picked: list[tuple[str, str]] = []
    for intent in INTENTS:
        pool = [text for text, cat in rows if cat == intent]
        if len(pool) < PER_INTENT:
            raise SystemExit(f"intent {intent!r} has only {len(pool)} rows")
        picked += [(text, intent) for text in rng.sample(pool, PER_INTENT)]
    rng.shuffle(picked)

    cases = [
        {
            "id": f"bnk-{i:04d}",
            "state": {"message": text},
            "expect": {"intent": intent},
        }
        for i, (text, intent) in enumerate(picked, 1)
    ]
    PACK.mkdir(parents=True, exist_ok=True)
    out = PACK / "cases.jsonl"
    out.write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in cases) + "\n")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()
