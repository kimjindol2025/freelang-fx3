#!/usr/bin/env python3
"""표시 전용. 저장 파일은 바꾸지 않는다. 문자열 밖의 ; 뒤에서만 줄을 나눈다."""

import sys


def show(text: str) -> str:
    out = []
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
        if c == ";":
            out.append(";\n")
            i += 1
            continue
        if c == "\n":
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out).rstrip("\n") + "\n"


def main(argv: list[str]) -> int:
    paths = argv[1:] or ["-"]
    for path in paths:
        raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        sys.stdout.write(show(raw))
        if len(paths) > 1:
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
