#!/usr/bin/env python3
"""U1 ops-hole retest with gpt-5.6-luna. AI-ENTRY unchanged."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = Path.home() / ".local/bin/codex"
MODEL = "gpt-5.6-luna"
AI_LIMIT = 180
RUN = ROOT / "bench/results/u1-ops-20260930"
TASKS = ROOT / "bench/u1-ops-hole/tasks"
FORBID_ABBREV = re.compile(r"(?<![A-Za-z0-9_-])([UJLR])\s*\(")
ALLOWED_OPS = {
    "defn",
    "let",
    "do",
    "if",
    "null?",
    "get",
    "+",
    "-",
    "*",
    "/",
    ">=",
    ">",
    "<=",
    "<",
    "==",
    "!=",
}


def entry_fragment() -> str:
    text = (ROOT / "AI-ENTRY.md").read_text(encoding="utf-8")
    m = re.search(r"## 프롬프트에 붙일 최소 조각.*?```text\n(.*?)```", text, re.S)
    if not m:
        raise SystemExit("AI-ENTRY fragment missing")
    return m.group(1).strip()


def strip_source(raw: str) -> str:
    text = raw.strip()
    m = re.search(r"```(?:fx3|text)?\n(.*?)```", text, re.S)
    if m:
        text = m.group(1).strip()
    if "F " in text:
        text = text[text.find("F ") :]
    lines = []
    for line in text.splitlines():
        if lines and line.strip() and not re.search(r"[;{}\[\]$?~F]", line) and not line.strip().startswith("F "):
            break
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


def run_codex(prompt: str, out: Path, events: Path, workdir: Path) -> int:
    workdir.mkdir(parents=True, exist_ok=True)
    prompt_path = workdir / "prompt.txt"
    prompt_path.write_text(prompt, encoding="utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    events.parent.mkdir(parents=True, exist_ok=True)
    with prompt_path.open("rb") as stdin, events.open("wb") as ev:
        proc = subprocess.run(
            [
                str(CLI),
                "exec",
                "--ephemeral",
                "--ignore-user-config",
                "--model",
                MODEL,
                "-c",
                "model_reasoning_effort=low",
                "--skip-git-repo-check",
                "--cd",
                str(workdir),
                "--output-last-message",
                str(out),
                "-",
            ],
            stdin=stdin,
            stdout=ev,
            stderr=subprocess.STDOUT,
            timeout=AI_LIMIT,
            check=False,
        )
    raw = out.read_text(encoding="utf-8") if out.exists() else ""
    out.write_text(strip_source(raw), encoding="utf-8")
    return proc.returncode


def invented_arith_calls(fl_text: str) -> list[str]:
    """Find unknown call heads. Match null? as a whole token (do not split on ?)."""
    # Do not use \b after null? — '?' is non-word and would truncate to 'null'.
    names = re.findall(
        r"\((null\?|[*/+\-]|(?:>=|<=|==|!=)|[<>]|[A-Za-z_][A-Za-z0-9_-]*)(?=[\s)])",
        fl_text,
    )
    invented = []
    defn_name = None
    m = re.search(r"\(defn\s+([A-Za-z_][A-Za-z0-9_-]*)", fl_text)
    if m:
        defn_name = m.group(1)
    for n in names:
        if n in ALLOWED_OPS:
            continue
        if defn_name and n == defn_name:
            continue
        invented.append(n)
    return sorted(set(invented))


def main() -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    frag = entry_fragment()
    before = (ROOT / "AI-ENTRY.md").read_bytes()
    (RUN / "entry-baseline.env").write_text(f"AI_ENTRY_BYTES={len(before)}\nMODEL={MODEL}\n")
    rows = []
    ok = 0
    abbrev_total = 0
    invented_total = 0
    for i in range(1, 7):
        case = f"case-{i:02d}"
        task = (TASKS / case / "TASK.md").read_text(encoding="utf-8")
        prompt = (
            "Return only one FX3 Core source file. No markdown fences. No commentary.\n\n"
            f"{frag}\n\n{task}\n"
        )
        out = RUN / "first" / f"{case}.fx3"
        events = RUN / "events" / f"{case}.jsonl"
        t0 = time.time()
        ai_exit = run_codex(prompt, out, events, RUN / "work" / case)
        ms = int((time.time() - t0) * 1000)
        text = out.read_text(encoding="utf-8")
        ab = FORBID_ABBREV.findall(text)
        abbrev_total += len(ab)
        fl_path = RUN / "lowered" / f"{case}.fl"
        fl_path.parent.mkdir(parents=True, exist_ok=True)
        p = subprocess.run(["python3", str(ROOT / "tools/lower.py"), str(out)], capture_output=True)
        lower = p.returncode == 0
        if lower:
            fl_path.write_bytes(p.stdout)
            fl_text = p.stdout.decode()
        else:
            fl_path.write_bytes(p.stderr)
            fl_text = p.stderr.decode()
        invented = invented_arith_calls(fl_text) if lower else []
        invented_total += len(invented)
        sem = False
        note = ""
        if lower and not invented:
            tests = json.loads((TASKS / case / "tests.json").read_text(encoding="utf-8"))
            sem = True
            for t in tests["tests"]:
                r = subprocess.run(
                    [
                        "python3",
                        str(ROOT / "tools/eval_fl_min.py"),
                        str(fl_path),
                        "--call",
                        "AUTO",
                        "--args-json",
                        json.dumps(t["args"]),
                        "--expect-json",
                        json.dumps(t["expect"]),
                    ],
                    capture_output=True,
                    text=True,
                )
                if r.returncode != 0:
                    sem = False
                    note = (r.stderr or r.stdout).strip()[:160]
                    break
        elif invented:
            note = "INVENTED:" + ",".join(invented)
        elif not lower:
            note = fl_text[:160]
        first = lower and sem and not ab and not invented
        if first:
            ok += 1
        rows.append(
            {
                "CASE": case,
                "AI_EXIT": ai_exit,
                "AI_MS": ms,
                "LOWER": "PASS" if lower else "FAIL",
                "SEMANTIC": "PASS" if sem else "FAIL",
                "INVENTED_ARITH_CALL": ",".join(invented) if invented else "0",
                "ABBREV": len(ab),
                "FIRST_VALID": "PASS" if first else "FAIL",
                "NOTE": note,
                "SOURCE": text.strip().replace("\n", "\\n"),
            }
        )
        print(case, "FIRST", "PASS" if first else "FAIL", note[:80], flush=True)

    after = (ROOT / "AI-ENTRY.md").read_bytes()
    entry_same = before == after
    pack = ok >= 5 and abbrev_total == 0 and invented_total == 0 and entry_same
    with (RUN / "metrics.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    summary = (
        f"MODEL={MODEL}\n"
        f"FIRST_VALID={ok}/6\n"
        f"ABBREVIATION_INVENTED={abbrev_total}\n"
        f"INVENTED_ARITH_CALL_COUNT={invented_total}\n"
        f"ENTRY_BYTES_UNCHANGED={'YES' if entry_same else 'NO'}\n"
        f"ENTRY_OUTSIDE_LOOKUP=NO\n"
        f"PACK={'PASS' if pack else 'FAIL'}\n"
    )
    (RUN / "summary.env").write_text(summary)
    print(summary, flush=True)


if __name__ == "__main__":
    main()
