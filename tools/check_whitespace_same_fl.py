#!/usr/bin/env python3
"""공백·줄바꿈이 달라도 같은 .fl (문법 아님).

폭: fixture 01–04 + corpus/stdlib.
저장 파일은 수정하지 않는다. Core/문법 변경 없음.
케밥 이름(`fetch-rate`)은 쪼개지 않는다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from lower import LowerError, lower_text  # noqa: E402
from show import show  # noqa: E402


def targets() -> list[Path]:
    paths: list[Path] = []
    exp = ROOT / "bench/expected"
    for i in range(1, 5):
        paths.append(exp / f"case-0{i}.fx3")
    paths.extend(sorted((ROOT / "corpus/stdlib").glob("*.fx3")))
    return paths


def map_outside_strings(text: str, transform) -> str:
    out: list[str] = []
    i = 0
    n = len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        out.extend(transform(c, text, i))
        i += 1
    return "".join(out)


def pad_delims(text: str) -> str:
    """문자열 밖에서 ]{  }{  ;( 사이 등 구분자 주변에만 스페이스."""

    def transform(c: str, text: str, i: int):
        nxt = text[i + 1] if i + 1 < len(text) else ""
        chunks = [c]
        if c in ";,])}" and nxt and nxt not in " \t\n;,])}":
            chunks.append(" ")
        if c in "[{(" and i > 0 and text[i - 1] not in " \t\n[{(":
            # already appended c; prepend space by rewriting — handle via lookbehind
            pass
        return chunks

    # second pass: insert space before { ( after ] if glued
    s = map_outside_strings(text, transform)
    out: list[str] = []
    i = 0
    n = len(s)
    in_str = False
    while i < n:
        c = s[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(s[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if c in "{([" and out and out[-1] not in " \t\n{([":
            out.append(" ")
        out.append(c)
        i += 1
    return "".join(out)


def collapse_ws(text: str) -> str:
    """문자열 밖 공백 연속을 스페이스 하나로."""

    out: list[str] = []
    i = 0
    n = len(text)
    in_str = False
    prev_space = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            prev_space = False
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            prev_space = False
            i += 1
            continue
        if c in " \t\n":
            if not prev_space:
                out.append(" ")
                prev_space = True
            i += 1
            continue
        out.append(c)
        prev_space = False
        i += 1
    return "".join(out)


def normalize_fl(text: str) -> str:
    text = re.sub(r";.*?$", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text.strip())


def main() -> int:
    failed = 0
    for path in targets():
        name = str(path.relative_to(ROOT))
        try:
            raw = path.read_text(encoding="utf-8")
            base = lower_text(raw)
            variants = {
                "show": show(raw),
                "pad_delims": pad_delims(raw),
                "collapse": collapse_ws(raw),
                "show+collapse": collapse_ws(show(raw)),
                "pad+show": show(pad_delims(raw)),
            }
            for label, src in variants.items():
                try:
                    got = lower_text(src)
                except LowerError as err:
                    raise RuntimeError(f"{label} lower fail: {err}") from err
                if normalize_fl(got) != normalize_fl(base):
                    raise RuntimeError(f"{label} → different .fl\n{got}\n---\n{base}")
            print(f"PASS {name}")
        except Exception as err:  # noqa: BLE001
            print(f"FAIL {name}: {err}")
            failed += 1

    print("WHITESPACE_SAME_FL_SCOPE=fixture_01_04+stdlib")
    print("WHITESPACE_SAME_FL_STORAGE_MUTATION=NO")
    if failed:
        print("WHITESPACE_SAME_FL=FAIL")
        return 1
    print("WHITESPACE_SAME_FL=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
