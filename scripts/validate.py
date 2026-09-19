#!/usr/bin/env python3
"""Validate jev-packs against spec v0 (SPEC.md). CI entry point."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
RESULTS_DIR = ROOT / "results"
INDEX = ROOT / "index.json"
MIN_CASES = 50

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
BACKEND_ID_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
KEY_RE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
TESTED_RE = re.compile(r"^jev-\d+\.\d+\.\d+$")

errors: list[str] = []


def err(path: str, msg: str) -> None:
    errors.append(f"{path}: {msg}")


def check_keys(path: str, obj: dict, required: set[str], allowed: set[str]) -> None:
    for k in required - obj.keys():
        err(path, f"missing required key `{k}`")
    for k in obj.keys() - allowed:
        err(path, f"unexpected key `{k}`")


def validate_pack(pdir: Path) -> dict | None:
    rel = str(pdir.relative_to(ROOT))
    yaml_path = pdir / "pack.yaml"
    cases_path = pdir / "cases.jsonl"
    for name in ("pack.yaml", "cases.jsonl", "README.md", "CHANGELOG.md"):
        if not (pdir / name).is_file():
            err(rel, f"missing {name}")
    if not yaml_path.is_file() or not cases_path.is_file():
        return None

    try:
        pack = yaml.safe_load(yaml_path.read_text())
    except yaml.YAMLError as exc:
        err(rel, f"pack.yaml does not parse: {exc}")
        return None
    if not isinstance(pack, dict):
        err(rel, "pack.yaml must be a mapping")
        return None

    check_keys(
        rel,
        pack,
        {"spec", "id", "version", "license", "tested", "description", "state", "questions"},
        {"spec", "id", "version", "license", "tested", "description", "state", "questions", "thresholds"},
    )
    if pack.get("spec") != 0:
        err(rel, f"spec must be 0, got {pack.get('spec')!r}")
    if pack.get("id") != pdir.name or not ID_RE.match(pdir.name):
        err(rel, f"id must equal kebab-case directory name `{pdir.name}`")
    if not SEMVER_RE.match(str(pack.get("version", ""))):
        err(rel, f"version must be semver, got {pack.get('version')!r}")
    if not isinstance(pack.get("license"), str) or not pack["license"]:
        err(rel, "license must be a non-empty SPDX string")
    if not isinstance(pack.get("description"), str) or not pack["description"].strip():
        err(rel, "description must be a non-empty string")

    tested = pack.get("tested")
    evidence = pdir / "evidence.md"
    if tested is None:
        if evidence.exists():
            err(rel, "evidence.md exists but tested is null — set tested to the recorded model version")
    elif isinstance(tested, str) and TESTED_RE.match(tested):
        if not evidence.is_file():
            err(rel, f"tested is {tested} but evidence.md is missing")
    else:
        err(rel, f"tested must be null or 'jev-<semver>', got {tested!r}")

    state = pack.get("state")
    fields: list[str] = []
    if not isinstance(state, dict):
        err(rel, "state must be a mapping")
    else:
        check_keys(rel, state, {"description", "fields"}, {"description", "fields"})
        fields = state.get("fields") or []
        if not isinstance(fields, list) or not fields or not all(isinstance(f, str) and f for f in fields):
            err(rel, "state.fields must be a non-empty list of field names")
            fields = []
        elif len(set(fields)) != len(fields):
            err(rel, "state.fields contains duplicates")

    questions = pack.get("questions")
    if not isinstance(questions, dict) or not questions:
        err(rel, "questions must be a non-empty mapping")
        return None if errors else pack

    labels: dict[str, set[str]] = {}
    for qid, q in questions.items():
        qpath = f"{rel}/questions/{qid}"
        if not isinstance(qid, str) or not KEY_RE.match(qid):
            err(qpath, f"question id must be a snake_case string (YAML parsed {qid!r}; quote it if it looks like a boolean)")
            continue
        if not isinstance(q, dict):
            err(qpath, "question must be a mapping")
            continue
        qtype = q.get("type")
        if qtype == "noul":
            check_keys(qpath, q, {"type", "instructions"}, {"type", "instructions"})
            labels[qid] = {"true", "false"}
        elif qtype == "choice":
            check_keys(qpath, q, {"type", "instructions", "options"}, {"type", "instructions", "options"})
            options = q.get("options")
            if not isinstance(options, dict) or len(options) < 2:
                err(qpath, "choice requires an options mapping with at least 2 labels")
            else:
                if "unknown" not in options:
                    err(qpath, "choice options must include `unknown` (Jev cannot abstain)")
                for key, meaning in options.items():
                    if not KEY_RE.match(str(key)):
                        err(qpath, f"option key `{key}` must be snake_case")
                    if not isinstance(meaning, str) or not meaning.strip():
                        err(qpath, f"option `{key}` needs a one-line meaning")
                labels[qid] = set(options)
        elif qtype == "score":
            check_keys(qpath, q, {"type", "instructions", "levels"}, {"type", "instructions", "levels", "level_descriptions"})
            levels = q.get("levels")
            if not isinstance(levels, list) or not 2 <= len(levels) <= 10:
                err(qpath, "score requires a levels list of 2-10 labels")
            else:
                if "unknown" not in levels:
                    err(qpath, "score levels must include `unknown` (Jev cannot abstain)")
                for lv in levels:
                    if not isinstance(lv, str) or not KEY_RE.match(lv):
                        err(qpath, f"level `{lv}` must be a snake_case string")
                labels[qid] = set(levels)
                descriptions = q.get("level_descriptions")
                if descriptions is not None:
                    if not isinstance(descriptions, dict):
                        err(qpath, "level_descriptions must be a mapping of level -> text")
                    else:
                        for lv, text in descriptions.items():
                            if lv not in labels[qid]:
                                err(qpath, f"level_descriptions key `{lv}` is not a declared level")
                            if not isinstance(text, str) or not text.strip():
                                err(qpath, f"level_descriptions for `{lv}` must be a non-empty string")
        else:
            err(qpath, f"type must be noul | choice | score, got {qtype!r}")
            continue
        if not isinstance(q.get("instructions"), str) or not q["instructions"].strip():
            err(qpath, "instructions must be a non-empty string")

    thresholds = pack.get("thresholds")
    if thresholds is not None:
        if not isinstance(thresholds, dict):
            err(rel, "thresholds must be a mapping")
        else:
            for qid, floors in thresholds.items():
                tpath = f"{rel}/thresholds/{qid}"
                if qid not in labels:
                    err(tpath, "unknown question")
                    continue
                if not isinstance(floors, dict) or not floors:
                    err(tpath, "must map label -> probability")
                    continue
                for label, p in floors.items():
                    label_key = "true" if label is True else "false" if label is False else str(label)
                    if label_key not in labels[qid]:
                        err(tpath, f"label `{label}` is not a valid answer for `{qid}`")
                    if not isinstance(p, (int, float)) or not (0 < float(p) <= 1):
                        err(tpath, f"threshold for `{label}` must be in (0, 1]")

    seen: set[str] = set()
    n_cases = 0
    for lineno, line in enumerate(cases_path.read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            err(f"{rel}/cases.jsonl:{lineno}", "blank line")
            continue
        n_cases += 1
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            err(f"{rel}/cases.jsonl:{lineno}", f"invalid JSON: {exc}")
            continue
        cpath = f"{rel}/cases.jsonl:{lineno}"
        if not isinstance(case, dict):
            err(cpath, "case must be an object")
            continue
        check_keys(cpath, case, {"id", "state", "expect"}, {"id", "state", "expect"})
        cid = case.get("id")
        if not isinstance(cid, str) or not cid:
            err(cpath, "id must be a non-empty string")
        elif cid in seen:
            err(cpath, f"duplicate id `{cid}`")
        else:
            seen.add(cid)
        cstate = case.get("state")
        if not isinstance(cstate, dict) or set(cstate) != set(fields):
            err(cpath, f"state keys must be exactly {sorted(fields)}, got {sorted(cstate) if isinstance(cstate, dict) else cstate!r}")
        expect = case.get("expect")
        if not isinstance(expect, dict) or set(expect) != set(labels):
            err(cpath, f"expect keys must be exactly {sorted(labels)}")
            expect = {}
        for qid, value in expect.items():
            if qid not in labels:
                continue
            if questions[qid].get("type") == "noul":
                if not isinstance(value, bool):
                    err(cpath, f"`{qid}` expects a boolean, got {value!r}")
            elif value not in labels[qid] or not isinstance(value, str):
                err(cpath, f"`{qid}` expects one of {sorted(labels[qid])}, got {value!r}")
    if n_cases < MIN_CASES:
        err(f"{rel}/cases.jsonl", f"needs at least {MIN_CASES} cases, found {n_cases}")

    return pack


def validate_results(packs: dict[str, dict]) -> int:
    """Validate benchmark results/ (see METHODOLOGY.md). Returns backends checked."""
    if not RESULTS_DIR.is_dir():
        return 0
    backends = 0
    for slug_dir in sorted(p for p in RESULTS_DIR.iterdir() if p.is_dir()):
        rel = str(slug_dir.relative_to(ROOT))
        meta_path = slug_dir / "backend.json"
        if not BACKEND_ID_RE.match(slug_dir.name):
            err(rel, "backend directory name must be lowercase letters/digits with - or . (model names may carry versions)")
        if not meta_path.is_file():
            err(rel, "missing backend.json")
            continue
        try:
            meta = json.loads(meta_path.read_text())
        except json.JSONDecodeError as exc:
            err(f"{rel}/backend.json", f"invalid JSON: {exc}")
            continue
        if not isinstance(meta, dict):
            err(f"{rel}/backend.json", "must be an object")
            continue
        check_keys(
            f"{rel}/backend.json",
            meta,
            {
                "schema", "id", "name", "provider", "model", "endpoint", "license",
                "submitted_by", "created", "updated", "tool", "pricing_usd_per_mtok", "notes",
            },
            {
                "schema", "id", "name", "provider", "model", "endpoint", "license",
                "submitted_by", "created", "updated", "tool", "adapter", "settings",
                "pricing_usd_per_mtok", "notes",
            },
        )
        if meta.get("schema") != 0:
            err(f"{rel}/backend.json", f"schema must be 0, got {meta.get('schema')!r}")
        if meta.get("id") != slug_dir.name:
            err(f"{rel}/backend.json", "id must equal the directory name")
        for key in ("name", "model", "license", "submitted_by", "created"):
            if not isinstance(meta.get(key), str) or not meta[key].strip():
                err(f"{rel}/backend.json", f"`{key}` must be a non-empty string")
        if meta.get("provider") not in ("openai", "anthropic", "bedrock", "typesafe"):
            err(f"{rel}/backend.json", f"provider must be openai | anthropic | bedrock | typesafe, got {meta.get('provider')!r}")
        endpoint = str(meta.get("endpoint") or "")
        if meta.get("provider") != "typesafe" and "typesafe" in endpoint:
            err(f"{rel}/backend.json", "non-typesafe backend must not point at the TypeSafe endpoint")
        if meta.get("provider") == "anthropic" and "anthropic" not in endpoint:
            err(f"{rel}/backend.json", "anthropic backend endpoint should be https://api.anthropic.com")
        if meta.get("provider") == "bedrock" and "bedrock" not in endpoint.lower():
            err(f"{rel}/backend.json", "bedrock backend endpoint should name AWS Bedrock")
        pricing = meta.get("pricing_usd_per_mtok")
        if not isinstance(pricing, dict):
            err(f"{rel}/backend.json", "pricing_usd_per_mtok must be an object")
        else:
            check_keys(f"{rel}/backend.json/pricing", pricing, {"input", "output"}, {"input", "output"})
            for side in ("input", "output"):
                value = pricing.get(side)
                if not isinstance(value, (int, float)) or value < 0:
                    err(f"{rel}/backend.json/pricing", f"`{side}` must be a non-negative number")

        json_files = sorted(slug_dir.glob("*.json"))
        json_files = [p for p in json_files if p.name != "backend.json"]
        if not json_files:
            err(rel, "no pack results — results/<backend>/<pack>.json expected")
        for result_path in json_files:
            rrel = str(result_path.relative_to(ROOT))
            try:
                result = json.loads(result_path.read_text())
            except json.JSONDecodeError as exc:
                err(rrel, f"invalid JSON: {exc}")
                continue
            if not isinstance(result, dict):
                err(rrel, "must be an object")
                continue
            pack_id = result_path.stem
            result_keys = {
                "backend", "pack", "pack_version", "predictions", "predictions_sha256",
                "recorded_models", "n_cases", "n_items", "accuracy", "ece", "recorded_at",
                "record_model", "tested", "accuracy_ci", "ece_ci", "suggestion",
                "mean_decision_prob", "cost_per_case_usd", "total_cost_usd",
                "p50_latency_ms", "p95_latency_ms", "per_question", "coverage",
                "threshold_coverage", "gates", "pricing", "case_errors", "missing_items",
                "report",
            }
            check_keys(
                rrel,
                result,
                {
                    "backend", "pack", "pack_version", "predictions", "predictions_sha256",
                    "recorded_models", "n_cases", "n_items", "accuracy", "ece", "recorded_at",
                },
                result_keys,
            )
            if result.get("backend") != slug_dir.name:
                err(rrel, "backend must match the results/<backend> directory")
            if pack_id not in packs:
                err(rrel, f"pack `{pack_id}` has no directory in packs/")
            predictions = ROOT / str(result.get("predictions"))
            if not predictions.is_file():
                err(rrel, f"predictions file not found: {result.get('predictions')!r}")
                continue
            digest = hashlib.sha256(predictions.read_bytes()).hexdigest()
            if result.get("predictions_sha256") != digest:
                err(rrel, "predictions_sha256 does not match the committed recording")
            models = sorted(
                {
                    record.get("model")
                    for record in (
                        json.loads(line) for line in predictions.read_text().splitlines() if line.strip()
                    )
                    if isinstance(record.get("model"), str)
                }
            )
            if result.get("recorded_models") != models:
                err(rrel, f"recorded_models {result.get('recorded_models')!r} != models in recording {models!r}")
        backends += 1
    return backends


def main() -> int:
    if not PACKS_DIR.is_dir():
        print("no packs/ directory", file=sys.stderr)
        return 1

    packs = {}
    for pdir in sorted(p for p in PACKS_DIR.iterdir() if p.is_dir()):
        pack = validate_pack(pdir)
        if pack:
            packs[pdir.name] = pack

    if not INDEX.is_file():
        err("index.json", "missing")
    else:
        try:
            index = json.loads(INDEX.read_text())
        except json.JSONDecodeError as exc:
            err("index.json", f"invalid JSON: {exc}")
            index = None
        if isinstance(index, dict):
            if index.get("spec") != 0:
                err("index.json", f"spec must be 0, got {index.get('spec')!r}")
            entries = index.get("packs")
            if not isinstance(entries, list):
                err("index.json", "packs must be a list")
                entries = []
            listed: set[str] = set()
            for i, entry in enumerate(entries):
                ipath = f"index.json/packs[{i}]"
                if not isinstance(entry, dict):
                    err(ipath, "entry must be an object")
                    continue
                check_keys(ipath, entry, {"id", "version", "path", "license", "status", "evidence"}, {"id", "version", "path", "license", "status", "evidence"})
                pid = entry.get("id")
                listed.add(pid)
                if pid not in packs:
                    err(ipath, f"id `{pid}` has no directory in packs/")
                    continue
                pack = packs[pid]
                if entry.get("version") != pack.get("version"):
                    err(ipath, f"version {entry.get('version')!r} != pack.yaml {pack.get('version')!r}")
                if entry.get("path") != f"packs/{pid}":
                    err(ipath, f"path must be `packs/{pid}`")
                if entry.get("license") != pack.get("license"):
                    err(ipath, "license must match pack.yaml")
                status = entry.get("status")
                evidence = ROOT / str(entry.get("evidence")) if entry.get("evidence") else None
                if status == "verified":
                    if pack.get("tested") is None or not (PACKS_DIR / pid / "evidence.md").is_file():
                        err(ipath, "status verified requires evidence.md and non-null tested")
                    if not evidence or not evidence.is_file():
                        err(ipath, "status verified requires an evidence path that exists")
                elif status == "provisional":
                    if pack.get("tested") is not None:
                        err(ipath, "status provisional but pack.yaml tested is set — flip to verified")
                else:
                    err(ipath, f"status must be provisional | verified, got {status!r}")
            for pid in sorted(packs.keys() - listed):
                err("index.json", f"pack `{pid}` is not listed")

    backends = validate_results(packs)

    if errors:
        for e in errors:
            print(f"ERROR {e}")
        print(f"\n{len(errors)} error(s), {len(packs)} pack(s), {backends} backend(s) checked")
        return 1
    print(f"OK: {len(packs)} pack(s), {backends} backend(s), all valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
