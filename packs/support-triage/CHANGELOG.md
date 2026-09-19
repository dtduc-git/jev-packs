# Changelog

## 0.6.0 — 2026-09-19

- `urgency` redesigned to three operational levels (`normal`, `high`,
  `critical`; `low` removed — feedback has the same operational urgency as a
  request). `high` now covers anything not working/failing/delayed/missing or
  costing money (bugs, delivery problems, stuck requests, refunds); `critical`
  is complete unavailability, active data loss or a live security incident.
  92 gold labels realigned to the new rule, 20 boundary cases added; evidence
  re-recorded: accuracy 0.843 → 0.887 (`urgency` 0.69 → 0.83).

## 0.5.0 — 2026-09-19

- `urgency` criteria rewritten as an ordered decision rule (ongoing
  outage/data loss/security incident → critical; blocked/access lost/money at
  stake → high, explicit refunds count; standard → normal; feedback/presales →
  low). Added 30 boundary cases (tone-only "urgent", veiled impact, active
  billing errors, live security incidents); evidence re-recorded.

## 0.4.0 — 2026-09-19

- Doubled from 200 to 400 cases; evidence re-recorded.

## 0.3.0 — 2026-09-19

- Expanded from 100 to 200 cases; evidence re-recorded.

## 0.2.0 — 2026-09-19

- Expanded from 50 to 100 cases (harder intents, multi-intent messages, unreadable edge cases); evidence re-recorded.

## 0.1.0 — 2026-09-19

- Initial pack: 50 cases; `refund_request`, `queue`, `urgency`.
- Pre-evidence revision: added `level_descriptions` anchors for `urgency` and
  realigned 14 gold labels to the anchors (access lost / money at stake →
  high; standard requests → normal; ongoing data loss → critical).
- Evidence recorded against `jev-1.13.0`: accuracy 0.840, ECE 0.062.
