#!/usr/bin/env python3
"""FX3 → lower → eval_fl_min 의미 검증 (Core 산술·조건 부분집합).

네이티브 FX ELF 빌드와 별개다. 전용 런타임을 만들지 않고,
저장소의 최소 평가기로 내린 `.fl`이 기대값을 내는지 확인한다.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "tools/lower.py"
EVAL = ROOT / "tools/eval_fl_min.py"

# (fx3 source, args_json, expect_json)
CASES = [
    ("F sum[$a,$b]{$a+$b;}", [2, 3], 5),
    ("F multiply[$left,$right]{$left*$right;}", [4, 5], 20),
    ("F subtract[$first,$second]{$first-$second;}", [10, 3], 7),
    ("F square-or-zero[$value]{?~$value{0}{$value*$value};}", [None], 0),
    ("F square-or-zero[$value]{?~$value{0}{$value*$value};}", [4], 16),
    ("F multiply-add[$a,$b,$c]{$a*$b+$c;}", [2, 3, 4], 10),
    ("F double-positive[$number]{?$number>0{$number*2}{0};}", [5], 10),
    ("F double-positive[$number]{?$number>0{$number*2}{0};}", [-1], 0),
]


def lower(src: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(LOWER)],
        input=src.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8")


def main() -> int:
    failed = 0
    with tempfile.TemporaryDirectory(prefix="fx3-sem-") as tmp:
        tmp_path = Path(tmp)
        for i, (src, args, expect) in enumerate(CASES, 1):
            name = f"case-{i:02d}"
            try:
                fl = lower(src)
            except RuntimeError as err:
                print(f"FAIL {name} lower: {err}")
                failed += 1
                continue
            fl_path = tmp_path / f"{name}.fl"
            fl_path.write_text(fl, encoding="utf-8")
            proc = subprocess.run(
                [
                    sys.executable,
                    str(EVAL),
                    str(fl_path),
                    "--args-json",
                    json.dumps(args),
                    "--expect-json",
                    json.dumps(expect),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if proc.returncode != 0:
                print(f"FAIL {name}: {proc.stderr.decode('utf-8', 'replace').strip() or proc.stdout.decode()}")
                failed += 1
                continue
            print(f"PASS {name}")
    if failed:
        print("SEMANTIC_MIN=FAIL")
        return 1
    print("SEMANTIC_MIN=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
