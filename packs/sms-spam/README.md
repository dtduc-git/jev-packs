# sms-spam

Classic spam/ham classification on real SMS traffic. A high-precision
baseline task: `true` means unsolicited bulk or fraudulent messaging, `false`
means personal or transactional traffic.

## Question

| question | type | labels |
|---|---|---|
| `spam` | noul | true / false |

The `true: 0.9` / `false: 0.9` floors reflect that both errors are expensive
(a filtered bank alert and a delivered scam are equally bad), so low-confidence
items route to review.

## Provenance

- Source: **SMS Spam Collection v.1** — T. A. Almeida, J. M. Gómez Hidalgo,
  A. Yamakami, *Contributions to the Study of SMS Spam Filtering*, UCI Machine
  Learning Repository (2011), <https://doi.org/10.24432/C5CC84>.
- License: **CC BY 4.0**. This pack is a derived subset; attribution above.
- Sample: 150 messages — 75 spam, 75 ham — drawn deterministically by
  `scripts/build-sms-spam.py` (seed 42) from the 5,574-message corpus.
  Messages are whitespace-normalized; no other edits.
- Labels are the corpus's own annotations, not re-labeled here. The corpus is
  from 2011 and stylistically dated; that is part of the point — a stable,
  well-known baseline.

Regenerate: `python scripts/build-sms-spam.py` (raw data stays in a temp dir).

## Evidence

Recorded 2026-09-19 against `jev-1.13.0`: accuracy **0.967**, ECE 0.053,
$0.000014/case. Full report: [evidence.md](evidence.md); raw recording:
[predictions.jsonl](predictions.jsonl).
