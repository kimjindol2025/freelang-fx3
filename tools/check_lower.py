#!/usr/bin/env python3
"""P2 lowering gate: AST → deterministic .fl bytes."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fx3_lex import LexError  # noqa: E402
from fx3_lower import LowerAstError, lower_bytes, lower_module, lower_text  # noqa: E402
from fx3_parse import (  # noqa: E402
    Body,
    Call,
    Defn,
    Map,
    Module,
    Num,
    ParseError,
    Var,
)

EXAMPLES = ROOT / "examples"
VALID = ROOT / "fixtures" / "lower" / "valid"
INVALID = ROOT / "fixtures" / "lower" / "invalid"
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


def check_golden() -> list:
    fails = []
    for stem in GOLDEN:
        src = (EXAMPLES / f"{stem}.fx3").read_text(encoding="utf-8")
        want = (EXAMPLES / f"{stem}.fl").read_bytes()
        try:
            got = lower_bytes(src)
        except (LowerAstError, ParseError, LexError) as e:
            fails.append(f"FAIL golden {stem}: {e}")
            continue
        if got != want:
            fails.append(f"FAIL golden {stem}: byte mismatch")
            continue
        print(f"PASS golden {stem} bytes={len(got)}")
    return fails


def check_determinism() -> list:
    fails = []
    for stem in GOLDEN:
        src = (EXAMPLES / f"{stem}.fx3").read_text(encoding="utf-8")
        a = lower_bytes(src)
        b = lower_bytes(src)
        if a != b:
            fails.append(f"FAIL determinism {stem}")
            continue
        print(f"PASS determinism {stem}")
    # also valid dir sources
    for fx3 in sorted(VALID.glob("*.fx3")):
        src = fx3.read_text(encoding="utf-8")
        if lower_bytes(src) != lower_bytes(src):
            fails.append(f"FAIL determinism {fx3.name}")
            continue
        print(f"PASS determinism {fx3.name}")
    return fails


def check_valid_dir() -> list:
    fails = []
    for fx3 in sorted(VALID.glob("*.fx3")):
        fl = fx3.with_suffix(".fl")
        expect_path = fx3.with_suffix(".expect")
        src = fx3.read_text(encoding="utf-8")
        try:
            got = lower_bytes(src)
        except (LowerAstError, ParseError, LexError) as e:
            fails.append(f"FAIL valid {fx3.name}: {e}")
            continue
        if fl.exists():
            want = fl.read_bytes()
            if got != want:
                fails.append(f"FAIL valid {fx3.name}: != {fl.name}")
                continue
        if expect_path.exists():
            expect = read_expect(expect_path)
            text = got.decode("utf-8")
            if expect.get("contains") and expect["contains"] not in text:
                fails.append(f"FAIL valid {fx3.name}: missing {expect['contains']!r}")
                continue
            if expect.get("bytes") and str(len(got)) != expect["bytes"]:
                fails.append(
                    f"FAIL valid {fx3.name}: bytes want {expect['bytes']} got {len(got)}"
                )
                continue
        # map key order: source order must appear in output order
        if "map" in fx3.name or fx3.name.startswith("02-"):
            # soft structural check already via .fl bytes when present
            pass
        print(f"PASS valid {fx3.name} bytes={len(got)}")
    return fails


def check_features() -> list:
    """binding / nested call / conditional / map order smokes."""
    fails = []
    # binding + nested get/call — golden handle-rate
    h = lower_text((EXAMPLES / "handle-rate-single.fx3").read_text(encoding="utf-8"))
    if "(let [$cur" not in h or "(str_upper (get (get $req" not in h:
        fails.append("FAIL feature binding/nested-call")
    else:
        print("PASS feature binding+nested-call")
    # conditional
    c = lower_text((EXAMPLES / "check-and-log.fx3").read_text(encoding="utf-8"))
    if "(if (> $x 10)" not in c:
        fails.append("FAIL feature conditional")
    else:
        print("PASS feature conditional")
    # map key ordering (source order ok,data,count)
    m = lower_text((EXAMPLES / "make-result.fx3").read_text(encoding="utf-8"))
    i_ok = m.find('"ok"')
    i_data = m.find('"data"')
    i_count = m.find('"count"')
    if not (0 <= i_ok < i_data < i_count):
        fails.append("FAIL feature map-key-order")
    else:
        print("PASS feature map-key-order")
    return fails


def check_unsupported_and_invalid_ast() -> list:
    fails = []
    # unsupported kind
    bad = SimpleNamespace(kind="loop", line=3, column=5, body=None)
    try:
        from fx3_lower import fmt

        fmt(bad, 0)
        fails.append("FAIL unsupported: expected error")
    except LowerAstError as e:
        if e.code != "E_UNSUPPORTED_NODE" or e.line != 3 or e.column != 5:
            fails.append(f"FAIL unsupported loc/code: {e}")
        else:
            print(f"PASS unsupported {e.code} {e.line}:{e.column}")

    # invalid module: two defns
    d1 = Defn(
        "defn",
        "a",
        (),
        Body("body", (), (Num("num", "1", 1, 8),), 1, 7),
        1,
        1,
    )
    d2 = Defn(
        "defn",
        "b",
        (),
        Body("body", (), (Num("num", "2", 1, 16),), 1, 15),
        1,
        9,
    )
    mod = Module("module", (d1, d2), 1, 1)
    try:
        lower_module(mod)
        fails.append("FAIL invalid-ast two-defn: expected error")
    except LowerAstError as e:
        if e.code != "E_UNSUPPORTED_NODE":
            fails.append(f"FAIL invalid-ast two-defn code: {e}")
        else:
            print(f"PASS invalid-ast two-defn {e.code} {e.line}:{e.column}")

    # invalid: body replaced with non-body
    bad_defn = Defn("defn", "a", (), Num("num", "1", 2, 4), 2, 1)
    try:
        lower_module(Module("module", (bad_defn,), 2, 1))
        fails.append("FAIL invalid-ast bad-body: expected error")
    except LowerAstError as e:
        if e.code != "E_UNSUPPORTED_NODE" or e.line != 2 or e.column != 4:
            fails.append(f"FAIL invalid-ast bad-body: {e}")
        else:
            print(f"PASS invalid-ast bad-body {e.code} {e.line}:{e.column}")

    # map with non-pair child
    bad_map = Map(
        "map",
        (Var("var", "$x", 4, 2),),
        4,
        1,
    )
    try:
        from fx3_lower import fmt

        fmt(bad_map, 0)
        fails.append("FAIL invalid-ast bad-pair: expected error")
    except LowerAstError as e:
        if e.code != "E_UNSUPPORTED_NODE" or e.line != 4 or e.column != 2:
            fails.append(f"FAIL invalid-ast bad-pair: {e}")
        else:
            print(f"PASS invalid-ast bad-pair {e.code} {e.line}:{e.column}")
    return fails


def check_invalid_dir() -> list:
    fails = []
    for fx3 in sorted(INVALID.glob("*.fx3")):
        expect = read_expect(fx3.with_suffix(".expect"))
        src = fx3.read_text(encoding="utf-8")
        try:
            out = lower_text(src)
            fails.append(
                f"FAIL invalid {fx3.name}: expected reject got {len(out)} chars"
            )
            continue
        except ParseError as e:
            # parse-level reject still counts if expect says so
            code = e.code
            line, col = e.line, e.column
        except LowerAstError as e:
            code = e.code
            line, col = e.line, e.column
        except LexError as e:
            fails.append(f"FAIL invalid {fx3.name}: lex {e}")
            continue
        want_code = expect["code"]
        want_line = int(expect["line"])
        want_col = int(expect["column"])
        if code != want_code or line != want_line or col != want_col:
            fails.append(
                f"FAIL invalid {fx3.name}: want {want_code} {want_line}:{want_col} "
                f"got {code} {line}:{col}"
            )
            continue
        print(f"PASS invalid {fx3.name} {code} {line}:{col}")
    return fails


def check_source_location_preserved() -> list:
    """Lower path keeps parse locations available on errors from AST nodes."""
    fails = []
    # Construct call with unsupported arg kind via SimpleNamespace inside Call
    weird = SimpleNamespace(kind="future", line=9, column=7)
    call = Call("call", "foo", (weird,), 9, 1)
    try:
        from fx3_lower import fmt

        fmt(call, 0)
        fails.append("PASS? unexpected success on future node")
        fails.append("FAIL location-preserve: expected error")
    except LowerAstError as e:
        if e.line != 9 or e.column != 7 or e.code != "E_UNSUPPORTED_NODE":
            fails.append(f"FAIL location-preserve: {e}")
        else:
            print(f"PASS location-preserve {e.code} {e.line}:{e.column}")
    return fails


def main() -> int:
    fails: list = []
    fails.extend(check_golden())
    fails.extend(check_valid_dir())
    fails.extend(check_features())
    fails.extend(check_determinism())
    fails.extend(check_unsupported_and_invalid_ast())
    fails.extend(check_invalid_dir())
    fails.extend(check_source_location_preserved())
    if fails:
        for f in fails:
            print(f)
        print("LOWER_GATE=FAIL")
        return 1
    print("LOWER_GATE=PASS")
    print("DETERMINISM=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
