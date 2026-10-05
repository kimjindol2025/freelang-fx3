#!/usr/bin/env python3
"""P3 IR/ABI gate: schema · determinism · location · unsupported reject."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fx3_ir import (  # noqa: E402
    ABI_NAME,
    ABI_VERSION,
    IrError,
    ast_to_ir,
    ir_bytes_from_text,
    ir_from_text,
    validate_ir,
)
from fx3_lex import LexError  # noqa: E402
from fx3_parse import ParseError  # noqa: E402

EXAMPLES = ROOT / "examples"
VALID = ROOT / "fixtures" / "ir" / "valid"
INVALID = ROOT / "fixtures" / "ir" / "invalid"
GOLDEN = [
    "handle-rate-single",
    "check-and-log",
    "make-result",
    "first-id",
]


def read_expect(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def walk_ops(node, out=None):
    if out is None:
        out = []
    if isinstance(node, dict):
        if "op" in node:
            out.append(node)
        for v in node.values():
            walk_ops(v, out)
    elif isinstance(node, list):
        for x in node:
            walk_ops(x, out)
    return out


def check_golden() -> list:
    fails = []
    for stem in GOLDEN:
        src = (EXAMPLES / f"{stem}.fx3").read_text(encoding="utf-8")
        want_path = VALID / f"{stem}.ir.json"
        if not want_path.exists():
            fails.append(f"FAIL golden {stem}: missing {want_path.name}")
            continue
        want = want_path.read_bytes()
        try:
            got = ir_bytes_from_text(src)
        except (IrError, ParseError, LexError) as e:
            fails.append(f"FAIL golden {stem}: {e}")
            continue
        if got != want:
            fails.append(f"FAIL golden {stem}: IR byte mismatch")
            continue
        ir = json.loads(got.decode("utf-8"))
        try:
            validate_ir(ir)
        except IrError as e:
            fails.append(f"FAIL golden {stem}: validate {e}")
            continue
        print(f"PASS golden {stem} bytes={len(got)}")
    return fails


def check_determinism() -> list:
    fails = []
    for stem in GOLDEN:
        src = (EXAMPLES / f"{stem}.fx3").read_text(encoding="utf-8")
        a = ir_bytes_from_text(src)
        b = ir_bytes_from_text(src)
        if a != b:
            fails.append(f"FAIL determinism {stem}")
            continue
        print(f"PASS determinism {stem}")
    return fails


def check_locations() -> list:
    fails = []
    for stem in GOLDEN:
        ir = ir_from_text((EXAMPLES / f"{stem}.fx3").read_text(encoding="utf-8"))
        nodes = walk_ops(ir)
        if not nodes:
            fails.append(f"FAIL location {stem}: no nodes")
            continue
        bad = [
            n
            for n in nodes
            if not isinstance(n.get("loc"), dict)
            or not isinstance(n["loc"].get("line"), int)
            or not isinstance(n["loc"].get("column"), int)
            or n["loc"]["line"] < 1
            or n["loc"]["column"] < 1
        ]
        if bad:
            fails.append(f"FAIL location {stem}: {bad[0].get('op')}")
            continue
        print(f"PASS location {stem} nodes={len(nodes)}")
    return fails


def check_schema_smoke() -> list:
    fails = []
    ir = ir_from_text((EXAMPLES / "make-result.fx3").read_text(encoding="utf-8"))
    if ir.get("abi") != ABI_NAME or ir.get("version") != ABI_VERSION:
        fails.append("FAIL schema abi/version")
    else:
        print(f"PASS schema abi={ABI_NAME} version={ABI_VERSION}")
    ops = {n["op"] for n in walk_ops(ir)}
    for need in ("program", "function", "result", "map", "map_entry", "call"):
        if need not in ops:
            fails.append(f"FAIL schema missing op {need}")
    if not fails:
        print("PASS schema core ops present")
    # result == body[-1]
    fn = ir["functions"][0]
    if fn["result"]["value"] != fn["body"][-1]:
        fails.append("FAIL schema result!=body[-1]")
    else:
        print("PASS schema result≡body[-1]")
    return fails


def check_unsupported_ast() -> list:
    fails = []
    bad = SimpleNamespace(kind="loop", line=6, column=2)
    mod = SimpleNamespace(
        kind="module",
        line=1,
        column=1,
        forms=[
            SimpleNamespace(
                kind="defn",
                name="x",
                params=(),
                line=1,
                column=1,
                body=SimpleNamespace(
                    kind="body",
                    line=1,
                    column=1,
                    bindings=(),
                    exprs=(bad,),
                ),
            )
        ],
    )
    try:
        ast_to_ir(mod)
        fails.append("FAIL unsupported-ast: expected error")
    except IrError as e:
        if e.code != "E_UNSUPPORTED_NODE" or e.line != 6 or e.column != 2:
            fails.append(f"FAIL unsupported-ast: {e}")
        else:
            print(f"PASS unsupported-ast {e.code} {e.line}:{e.column}")
    return fails


def check_invalid_dir() -> list:
    fails = []
    for path in sorted(INVALID.glob("*.ir.json")):
        base = path.name[: -len(".ir.json")]
        expect_path = path.parent / f"{base}.expect"
        expect = read_expect(expect_path) if expect_path.exists() else {}
        raw = path.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            fails.append(f"FAIL invalid {path.name}: bad json {e}")
            continue
        try:
            validate_ir(data)
            fails.append(f"FAIL invalid {path.name}: expected reject")
            continue
        except IrError as e:
            want_code = expect.get("code", "E_UNSUPPORTED_NODE")
            want_line = int(expect.get("line", "0"))
            want_col = int(expect.get("column", "0"))
            if e.code != want_code:
                fails.append(f"FAIL invalid {path.name}: code {e.code} want {want_code}")
                continue
            if want_line and (e.line != want_line or e.column != want_col):
                fails.append(
                    f"FAIL invalid {path.name}: want {want_line}:{want_col} "
                    f"got {e.line}:{e.column}"
                )
                continue
            print(f"PASS invalid {path.name} {e.code} {e.line}:{e.column}")
    return fails


def main() -> int:
    fails: list = []
    fails.extend(check_golden())
    fails.extend(check_determinism())
    fails.extend(check_locations())
    fails.extend(check_schema_smoke())
    fails.extend(check_unsupported_ast())
    fails.extend(check_invalid_dir())
    if fails:
        for f in fails:
            print(f)
        print("P3_IR_GATE=FAIL")
        return 1
    print("P3_IR_GATE=PASS")
    print("DETERMINISM=PASS")
    print("LOCATION_PRESERVATION=PASS")
    print(f"ABI_SCHEMA={ABI_NAME}@{ABI_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
