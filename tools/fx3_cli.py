#!/usr/bin/env python3
"""FX3 CLI — check / lower / ir / cap / run / test / package verify.

P5 usable gate + delegated run (eval default, optional native).
No owned FX3 VM. No capability target-file I/O.
Facades existing tools only. See docs/FX3-CLI.md and docs/FX3-RUN.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from eval_fl_ext import EvalError, call, load_program  # noqa: E402
from eval_fl_min import parse, tokenize  # noqa: E402
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

DEFAULT_FX_ROOT = "/home/kim/kim/platform/freelang-v11-fx"
ENGINES = ("eval", "native")


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _literal_value(node: Any) -> Any:
    """Convert eval_fl_min AST node to a Python value for --call args."""
    if isinstance(node, list):
        raise ValueError("call args cannot be nested calls")
    if not isinstance(node, tuple) or len(node) < 2:
        raise ValueError("call args must be literals")
    kind = node[0]
    if kind in ("num", "str", "lit"):
        return node[1]
    if kind == "sym":
        return node[1]
    if kind == "vector":
        return [_literal_value(x) for x in node[1]]
    if kind == "map":
        out: dict[Any, Any] = {}
        for k, v in node[1]:
            out[_literal_value(k)] = _literal_value(v)
        return out
    raise ValueError(f"unsupported call arg kind: {kind}")


def _parse_call_sexpr(text: str) -> tuple[str, list[Any]]:
    """Parse '(name args…)' into name + Python values (literals/maps/vectors)."""
    forms = parse(tokenize(text.strip()))
    if len(forms) != 1 or not isinstance(forms[0], list) or not forms[0]:
        raise ValueError("call must be one form: (name args…)")
    form = forms[0]
    head = form[0]
    if not (isinstance(head, tuple) and head[0] == "sym"):
        raise ValueError("call head must be a symbol")
    name = head[1]
    args = [_literal_value(a) for a in form[1:]]
    return name, args


def _format_eval_result(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    except TypeError:
        return repr(value)


def _py_to_fl(value: Any) -> str:
    """Emit an FX .fl literal from a Python value (native --call adapter)."""
    if value is None:
        return "nil"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + " ".join(_py_to_fl(x) for x in value) + "]"
    if isinstance(value, dict):
        parts = [f"{json.dumps(str(k), ensure_ascii=False)} {_py_to_fl(v)}" for k, v in value.items()]
        return "{" + " ".join(parts) + "}"
    raise ValueError(f"cannot emit FX literal for {type(value).__name__}")


def _call_to_fl_sexpr(call_text: str) -> str:
    name, args = _parse_call_sexpr(call_text)
    if not args:
        return f"({name})"
    return "(" + name + " " + " ".join(_py_to_fl(a) for a in args) + ")"


def _fl_for_native(fl_text: str) -> str:
    """Adapt FX3-lowered .fl to freelang-v11-fx native (= equality)."""
    # FX3 Core lowers == ; native CGC implements = as fl_eq.
    return fl_text.replace("(== ", "(= ")


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


def _run_eval(fl_text: str, call_text: str) -> int:
    try:
        name, args = _parse_call_sexpr(call_text)
    except (ValueError, EvalError) as e:
        _eprint(f"fx3 run: bad --call: {e}")
        return EXIT_USAGE
    try:
        fns = load_program(fl_text)
        got = call(fns, name, args)
    except EvalError as e:
        _eprint(f"fx3 run: eval error: {e}")
        return EXIT_FAIL
    print(_format_eval_result(got))
    return EXIT_OK


def _fx_build_sh() -> Path | None:
    fx_root = Path(os.environ.get("FX_ROOT", DEFAULT_FX_ROOT))
    build = fx_root / "fl-build.sh"
    if build.is_file():
        return build
    return None


def _run_native(fl_text: str, call_text: str) -> int:
    build = _fx_build_sh()
    if build is None:
        _eprint("FX_NATIVE=BLOCKED")
        _eprint(f"CAUSE=missing fl-build.sh under FX_ROOT={os.environ.get('FX_ROOT', DEFAULT_FX_ROOT)}")
        return EXIT_USAGE
    try:
        call_fl = _call_to_fl_sexpr(call_text)
    except (ValueError, EvalError) as e:
        _eprint(f"fx3 run: bad --call: {e}")
        return EXIT_USAGE
    native_fl = _fl_for_native(fl_text)
    work = Path(tempfile.mkdtemp(prefix="fx3-run-"))
    try:
        fl_path = work / "prog.fl"
        bin_path = work / "prog"
        fl_path.write_text(native_fl + f"(println {call_fl})\n", encoding="utf-8")
        proc = subprocess.run(
            ["bash", str(build), str(fl_path), str(bin_path), "--no-net"],
            cwd=str(work),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            _eprint("fx3 run: native build failed")
            if proc.stderr:
                _eprint(proc.stderr.rstrip())
            elif proc.stdout:
                _eprint(proc.stdout.rstrip())
            return EXIT_FAIL
        if not bin_path.is_file():
            _eprint("fx3 run: native binary missing after build")
            return EXIT_FAIL
        run = subprocess.run(
            [str(bin_path)],
            cwd=str(work),
            capture_output=True,
            text=True,
        )
        if run.returncode != 0:
            _eprint("fx3 run: native exec failed")
            if run.stderr:
                _eprint(run.stderr.rstrip())
            return EXIT_FAIL
        lines = run.stdout.replace("\r", "").splitlines()
        last = lines[-1] if lines else ""
        # Normalize JSON-looking native output for stable comparison with eval.
        try:
            last = json.dumps(json.loads(last), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        except json.JSONDecodeError:
            pass
        print(last)
        return EXIT_OK
    finally:
        shutil.rmtree(work, ignore_errors=True)


def cmd_run(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.is_file():
        _eprint(f"fx3 run: not a file: {path}")
        return EXIT_USAGE
    if not args.call:
        _eprint("fx3 run: --call '(name args…)' is required")
        return EXIT_USAGE
    engine = (args.engine or "eval").strip().lower()
    if engine not in ENGINES:
        _eprint(f"fx3 run: bad --engine={args.engine!r} (want eval|native)")
        return EXIT_USAGE
    try:
        fl_text = lower_text(_read_text(path))
    except (LexError, ParseError, LowerAstError) as e:
        _eprint(str(e))
        return EXIT_FAIL
    if engine == "eval":
        return _run_eval(fl_text, args.call)
    return _run_native(fl_text, args.call)


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
        ROOT / "docs" / "FX3-RUN.md",
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
        TOOLS / "eval_fl_min.py",
        TOOLS / "eval_fl_ext.py",
        ROOT / "src" / "manifest-validator.fx3",
        ROOT / "src" / "config-lint.fx3",
        ROOT / "docs" / "FX3-RUN.md",
        ROOT / "docs" / "FX3-DELEGATED-LIMITS.md",
        ROOT / "tools" / "check_poc.py",
        ROOT / "poc" / "README.md",
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
        description=(
            "FX3 Core CLI (check/lower/ir/cap/run/test). "
            "Run is delegated (eval|native). No owned FX3 VM."
        ),
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

    rn = sub.add_parser(
        "run",
        help="lower .fx3 and execute via delegated engine (eval default)",
    )
    rn.add_argument("file")
    rn.add_argument(
        "--call",
        required=True,
        help="FX S-expr call, e.g. '(sum 2 3)'",
    )
    rn.add_argument(
        "--engine",
        default="eval",
        help="eval (default) or native (fl-build.sh --no-net)",
    )
    rn.set_defaults(func=cmd_run)

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
