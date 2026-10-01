#!/usr/bin/env python3
"""delimiter / trailing-`;` / `$a-$b` 회귀. fixture 01–04 바이트는 건드리지 않는다."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lower import LowerError, lower_text  # noqa: E402

CASES = [
    # name, source, must_contain_substring
    ("sub-trailing-semi", "F subtract[$first,$second]{$first-$second;}", "(- $first $second)"),
    ("sub-no-semi", "F subtract[$first,$second]{$first-$second}", "(- $first $second)"),
    ("sum-trailing-semi", "F sum[$a,$b]{$a+$b;}", "(+ $a $b)"),
    ("product", "F multiply[$left,$right]{$left*$right;}", "(* $left $right)"),
    ("kebab-name", "F handle-rate-single[$req]{$req}", "$req"),
    ("nested-kebab-call", 'F f[$x]{http-get-body($x)}', "(http-get-body $x)"),
]


def main() -> int:
    failed = 0
    for name, src, needle in CASES:
        try:
            got = lower_text(src)
        except LowerError as err:
            print(f"FAIL {name}: lower error: {err}")
            failed += 1
            continue
        if needle not in got:
            print(f"FAIL {name}: missing {needle!r}\n{got}")
            failed += 1
            continue
        # 잘못된 한 토큰 변수명 방지
        if "$first-" in got or "$a-" in got:
            print(f"FAIL {name}: hyphen glued into var\n{got}")
            failed += 1
            continue
        print(f"PASS {name}")
    # ops-hole 원본 6건
    ops = ROOT / "bench/results/u1-ops-20260930/first"
    if ops.is_dir():
        for path in sorted(ops.glob("case-*.fx3")):
            try:
                lower_text(path.read_text(encoding="utf-8"))
                print(f"PASS ops-{path.stem}")
            except LowerError as err:
                print(f"FAIL ops-{path.stem}: {err}")
                failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
