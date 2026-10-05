#!/usr/bin/env python3
"""P1 parser gate: valid AST PASS, invalid REJECT with code+location."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fx3_lex import LexError  # noqa: E402
from fx3_parse import ParseError, parse_text, walk  # noqa: E402

EXAMPLES = ROOT / "examples"
VALID = ROOT / "fixtures" / "parse" / "valid"
INVALID = ROOT / "fixtures" / "parse" / "invalid"
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


def assert_locations(mod) -> Optional[str]:
    for node in walk(mod):
        line = getattr(node, "line", None)
        column = getattr(node, "column", None)
        if line is None or column is None or line < 1 or column < 1:
            return f"bad location on {getattr(node, 'kind', type(node))}: {line}:{column}"
    return None


def check_golden() -> list:
    fails = []
    for name in GOLDEN:
        src = (EXAMPLES / f"{name}.fx3").read_text(encoding="utf-8")
        try:
            mod = parse_text(src)
        except (ParseError, LexError) as e:
            fails.append(f"FAIL golden {name}: unexpected {e}")
            continue
        loc_err = assert_locations(mod)
        if loc_err:
            fails.append(f"FAIL golden {name}: {loc_err}")
            continue
        if len(mod.forms) != 1 or mod.forms[0].kind != "defn":
            fails.append(f"FAIL golden {name}: expected one defn")
            continue
        print(f"PASS golden {name} defn={mod.forms[0].name}")
    return fails


def check_valid_dir() -> list:
    fails = []
    for fx3 in sorted(VALID.glob("*.fx3")):
        expect = read_expect(fx3.with_suffix(".expect"))
        src = fx3.read_text(encoding="utf-8")
        try:
            mod = parse_text(src)
        except (ParseError, LexError) as e:
            fails.append(f"FAIL valid {fx3.name}: unexpected {e}")
            continue
        loc_err = assert_locations(mod)
        if loc_err:
            fails.append(f"FAIL valid {fx3.name}: {loc_err}")
            continue
        defn = mod.forms[0]
        if expect.get("defn") and defn.name != expect["defn"]:
            fails.append(f"FAIL valid {fx3.name}: defn want {expect['defn']} got {defn.name}")
            continue
        if expect.get("params") and str(len(defn.params)) != expect["params"]:
            fails.append(
                f"FAIL valid {fx3.name}: params want {expect['params']} got {len(defn.params)}"
            )
            continue
        if expect.get("bindings") and str(len(defn.body.bindings)) != expect["bindings"]:
            fails.append(
                f"FAIL valid {fx3.name}: bindings want {expect['bindings']} "
                f"got {len(defn.body.bindings)}"
            )
            continue
        kinds = {n.kind for n in walk(mod)}
        if expect.get("has_if") == "1" and "if" not in kinds:
            fails.append(f"FAIL valid {fx3.name}: missing if")
            continue
        if expect.get("has_map") == "1" and "map" not in kinds:
            fails.append(f"FAIL valid {fx3.name}: missing map")
            continue
        if expect.get("has_call") == "1" and "call" not in kinds:
            fails.append(f"FAIL valid {fx3.name}: missing call")
            continue
        if expect.get("has_op") == "1" and "op" not in kinds:
            fails.append(f"FAIL valid {fx3.name}: missing op")
            continue
        if expect.get("defn_line") and defn.line != int(expect["defn_line"]):
            fails.append(f"FAIL valid {fx3.name}: defn_line")
            continue
        if expect.get("defn_column") and defn.column != int(expect["defn_column"]):
            fails.append(f"FAIL valid {fx3.name}: defn_column")
            continue
        if expect.get("binding0_name"):
            b0 = defn.body.bindings[0]
            if b0.name != expect["binding0_name"]:
                fails.append(f"FAIL valid {fx3.name}: binding0_name")
                continue
            if b0.line != int(expect["binding0_line"]) or b0.column != int(
                expect["binding0_column"]
            ):
                fails.append(
                    f"FAIL valid {fx3.name}: binding0 loc want "
                    f"{expect['binding0_line']}:{expect['binding0_column']} "
                    f"got {b0.line}:{b0.column}"
                )
                continue
        print(f"PASS valid {fx3.name}")
    return fails


def check_invalid_dir() -> list:
    fails = []
    for fx3 in sorted(INVALID.glob("*.fx3")):
        expect = read_expect(fx3.with_suffix(".expect"))
        src = fx3.read_text(encoding="utf-8")
        try:
            mod = parse_text(src)
            fails.append(
                f"FAIL invalid {fx3.name}: expected {expect.get('code')} "
                f"got module forms={len(mod.forms)}"
            )
            continue
        except LexError as e:
            fails.append(f"FAIL invalid {fx3.name}: lex error {e} (want parse reject)")
            continue
        except ParseError as e:
            want_code = expect["code"]
            want_line = int(expect["line"])
            want_col = int(expect["column"])
            if e.code != want_code or e.line != want_line or e.column != want_col:
                fails.append(
                    f"FAIL invalid {fx3.name}: want {want_code} {want_line}:{want_col} "
                    f"got {e.code} {e.line}:{e.column}"
                )
                continue
            print(f"PASS invalid {fx3.name} {e.code} {e.line}:{e.column}")
    return fails


def main() -> int:
    fails: list = []
    fails.extend(check_golden())
    fails.extend(check_valid_dir())
    fails.extend(check_invalid_dir())
    if fails:
        for f in fails:
            print(f)
        print("PARSE_GATE=FAIL")
        return 1
    print("PARSE_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
