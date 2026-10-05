#!/usr/bin/env python3
"""P1 lexer gate: valid fixture PASS, invalid REJECT, diagnostic location PASS."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fx3_lex import LexError, lex  # noqa: E402

EXAMPLES = ROOT / "examples"
VALID = ROOT / "fixtures" / "lex" / "valid"
INVALID = ROOT / "fixtures" / "lex" / "invalid"
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
    for name in GOLDEN:
        src = (EXAMPLES / f"{name}.fx3").read_text(encoding="utf-8")
        try:
            tokens = lex(src)
        except LexError as e:
            fails.append(f"FAIL golden {name}: unexpected {e}")
            continue
        if not tokens:
            fails.append(f"FAIL golden {name}: empty token stream")
            continue
        bad_loc = [t for t in tokens if t.line < 1 or t.column < 1]
        if bad_loc:
            fails.append(f"FAIL golden {name}: bad location on {bad_loc[0]}")
            continue
        print(f"PASS golden {name} tokens={len(tokens)}")
    return fails


def check_valid_dir() -> list:
    fails = []
    for fx3 in sorted(VALID.glob("*.fx3")):
        expect_path = fx3.with_suffix(".expect")
        expect = read_expect(expect_path) if expect_path.exists() else {"ok": "1"}
        src = fx3.read_text(encoding="utf-8")
        try:
            tokens = lex(src)
        except LexError as e:
            fails.append(f"FAIL valid {fx3.name}: unexpected {e}")
            continue
        if expect.get("ok") == "1" and not tokens:
            fails.append(f"FAIL valid {fx3.name}: empty token stream")
            continue
        if "token0" in expect:
            kind_or_val, line_s, col_s = expect["token0"].split(":")
            t0 = tokens[0]
            if not (
                (t0.kind == kind_or_val or t0.value == kind_or_val)
                and t0.line == int(line_s)
                and t0.column == int(col_s)
            ):
                fails.append(
                    f"FAIL valid {fx3.name}: token0 want {expect['token0']} "
                    f"got {t0.kind}:{t0.value}:{t0.line}:{t0.column}"
                )
                continue
        if "token_var_y" in expect:
            _, line_s, col_s = expect["token_var_y"].split(":")
            hit = next((t for t in tokens if t.kind == "VAR" and t.value == "$y"), None)
            if hit is None or hit.line != int(line_s) or hit.column != int(col_s):
                fails.append(
                    f"FAIL valid {fx3.name}: token_var_y want {expect['token_var_y']} "
                    f"got {hit}"
                )
                continue
        print(f"PASS valid {fx3.name} tokens={len(tokens)}")
    return fails


def check_invalid_dir() -> list:
    fails = []
    for fx3 in sorted(INVALID.glob("*.fx3")):
        expect = read_expect(fx3.with_suffix(".expect"))
        src = fx3.read_text(encoding="utf-8")
        try:
            tokens = lex(src)
            fails.append(
                f"FAIL invalid {fx3.name}: expected reject "
                f"{expect.get('code')} got {len(tokens)} tokens"
            )
            continue
        except LexError as e:
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
        print("LEX_GATE=FAIL")
        return 1
    print("LEX_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
