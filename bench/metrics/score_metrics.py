#!/usr/bin/env python3
"""Score FX3 AI metrics without inventing a model tokenizer."""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def utf8_bytes(path: Path) -> int:
    return len(path.read_bytes())


def edit_span(a: str, b: str) -> int:
    """Sum of replace/delete/insert character lengths between two strings."""
    span = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            span += max(i2 - i1, j2 - j1)
        elif tag == "delete":
            span += i2 - i1
        elif tag == "insert":
            span += j2 - j1
    return span


def usage_from_events(events: Path) -> dict[str, int | str]:
    if not events.is_file():
        return {
            "OUTPUT_TOKENS": "NOT_MEASURED",
            "REASONING_TOKENS": "NOT_MEASURED",
            "INPUT_TOKENS": "NOT_MEASURED",
        }
    last = None
    for line in events.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        usage = obj.get("usage")
        if isinstance(usage, dict) and "output_tokens" in usage:
            last = usage
            continue
        for value in obj.values():
            if isinstance(value, dict) and "output_tokens" in value:
                last = value
    if not last:
        return {
            "OUTPUT_TOKENS": "NOT_MEASURED",
            "REASONING_TOKENS": "NOT_MEASURED",
            "INPUT_TOKENS": "NOT_MEASURED",
        }
    return {
        "OUTPUT_TOKENS": int(last.get("output_tokens", 0)),
        "REASONING_TOKENS": int(last.get("reasoning_output_tokens", 0)),
        "INPUT_TOKENS": int(last.get("input_tokens", 0)),
    }


def find_pair(trial: Path, stem: str) -> tuple[Path | None, Path | None]:
    """Return (first, final) source paths for fx3 or python/fl."""
    candidates = [
        (trial / f"first.{stem}", trial / f"final.{stem}"),
        (trial / f"first-input.{stem}", trial / f"final-input.{stem}"),
    ]
    for first, final in candidates:
        if first.is_file() and final.is_file():
            return first, final
    # single final only
    final_only = trial / f"final.{stem}"
    if final_only.is_file():
        return None, final_only
    return None, None


def score_trial(trial: Path) -> dict[str, object]:
    surface = "UNKNOWN"
    first = final = None
    for stem, name in (("fx3", "FX3"), ("py", "PYTHON"), ("fl", "FX_FL")):
        f, g = find_pair(trial, stem)
        if g is not None:
            first, final = f, g
            surface = name
            # prefer fx3 when both exist
            if stem == "fx3":
                break
        if stem == "py":
            f, g = find_pair(trial, "py")
            if g is None:
                # python answers sometimes as .py via answer naming
                for alt in trial.glob("final*.py"):
                    final = alt
                    surface = "PYTHON"
                    firsts = list(trial.glob("first*.py"))
                    first = firsts[0] if firsts else None
                    break

    # python trials in timing experiments use final code without extension pattern
    if final is None:
        for name in ("final.fx3", "final.py", "final.fl", "answer.fx3", "answer.py"):
            p = trial / name
            if p.is_file():
                final = p
                surface = {"final.fx3": "FX3", "answer.fx3": "FX3", "final.py": "PYTHON", "answer.py": "PYTHON", "final.fl": "FX_FL"}[name]
                first_name = name.replace("final", "first").replace("answer", "first")
                # answer -> no first
                fp = trial / first_name if "final" in name else None
                first = fp if fp and fp.is_file() else None
                break

    row: dict[str, object] = {
        "TRIAL": trial.name,
        "SURFACE": surface,
        "OUTPUT_BYTES": utf8_bytes(final) if final else "NOT_MEASURED",
        "FIRST_BYTES": utf8_bytes(first) if first else "NOT_MEASURED",
        "EDIT_SPAN": "NOT_MEASURED",
        "EDIT_LOCALITY": "NOT_MEASURED",
        "CORRECTION_HINT": "NOT_MEASURED",
    }
    row.update(usage_from_events(trial / "ai-events.jsonl"))
    # some trials nest repair events only; also scan *ai-events.jsonl
    if row["OUTPUT_TOKENS"] == "NOT_MEASURED":
        for ev in sorted(trial.glob("*ai-events.jsonl")):
            u = usage_from_events(ev)
            if u["OUTPUT_TOKENS"] != "NOT_MEASURED":
                row.update(u)
                break

    if first is not None and final is not None:
        a = first.read_text(encoding="utf-8")
        b = final.read_text(encoding="utf-8")
        span = edit_span(a, b)
        row["EDIT_SPAN"] = span
        row["EDIT_LOCALITY"] = round(span / max(len(a), 1), 6)
        row["CORRECTION_HINT"] = 0 if a == b else "CHANGED"

    # lowering / first validity hints from logs when present
    first_test = trial / "first-test.result"
    final_test = trial / "final-test.result"
    if first_test.is_file():
        row["FIRST_PASS_HINT"] = first_test.read_text(encoding="utf-8").strip() or "EMPTY"
    else:
        row["FIRST_PASS_HINT"] = "NOT_MEASURED"
    if final_test.is_file():
        row["FINAL_PASS_HINT"] = final_test.read_text(encoding="utf-8").strip() or "EMPTY"
    else:
        row["FINAL_PASS_HINT"] = "NOT_MEASURED"
    return row


def score_baseline() -> list[dict[str, object]]:
    rows = []
    expected = ROOT / "bench" / "expected"
    for fx3 in sorted(expected.glob("case-*.fx3")):
        fl = fx3.with_suffix(".fl")
        if not fl.is_file():
            continue
        b3 = utf8_bytes(fx3)
        bf = utf8_bytes(fl)
        rows.append(
            {
                "CASE": fx3.stem,
                "FX3_BYTES": b3,
                "FX_BYTES": bf,
                "CHAR_REDUCTION_PERCENT": round((bf - b3) / bf * 100, 4) if bf else "NA",
                "OUTPUT_TOKENS": "NOT_MEASURED",
            }
        )
    return rows


def score_experiment(exp: Path) -> list[dict[str, object]]:
    trials_root = exp / "trials"
    if not trials_root.is_dir():
        raise SystemExit(f"no trials/ under {exp}")
    rows = []
    for trial in sorted(p for p in trials_root.iterdir() if p.is_dir()):
        row = score_trial(trial)
        row["EXPERIMENT"] = exp.name
        rows.append(row)
    return rows


def write_tsv(rows: list[dict[str, object]], out: Path | None) -> None:
    if not rows:
        print("NO_ROWS", file=sys.stderr)
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    sink = open(out, "w", encoding="utf-8", newline="") if out else sys.stdout
    close = out is not None
    try:
        w = csv.DictWriter(sink, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    finally:
        if close:
            sink.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p0 = sub.add_parser("baseline", help="score bench/expected FX3 vs FX bytes")
    p0.add_argument("-o", "--output", type=Path)

    p1 = sub.add_parser("trial", help="score one trial directory")
    p1.add_argument("path", type=Path)
    p1.add_argument("-o", "--output", type=Path)

    p2 = sub.add_parser("experiment", help="score all trials under an experiment")
    p2.add_argument("path", type=Path)
    p2.add_argument("-o", "--output", type=Path)

    args = ap.parse_args()
    if args.cmd == "baseline":
        rows = score_baseline()
    elif args.cmd == "trial":
        rows = [score_trial(args.path)]
    else:
        rows = score_experiment(args.path)
    write_tsv(rows, getattr(args, "output", None))


if __name__ == "__main__":
    main()
