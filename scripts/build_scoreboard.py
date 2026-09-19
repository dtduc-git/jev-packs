#!/usr/bin/env python3
"""Build docs/index.html — the benchmark scoreboard — from results/.

Reads index.json and results/<backend>/<pack>.json (written by
scripts/record-backend.py). Deterministic: same inputs, same HTML.
Use --check in CI to fail when the committed page is stale.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
INDEX = ROOT / "index.json"
OUT = ROOT / "docs" / "index.html"
REPO = "https://github.com/dtduc-git/jev-packs/blob/master"


def load_backends() -> dict[str, dict[str, Any]]:
    backends: dict[str, dict[str, Any]] = {}
    if not RESULTS_DIR.is_dir():
        return backends
    for slug_dir in sorted(p for p in RESULTS_DIR.iterdir() if p.is_dir()):
        meta_path = slug_dir / "backend.json"
        if not meta_path.is_file():
            continue
        backends[slug_dir.name] = json.loads(meta_path.read_text())
    return backends


def load_results() -> dict[str, dict[str, dict[str, Any]]]:
    results: dict[str, dict[str, dict[str, Any]]] = {}
    if not RESULTS_DIR.is_dir():
        return results
    for slug_dir in sorted(p for p in RESULTS_DIR.iterdir() if p.is_dir()):
        for path in sorted(slug_dir.glob("*.json")):
            if path.name == "backend.json":
                continue
            results.setdefault(path.stem, {})[slug_dir.name] = json.loads(path.read_text())
    return results


def money(value: float | None) -> str:
    if value is None:
        return "—"
    if value == 0:
        return "$0"
    return f"${value:.6f}"


def accuracy_cell(result: dict[str, Any], slug: str) -> str:
    accuracy = result.get("accuracy")
    if not isinstance(accuracy, (int, float)) or result.get("n_items", 0) == 0:
        return "—"
    cell = f"<strong>{accuracy:.3f}</strong>"
    ci = result.get("accuracy_ci")
    if isinstance(ci, list) and len(ci) == 2:
        cell += f" <span class='ci'>({ci[0]:.3f}–{ci[1]:.3f})</span>"
    ece = result.get("ece")
    if isinstance(ece, (int, float)):
        cell += f"<br><span class='sub'>ECE {ece:.3f}</span>"
    cell += f"<br><span class='sub'>{money(result.get('cost_per_case_usd'))}/case</span>"
    report = result.get("report") or f"results/{slug}/{result['pack']}.md"
    cell += f"<br><span class='sub'><a href='{REPO}/{html.escape(report)}'>report</a>"
    cell += f" · <a href='{REPO}/results/{slug}/{result['pack']}.json'>json</a></span>"
    return cell


def render() -> str:
    index = json.loads(INDEX.read_text())
    backends = load_backends()
    results = load_results()
    order = [entry["id"] for entry in index["packs"]]
    ordered_slugs = sorted(backends, key=lambda slug: (backends[slug]["provider"] != "typesafe", slug))

    lines: list[str] = []
    lines.append("<!doctype html>")
    lines.append("<html lang='en'><head><meta charset='utf-8'>")
    lines.append("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    lines.append("<title>Jev Bench — independent results for Jev-compatible decision backends</title>")
    lines.append("<style>")
    lines.append(
        "body{font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;"
        "max-width:1100px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}"
        "h1{margin-bottom:.2rem}h2{margin-top:2.2rem;border-bottom:1px solid #ddd;padding-bottom:.3rem}"
        "a{color:#0b5cad;text-decoration:none}a:hover{text-decoration:underline}"
        "table{border-collapse:collapse;width:100%;font-size:13.5px}"
        "th,td{border:1px solid #ddd;padding:.45rem .6rem;text-align:left;vertical-align:top}"
        "th{background:#f6f8fa}"
        ".sub{color:#666;font-size:12px}.ci{color:#666;font-size:12px}"
        "code{background:#f3f4f6;padding:.1rem .3rem;border-radius:3px;font-size:13px}"
        ".note{color:#555;font-size:13px}"
        "</style></head><body>")
    lines.append("<h1>Jev Bench</h1>")
    lines.append(
        "<p class='note'>Independent, reproducible results for Jev-compatible decision backends "
        f"on <a href='https://github.com/dtduc-git/jev-packs'>jev-packs</a> golden sets. "
        f"Generated from <code>results/</code> ({html.escape(index.get('updated', ''))}). "
        "Every number replays offline from the committed recordings — see "
        "<a href='https://github.com/dtduc-git/jev-packs/blob/master/METHODOLOGY.md'>METHODOLOGY.md</a>. "
        "Community-run; not affiliated with TypeSafe AI.</p>")

    lines.append("<h2>Results</h2>")
    if not backends:
        lines.append("<p class='note'>No backend results yet — <code>results/</code> is empty.</p>")
    else:
        lines.append("<table><thead><tr><th>pack</th>")
        for slug in ordered_slugs:
            meta = backends[slug]
            lines.append(
                f"<th>{html.escape(meta['name'])}<br><span class='sub'>"
                f"<code>{html.escape(meta['model'])}</code></span></th>"
            )
        lines.append("</tr></thead><tbody>")
        for pack_id in order:
            version = next(e["version"] for e in index["packs"] if e["id"] == pack_id)
            n_items = None
            for slug in ordered_slugs:
                cell = results.get(pack_id, {}).get(slug)
                if cell:
                    n_items = cell.get("n_items", n_items)
            items = f" — {n_items} items" if n_items else ""
            lines.append(
                f"<tr><td><a href='{REPO}/packs/{pack_id}'>{pack_id}</a> "
                f"<span class='sub'>v{version}{items}</span></td>"
            )
            for slug in ordered_slugs:
                cell = results.get(pack_id, {}).get(slug)
                lines.append(f"<td>{accuracy_cell(cell, slug) if cell else '—'}</td>")
            lines.append("</tr>")
        lines.append("</tbody></table>")
        lines.append(
            "<p class='note'>Accuracy over all labeled items with bootstrap 95% CI; "
            "ECE is expected calibration error (lower is better); cost is per case at the "
            "prices in each backend.json. Click through for per-question breakdowns.</p>")

    lines.append("<h2>Backends</h2>")
    lines.append(
        "<table><thead><tr><th>backend</th><th>provider</th><th>model</th><th>license</th>"
        "<th>endpoint</th><th>pricing / MTok</th><th>notes</th></tr></thead><tbody>")
    for slug in ordered_slugs:
        meta = backends[slug]
        pricing = meta.get("pricing_usd_per_mtok", {})
        price = f"in ${pricing.get('input', 0)} · out ${pricing.get('output', 0)}"
        lines.append(
            "<tr>"
            f"<td><code>{html.escape(slug)}</code></td>"
            f"<td>{html.escape(str(meta.get('provider')))}</td>"
            f"<td><code>{html.escape(str(meta.get('model')))}</code></td>"
            f"<td>{html.escape(str(meta.get('license')))}</td>"
            f"<td><code>{html.escape(str(meta.get('endpoint')))}</code></td>"
            f"<td>{html.escape(price)}</td>"
            f"<td>{html.escape(str(meta.get('notes') or ''))}</td>"
            "</tr>")
    lines.append("</tbody></table>")
    lines.append("<p class='note'>Every backend uses the same questions and the same golden cases; "
                 "LLM backends go through TypeSafe's official "
                 "<a href='https://github.com/typesafe-ai/system-one-adapter-python'>system-one-adapter</a> "
                 "with identical settings, so the comparison is like for like.</p>")

    lines.append("<h2>Reproduce</h2>")
    lines.append("<p class='note'>Recording needs the backend's runtime (a local server or API key); "
                 "checking a committed recording is offline, free and deterministic:</p>")
    lines.append("<pre><code>")
    example = "sms-spam"
    lines.append(html.escape(
        f"uvx jevassert check packs/{example} -p results/<backend>/{example}.predictions.jsonl"))
    lines.append("</code></pre>")
    lines.append("<p class='note'>To add a backend, see "
                 "<a href='https://github.com/dtduc-git/jev-packs/blob/master/CONTRIBUTING.md'>CONTRIBUTING.md</a> "
                 "and open a PR with <code>results/&lt;your-backend&gt;/</code>.</p>")

    lines.append("<h2>Files</h2>")
    lines.append("<ul class='note'>")
    lines.append("<li><a href='https://github.com/dtduc-git/jev-packs/blob/master/METHODOLOGY.md'>Methodology</a> — what is measured, how, and the caveats.</li>")
    lines.append("<li><a href='https://github.com/dtduc-git/jev-packs'>jev-packs</a> — the packs and the format.</li>")
    lines.append("<li><a href='https://github.com/dtduc-git/jevassert'>jevassert</a> — the record/replay runner that produces every number.</li>")
    lines.append("</ul>")
    lines.append("</body></html>")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if docs/index.html is stale")
    args = parser.parse_args()

    rendered = render()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != rendered:
            print("docs/index.html is stale — run scripts/build_scoreboard.py", file=sys.stderr)
            return 1
        print("docs/index.html is up to date")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
