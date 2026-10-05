#!/usr/bin/env python3
"""FX3 CLI — check / lower / ir / cap / test / package verify.

P5 usable gate. No dedicated runtime. No capability target-file I/O.
Facades existing tools only. See docs/FX3-CLI.md.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from fx3_capability import (  # noqa: E402
    SCHEMA as CAP_SCHEMA,
    decide,
    serialize_decision,
)
from fx3_ir import ABI_NAME, ABI_VERSION, IrError, ir_from_text, serialize_ir  # noqa: E402
from fx3_lex import LexError, lex  # noqa: E402
from fx3_lower import LowerAstError, lower_text  # noqa: E402
from fx3_parse import ParseError, parse_tokens  # noqa: E402

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def cmd_check(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        _eprint(f"fx3 check: not a file: {path}")
        return EXIT_USAGE
    try:
        parse_tokens(lex(_read_text(path)))
    except (LexError, ParseError) as e:
        _eprint(str(e))
        return EXIT_FAIL
    print("OK")
    return EXIT_OK


def cmd_lower(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        _eprint(f"fx3 lower: not a file: {path}")
        return EXIT_USAGE
    try:
        out = lower_text(_read_text(path))
    except (LexError, ParseError, LowerAstError) as e:
        _eprint(str(e))
        return EXIT_FAIL
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)
    return EXIT_OK


def cmd_ir(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        _eprint(f"fx3 ir: not a file: {path}")
        return EXIT_USAGE
    try:
        ir = ir_from_text(_read_text(path))
        text = serialize_ir(ir)
    except (LexError, ParseError, IrError) as e:
        _eprint(str(e))
        return EXIT_FAIL
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        # serialize_ir is deterministic without forced trailing newline
        sys.stdout.write(text)
    return EXIT_OK


def cmd_cap(args: argparse.Namespace) -> int:
    req_path = Path(args.request)
    if not req_path.is_file():
        _eprint(f"fx3 cap: not a file: {req_path}")
        return EXIT_USAGE
    if not args.canonical_root:
        _eprint("fx3 cap: --canonical-root is required (server-fixed root)")
        return EXIT_USAGE
    try:
        req = json.loads(req_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        _eprint(f"fx3 cap: invalid JSON: {e}")
        return EXIT_FAIL
    # Request file read only — never opens capability target paths.
    decision = decide(req, canonical_root=args.canonical_root)
    sys.stdout.write(serialize_decision(decision))
    sys.stdout.write("\n")
    if decision.get("decision") == "allow":
        return EXIT_OK
    return EXIT_FAIL


def _run_gate(name: str, script: str) -> int:
    proc = subprocess.run(
        [sys.executable, str(TOOLS / script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if proc.stdout:
        sys.stdout.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            sys.stdout.write("\n")
    if proc.returncode != 0:
        _eprint(f"fx3 test: FAIL gate={name} exit={proc.returncode}")
        if proc.stderr:
            _eprint(proc.stderr.rstrip())
        return EXIT_FAIL
    print(f"PASS gate={name}")
    return EXIT_OK


def cmd_test(args: argparse.Namespace) -> int:
    gates = [
        ("lex", "check_lex.py"),
        ("parse", "check_parse.py"),
        ("lower", "check_lower.py"),
    ]
    if not args.quick:
        gates.extend(
            [
                ("ir", "check_ir.py"),
                ("capability", "check_capability.py"),
            ]
        )
        if args.legacy_lower:
            gates.append(("legacy_lower", "lower.py"))
    for name, script in gates:
        if script == "lower.py":
            proc = subprocess.run(
                [sys.executable, str(TOOLS / "lower.py"), "--check"],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
            )
            if proc.stdout:
                sys.stdout.write(proc.stdout)
            if proc.returncode != 0:
                _eprint(f"fx3 test: FAIL gate={name} exit={proc.returncode}")
                if proc.stderr:
                    _eprint(proc.stderr.rstrip())
                return EXIT_FAIL
            print(f"PASS gate={name}")
            continue
        rc = _run_gate(name, script)
        if rc != EXIT_OK:
            return rc
    print("FX3_TEST=PASS")
    return EXIT_OK


def cmd_package_verify(args: argparse.Namespace) -> int:
    required = [
        ROOT / "docs" / "IR-ABI-CONTRACT.md",
        ROOT / "docs" / "CAPABILITY-CONTRACT.md",
        ROOT / "docs" / "FX3-CLI.md",
        ROOT / "examples" / "handle-rate-single.fx3",
        ROOT / "examples" / "handle-rate-single.fl",
        ROOT / "examples" / "check-and-log.fx3",
        ROOT / "examples" / "make-result.fx3",
        ROOT / "examples" / "first-id.fx3",
        TOOLS / "fx3_lex.py",
        TOOLS / "fx3_parse.py",
        TOOLS / "fx3_lower.py",
        TOOLS / "fx3_ir.py",
        TOOLS / "fx3_capability.py",
        TOOLS / "fx3_cli.py",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        for m in missing:
            _eprint(f"fx3 package verify: missing {m}")
        return EXIT_FAIL
    # schema constants
    if CAP_SCHEMA != "fx3-capability@1":
        _eprint(f"fx3 package verify: bad capability schema {CAP_SCHEMA!r}")
        return EXIT_FAIL
    if ABI_NAME != "fx3-ir" or ABI_VERSION != 1:
        _eprint(f"fx3 package verify: bad IR abi {ABI_NAME!r}@{ABI_VERSION!r}")
        return EXIT_FAIL
    ns = argparse.Namespace(quick=True, legacy_lower=False)
    rc = cmd_test(ns)
    if rc != EXIT_OK:
        return rc
    print("FX3_PACKAGE_VERIFY=PASS")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fx3",
        description="FX3 Core CLI (check/lower/ir/cap/test). No dedicated runtime.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="lex+parse a .fx3 file")
    c.add_argument("file")
    c.set_defaults(func=cmd_check)

    lo = sub.add_parser("lower", help="lower .fx3 to deterministic .fl")
    lo.add_argument("file")
    lo.add_argument("--out", default=None, help="write .fl to path (default stdout)")
    lo.set_defaults(func=cmd_lower)

    irp = sub.add_parser("ir", help="emit deterministic fx3-ir JSON")
    irp.add_argument("file")
    irp.add_argument("--out", default=None, help="write IR JSON to path (default stdout)")
    irp.set_defaults(func=cmd_ir)

    cap = sub.add_parser("cap", help="capability decide (request JSON only)")
    cap.add_argument("request", help="capability request JSON path")
    cap.add_argument(
        "--canonical-root",
        required=True,
        help="server-fixed workspace root (never from request)",
    )
    cap.set_defaults(func=cmd_cap)

    t = sub.add_parser("test", help="run FX3 gate suite")
    t.add_argument("--quick", action="store_true", help="lex+parse+lower only")
    t.add_argument(
        "--legacy-lower",
        action="store_true",
        help="also run tools/lower.py --check",
    )
    t.set_defaults(func=cmd_test)

    pkg = sub.add_parser("package", help="package helpers")
    pkg_sub = pkg.add_subparsers(dest="pkg_cmd", required=True)
    ver = pkg_sub.add_parser("verify", help="verify docs/fixtures/schema + quick test")
    ver.set_defaults(func=cmd_package_verify)

    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else EXIT_USAGE
        return code if code is not None else EXIT_USAGE
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help(sys.stderr)
        return EXIT_USAGE
    return int(func(args))


if __name__ == "__main__":
    raise SystemExit(main())
