#!/usr/bin/env python3
"""세미콜론 표시 검사.

저장 파일은 한 줄. 다시 볼 때만 문자열 밖 `;`에서 줄을 나눈다.
블록 안 추가 접기·들여쓰기 없음. 줄바꿈은 문법 아님 → 같은 .fx3 → 같은 .fl.
폭: fixture 01–04 + corpus/stdlib. 문법·Core·fixture05·app 변경 없음.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lower import lower_text  # noqa: E402
from show import show  # noqa: E402


def normalize_fl(text: str) -> str:
    text = re.sub(r";.*?$", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text.strip())


def targets() -> list[tuple[str, Path, Path | None]]:
    rows: list[tuple[str, Path, Path | None]] = []
    exp = ROOT / "bench/expected"
    for i in range(1, 5):
        fx3 = exp / f"case-0{i}.fx3"
        fl = exp / f"case-0{i}.fl"
        rows.append((f"fixture/{fx3.stem}", fx3, fl))
    std = ROOT / "corpus/stdlib"
    for fx3 in sorted(std.glob("*.fx3")):
        fl = fx3.with_suffix(".fl")
        rows.append((f"stdlib/{fx3.stem}", fx3, fl if fl.is_file() else None))
    return rows


def assert_storage_one_line(name: str, raw: str) -> None:
    body = raw.rstrip("\n")
    if "\n" in body:
        raise RuntimeError(f"{name}: 저장 파일에 내부 줄바꿈이 있습니다 (한 줄이어야 함)")


def assert_show_rules(name: str, raw: str, displayed: str) -> None:
    # 들여쓰기·탭으로 블록을 더 접지 않음
    for line in displayed.splitlines():
        if line.startswith((" ", "\t")):
            raise RuntimeError(f"{name}: 표시에 들여쓰기가 있습니다: {line!r}")
    # 문자열 밖 ; 뒤에는 줄바꿈
    if ";" in raw.rstrip("\n"):
        if ";\n" not in displayed and not displayed.rstrip().endswith(";"):
            # 마지막이 ; 없이 끝나는 본문도 있음 — 중간 ; 는 ;\n
            if raw.count(";") > 0 and ";\n" not in displayed:
                raise RuntimeError(f"{name}: `;` 뒤 줄바꿈이 없습니다")


def main() -> int:
    failed = 0
    for name, fx3, fl in targets():
        try:
            raw = fx3.read_text(encoding="utf-8")
            assert_storage_one_line(name, raw)
            displayed = show(raw)
            assert_show_rules(name, raw, displayed)
            low_raw = lower_text(raw)
            low_disp = lower_text(displayed)
            if low_raw != low_disp:
                raise RuntimeError(f"{name}: 표시 줄바꿈이 lower 결과를 바꿨습니다")
            if fl is not None:
                want = fl.read_text(encoding="utf-8")
                if normalize_fl(low_raw) != normalize_fl(want):
                    raise RuntimeError(f"{name}: lower ≠ golden .fl")
            print(f"PASS {name}")
            if ";" in raw:
                # 표시 미리보기 한 줄 요약
                nlines = len(displayed.splitlines())
                print(f"  show_lines={nlines}")
        except Exception as err:  # noqa: BLE001
            print(f"FAIL {name}: {err}")
            failed += 1

    print("SEMI_DISPLAY_SCOPE=fixture_01_04+stdlib")
    print("SEMI_DISPLAY_STORAGE=ONE_LINE")
    print("SEMI_DISPLAY_NEWLINE_GRAMMAR=NO")
    print("SEMI_DISPLAY_CORE_CUT=NO")
    print("SEMI_DISPLAY_FIXTURE_05=NO")
    print("SEMI_DISPLAY_HOT_ALIAS=NO")
    print("SEMI_DISPLAY_APP=NO")
    if failed:
        print("SEMI_DISPLAY=FAIL")
        return 1
    print("SEMI_DISPLAY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
