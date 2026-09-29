#!/usr/bin/env python3
"""Minimal evaluator for FX3-lowered .fl Core subset. Not a full FX runtime."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


class EvalError(Exception):
    pass


def tokenize(src: str) -> list[str]:
    src = re.sub(r";.*?$", "", src, flags=re.M)
    out: list[str] = []
    i = 0
    n = len(src)
    while i < n:
        ch = src[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "()[]{}":
            out.append(ch)
            i += 1
            continue
        if ch == '"':
            j = i + 1
            while j < n:
                if src[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if src[j] == '"':
                    j += 1
                    break
                j += 1
            out.append(src[i:j])
            i = j
            continue
        j = i
        while j < n and not src[j].isspace() and src[j] not in "()[]{}":
            j += 1
        out.append(src[i:j])
        i = j
    return out


def parse(tokens: list[str]) -> list[Any]:
    def rec(i: int) -> tuple[Any, int]:
        if i >= len(tokens):
            raise EvalError("unexpected end")
        t = tokens[i]
        if t == "(":
            forms: list[Any] = []
            i += 1
            while i < len(tokens) and tokens[i] != ")":
                node, i = rec(i)
                forms.append(node)
            if i >= len(tokens) or tokens[i] != ")":
                raise EvalError("missing )")
            return forms, i + 1
        if t == "[":
            forms = []
            i += 1
            while i < len(tokens) and tokens[i] != "]":
                node, i = rec(i)
                forms.append(node)
            if i >= len(tokens) or tokens[i] != "]":
                raise EvalError("missing ]")
            return ("vector", forms), i + 1
        if t == "{":
            forms = []
            i += 1
            while i < len(tokens) and tokens[i] != "}":
                node, i = rec(i)
                forms.append(node)
            if i >= len(tokens) or tokens[i] != "}":
                raise EvalError("missing }")
            if len(forms) % 2 != 0:
                raise EvalError("map pairs")
            pairs = [(forms[k], forms[k + 1]) for k in range(0, len(forms), 2)]
            return ("map", pairs), i + 1
        if t.startswith('"'):
            return ("str", json.loads(t)), i + 1
        if re.fullmatch(r"-?\d+", t):
            return ("num", int(t)), i + 1
        if t in ("true", "false", "nil"):
            return ("lit", {"true": True, "false": False, "nil": None}[t]), i + 1
        if t.startswith("$"):
            return ("var", t), i + 1
        return ("sym", t), i + 1

    forms: list[Any] = []
    i = 0
    while i < len(tokens):
        node, i = rec(i)
        forms.append(node)
    return forms


def ev(node: Any, env: dict[str, Any], fns: dict[str, Any]) -> Any:
    if isinstance(node, list):
        if not node:
            raise EvalError("empty form")
        head = node[0]
        if not (isinstance(head, tuple) and head[0] == "sym"):
            raise EvalError("bad call head")
        op = head[1]
        if op == "defn":
            name = node[1][1]
            params = node[2][1] if node[2][0] == "vector" else []
            fns[name] = (params, node[3])
            return name
        if op == "let":
            binds = node[1][1] if node[1][0] == "vector" else []
            local = dict(env)
            for bi in range(0, len(binds), 2):
                local[binds[bi][1]] = ev(binds[bi + 1], local, fns)
            return ev(node[2], local, fns)
        if op == "do":
            val = None
            for part in node[1:]:
                val = ev(part, env, fns)
            return val
        if op == "if":
            return ev(node[2], env, fns) if ev(node[1], env, fns) else ev(node[3], env, fns)
        if op == "null?":
            return ev(node[1], env, fns) is None
        if op == "get":
            obj = ev(node[1], env, fns)
            key = ev(node[2], env, fns)
            if isinstance(obj, dict):
                return obj.get(key)
            if isinstance(obj, (list, tuple)) and isinstance(key, int):
                return obj[key]
            raise EvalError("get on bad object")
        if op in ("+", "-", "*", "/", ">=", ">", "<=", "<", "==", "!="):
            vals = [ev(a, env, fns) for a in node[1:]]
            a0, a1 = vals[0], vals[1]
            if op == "+":
                return a0 + a1
            if op == "-":
                return a0 - a1
            if op == "*":
                return a0 * a1
            if op == "/":
                return a0 // a1
            if op == ">=":
                return a0 >= a1
            if op == ">":
                return a0 > a1
            if op == "<=":
                return a0 <= a1
            if op == "<":
                return a0 < a1
            if op == "==":
                return a0 == a1
            if op == "!=":
                return a0 != a1
        if op in fns:
            params, body = fns[op]
            args = [ev(a, env, fns) for a in node[1:]]
            local = dict(env)
            for p, a in zip(params, args):
                local[p[1]] = a
            return ev(body, local, fns)
        raise EvalError(f"unknown op {op}")
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "str":
        return node[1]
    if kind == "lit":
        return node[1]
    if kind == "var":
        if node[1] not in env:
            raise EvalError(f"unbound {node[1]}")
        return env[node[1]]
    if kind == "sym":
        return node[1]
    if kind == "map":
        return {ev(k, env, fns): ev(v, env, fns) for k, v in node[1]}
    if kind == "vector":
        return [ev(x, env, fns) for x in node[1]]
    raise EvalError(f"bad node {node}")


def load_program(src: str) -> dict[str, Any]:
    fns: dict[str, Any] = {}
    env: dict[str, Any] = {}
    for form in parse(tokenize(src)):
        ev(form, env, fns)
    return fns


def call(fns: dict[str, Any], name: str, args: list[Any]) -> Any:
    if name not in fns:
        if len(fns) == 1:
            name = next(iter(fns))
        else:
            raise EvalError(f"no function {name}; have {list(fns)}")
    params, body = fns[name]
    env = {p[1]: a for p, a in zip(params, args)}
    return ev(body, env, fns)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fl")
    ap.add_argument("--call", default="AUTO")
    ap.add_argument("--args-json", required=True)
    ap.add_argument("--expect-json", required=True)
    args = ap.parse_args(argv)
    fns = load_program(Path(args.fl).read_text(encoding="utf-8"))
    got = call(fns, args.call, json.loads(args.args_json))
    exp = json.loads(args.expect_json)
    if got != exp:
        print(f"FAIL got={got!r} expect={exp!r}", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
