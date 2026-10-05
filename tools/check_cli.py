#!/usr/bin/env python3
"""P5 CLI smoke gate for fx3 check/lower/ir/cap/test/package verify."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "tools" / "fx3_cli.py")]


def run(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        CLI + args,
        cwd=str(ROOT),
        input=input_text,
        capture_output=True,
        text=True,
    )


def main() -> int:
    fails = []

    p = run(["--help"])
    if p.returncode != 0:
        fails.append(f"help exit {p.returncode}")
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
