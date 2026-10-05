#!/usr/bin/env python3
"""CLI smoke gate for fx3 check/lower/ir/cap/run/test/package verify."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "tools" / "fx3_cli.py")]
DEFAULT_FX_ROOT = "/home/kim/kim/platform/freelang-v11-fx"


def run(args: list[str], input_text: str | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    merged = None
    if env is not None:
        merged = os.environ.copy()
        merged.update(env)
    return subprocess.run(
        CLI + args,
        cwd=str(ROOT),
        input=input_text,
        capture_output=True,
        text=True,
        env=merged,
    )


def main() -> int:
    fails = []

    p = run(["--help"])
    if p.returncode != 0:
        fails.append(f"help exit {p.returncode}")
    else:
        if "run" not in p.stdout:
            fails.append("help missing run")
        else:
            print("PASS help")

    p = run(["nosuch"])
    if p.returncode != 2:
        fails.append(f"usage want 2 got {p.returncode}")
    else:
        print("PASS bad-subcommand exit 2")

    p = run(["check", "examples/handle-rate-single.fx3"])
    if p.returncode != 0 or p.stdout.strip() != "OK":
        fails.append(f"check ok: {p.returncode} {p.stdout!r}")
    else:
        print("PASS check ok")

    p = run(["check", "fixtures/parse/invalid/03-expected-f.fx3"])
    if p.returncode != 1 or "E_EXPECTED_F" not in p.stderr:
        fails.append(f"check fail: {p.returncode} {p.stderr!r}")
    else:
        print("PASS check fail diagnostic")

    p = run(["lower", "examples/first-id.fx3"])
    want = (ROOT / "examples" / "first-id.fl").read_text(encoding="utf-8")
    if p.returncode != 0 or p.stdout != want:
        fails.append("lower byte mismatch")
    else:
        print("PASS lower bytes")

    p = run(["ir", "examples/first-id.fx3"])
    want_ir = (ROOT / "fixtures" / "ir" / "valid" / "first-id.ir.json").read_bytes()
    if p.returncode != 0 or p.stdout.encode("utf-8") != want_ir:
        fails.append("ir byte mismatch")
    else:
        print("PASS ir bytes")

    p = run(
        [
            "cap",
            "fixtures/capability/allow/01-source-read.request.json",
            "--canonical-root",
            "/canonical/root",
        ]
    )
    if p.returncode != 0:
        fails.append(f"cap allow exit {p.returncode}")
    else:
        d = json.loads(p.stdout)
        if d.get("decision") != "allow":
            fails.append(f"cap allow body {d}")
        else:
            print("PASS cap allow")

    p = run(
        [
            "cap",
            "fixtures/capability/deny/19-request-canonical-root.request.json",
            "--canonical-root",
            "/canonical/root",
        ]
    )
    if p.returncode != 1:
        fails.append(f"cap deny exit {p.returncode}")
    else:
        d = json.loads(p.stdout)
        if d.get("decision") != "deny" or d.get("reason") != "invalid_argument":
            fails.append(f"cap deny body {d}")
        else:
            print("PASS cap deny")

    # --- run (delegated) ---
    p = run(["run", "fixtures/run/sum.fx3", "--call", "(sum 2 3)"])
    if p.returncode != 0 or p.stdout.strip() != "5":
        fails.append(f"run eval: {p.returncode} {p.stdout!r} {p.stderr!r}")
    else:
        print("PASS run eval")

    p = run(
        ["run", "fixtures/run/sum.fx3", "--call", "(sum 2 3)", "--engine", "eval"]
    )
    if p.returncode != 0 or p.stdout.strip() != "5":
        fails.append(f"run engine=eval: {p.returncode} {p.stdout!r}")
    else:
        print("PASS run --engine=eval")

    p = run(
        ["run", "fixtures/parse/invalid/03-expected-f.fx3", "--call", "(sum 2 3)"]
    )
    if p.returncode != 1 or "E_EXPECTED_F" not in p.stderr:
        fails.append(f"run parse fail: {p.returncode} {p.stderr!r}")
    else:
        print("PASS run parse fail exit 1")

    p = run(["run", "fixtures/run/sum.fx3"])
    if p.returncode != 2:
        fails.append(f"run missing --call want 2 got {p.returncode}")
    else:
        print("PASS run missing --call exit 2")

    p = run(
        ["run", "fixtures/run/sum.fx3", "--call", "(sum 2 3)", "--engine", "bogus"]
    )
    if p.returncode != 2:
        fails.append(f"run bad engine want 2 got {p.returncode}")
    else:
        print("PASS run bad --engine exit 2")

    build = Path(os.environ.get("FX_ROOT", DEFAULT_FX_ROOT)) / "fl-build.sh"
    if build.is_file():
        p = run(
            [
                "run",
                "fixtures/run/sum.fx3",
                "--call",
                "(sum 2 3)",
                "--engine",
                "native",
            ]
        )
        if p.returncode != 0 or p.stdout.strip() != "5":
            fails.append(f"run native: {p.returncode} {p.stdout!r} {p.stderr!r}")
        else:
            print("PASS run --engine=native")
    else:
        print("SKIP run native (fl-build.sh missing)")

    p = run(
        ["run", "fixtures/run/sum.fx3", "--call", "(sum 2 3)", "--engine", "native"],
        env={"FX_ROOT": "/nonexistent-fx-root"},
    )
    if p.returncode != 2 or "FX_NATIVE=BLOCKED" not in p.stderr:
        fails.append(f"run native blocked: {p.returncode} {p.stderr!r}")
    else:
        print("PASS run native BLOCKED exit 2")

    p = run(["test", "--quick"])
    if p.returncode != 0 or "FX3_TEST=PASS" not in p.stdout:
        fails.append(f"test quick {p.returncode}")
    else:
        print("PASS test --quick")

    p = run(["package", "verify"])
    if p.returncode != 0 or "FX3_PACKAGE_VERIFY=PASS" not in p.stdout:
        fails.append(f"package verify {p.returncode} {p.stdout[-200:]}")
    else:
        print("PASS package verify")

    if fails:
        for f in fails:
            print("FAIL", f)
        print("CLI_GATE=FAIL")
        return 1
    print("CLI_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
