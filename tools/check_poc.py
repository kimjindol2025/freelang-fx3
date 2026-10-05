#!/usr/bin/env python3
"""Shared delegated-run POC gate.

Layout per POC:

  poc/<name>/poc.json          # name, source, pass_tag, min_cases
  poc/<name>/fixtures/*.call
  poc/<name>/fixtures/*.expect.json
  poc/<name>/fixtures/*.meta.json   # optional ok/code/field

Does not implement an FX3 VM. Runs via ./bin/fx3 (eval + native).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "tools" / "fx3_cli.py")]

IO_FORBIDDEN = re.compile(
    r"open\(|Path\(|write_text|urlopen|socket\.|subprocess|http"
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _canon(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _run_fx3(src: Path, call: str, engine: str | None = None) -> subprocess.CompletedProcess:
    args = ["run", str(src), "--call", call]
    if engine:
        args.extend(["--engine", engine])
    return subprocess.run(
        CLI + args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def _pick_determinism_call(fix_dir: Path) -> Path | None:
    preferred = sorted(fix_dir.glob("*-ok*.call"))
    if preferred:
        return preferred[0]
    calls = sorted(fix_dir.glob("*.call"))
    return calls[0] if calls else None


def verify_poc(poc_dir: Path) -> int:
    poc_dir = poc_dir.resolve()
    cfg_path = poc_dir / "poc.json"
    if not cfg_path.is_file():
        print(f"FAIL missing {cfg_path}", file=sys.stderr)
        return 1
    cfg = _load_json(cfg_path)
    name = cfg.get("name") or poc_dir.name
    pass_tag = cfg.get("pass_tag") or f"POC_{name.upper().replace('-', '_')}"
    min_cases = int(cfg.get("min_cases", 6))
    src = ROOT / cfg["source"]
    fix = poc_dir / "fixtures"
    if not src.is_file():
        print(f"FAIL missing source {src}", file=sys.stderr)
        return 1
    if not fix.is_dir():
        print(f"FAIL missing fixtures {fix}", file=sys.stderr)
        return 1

    failed = 0
    case_count = 0

    for call_file in sorted(fix.glob("*.call")):
        base = call_file.stem
        expect_file = fix / f"{base}.expect.json"
        meta_file = fix / f"{base}.meta.json"
        if not expect_file.is_file():
            print(f"FAIL {base} missing expect.json", file=sys.stderr)
            failed = 1
            continue
        call = call_file.read_text(encoding="utf-8").strip()
        want = _canon(_load_json(expect_file))
        case_count += 1

        ev = _run_fx3(src, call)
        if ev.returncode != 0:
            print(f"FAIL {base} eval exit {ev.returncode} {ev.stderr.strip()}", file=sys.stderr)
            failed = 1
            continue
        nv = _run_fx3(src, call, engine="native")
        if nv.returncode != 0:
            print(f"FAIL {base} native exit {nv.returncode} {nv.stderr.strip()}", file=sys.stderr)
            failed = 1
            continue

        got_eval = ev.stdout.strip()
        got_native = nv.stdout.strip()
        try:
            eval_obj = json.loads(got_eval)
            native_obj = json.loads(got_native)
            want_obj = json.loads(want)
        except json.JSONDecodeError as e:
            print(f"FAIL {base} json parse: {e}", file=sys.stderr)
            failed = 1
            continue

        if eval_obj != want_obj:
            print(f"FAIL {base} eval got={_canon(eval_obj)} want={want}", file=sys.stderr)
            failed = 1
            continue
        if native_obj != want_obj:
            print(f"FAIL {base} native got={_canon(native_obj)} want={want}", file=sys.stderr)
            failed = 1
            continue
        if eval_obj != native_obj:
            print(f"FAIL {base} eval/native mismatch", file=sys.stderr)
            failed = 1
            continue

        if meta_file.is_file():
            meta = _load_json(meta_file)
            if meta.get("ok") != eval_obj.get("ok"):
                print(
                    f"FAIL {base} meta ok mismatch meta={meta.get('ok')!r} got={eval_obj.get('ok')!r}",
                    file=sys.stderr,
                )
                failed = 1
                continue
            if meta.get("ok") is False:
                if meta.get("code") != eval_obj.get("code") or meta.get("field") != eval_obj.get(
                    "field"
                ):
                    print(
                        f"FAIL {base} code/field meta={meta.get('code')}/{meta.get('field')} "
                        f"got={eval_obj.get('code')}/{eval_obj.get('field')}",
                        file=sys.stderr,
                    )
                    failed = 1
                    continue

        print(f"PASS {base}")

    if case_count < min_cases:
        print(f"FAIL too few fixtures: {case_count} < {min_cases}", file=sys.stderr)
        failed = 1

    det = _pick_determinism_call(fix)
    if det is None:
        print("FAIL no call fixture for determinism", file=sys.stderr)
        failed = 1
    else:
        call = det.read_text(encoding="utf-8").strip()
        r1 = _run_fx3(src, call).stdout.strip()
        r2 = _run_fx3(src, call).stdout.strip()
        r3 = _run_fx3(src, call).stdout.strip()
        if r1 == r2 == r3:
            print("PASS determinism-eval")
        else:
            print("FAIL determinism-eval", file=sys.stderr)
            failed = 1
        n1 = _run_fx3(src, call, engine="native").stdout.strip()
        n2 = _run_fx3(src, call, engine="native").stdout.strip()
        if n1 == n2:
            print("PASS determinism-native")
        else:
            print("FAIL determinism-native", file=sys.stderr)
            failed = 1

    usage = subprocess.run(
        CLI + ["run", str(src)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if usage.returncode == 2:
        print("PASS cli-usage-missing-call")
    else:
        print(f"FAIL cli-usage want 2 got {usage.returncode}", file=sys.stderr)
        failed = 1

    # Static I/O ban in FX3 source + eval_fl_ext (not in check_poc itself).
    scan_paths = [src, ROOT / "tools" / "eval_fl_ext.py"]
    io_hits: list[str] = []
    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if IO_FORBIDDEN.search(line):
                io_hits.append(f"{path.relative_to(ROOT)}:{i}:{line.strip()}")
    if io_hits:
        print("FAIL forbidden I/O symbols found:", file=sys.stderr)
        for h in io_hits:
            print(h, file=sys.stderr)
        failed = 1
    else:
        print("PASS no-forbidden-io-static")

    if failed:
        print(f"{pass_tag}=FAIL")
        return 1
    print(f"{pass_tag}=PASS cases={case_count}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "poc",
        nargs="+",
        help="POC directory under repo (e.g. poc/manifest-validator) or 'all'",
    )
    args = ap.parse_args(argv)
    targets: list[Path] = []
    for item in args.poc:
        if item == "all":
            for child in sorted((ROOT / "poc").iterdir()):
                if child.is_dir() and (child / "poc.json").is_file():
                    targets.append(child)
        else:
            p = Path(item)
            if not p.is_absolute():
                p = ROOT / p
            targets.append(p)
    if not targets:
        print("FAIL no POC targets", file=sys.stderr)
        return 1
    rc = 0
    for t in targets:
        try:
            label = t.relative_to(ROOT)
        except ValueError:
            label = t
        print(f"## POC {label}")
        if verify_poc(t) != 0:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
