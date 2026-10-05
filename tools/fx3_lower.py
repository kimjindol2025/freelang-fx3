#!/usr/bin/env python3
"""FX3 Core AST → deterministic FreeLang .fl lowering.

P2 slice. Consumes located AST from fx3_parse. Not a runtime.
Does not modify tools/lower.py. Core grammar unchanged.
Identical AST always yields identical UTF-8 bytes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from fx3_lex import lex
from fx3_parse import Module, parse_tokens


@dataclass(frozen=True)
class LowerAstError(Exception):
    code: str
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.code} {self.line}:{self.column} {self.message}"


def _err(node: Any, code: str, message: str) -> LowerAstError:
    line = getattr(node, "line", 1) or 1
    column = getattr(node, "column", 1) or 1
    return LowerAstError(code, message, line, column)


def fmt(node: Any, col: int) -> str:
    kind = getattr(node, "kind", None)
    if kind == "var":
        return node.name
    if kind == "sym":
        return node.name
    if kind == "num":
        return node.value
    if kind == "str":
        return node.value
    if kind == "null?":
        return "(null? " + fmt(node.value, col + 7) + ")"
    if kind == "op":
        left = fmt(node.left, col + len(node.op) + 2)
        right = fmt(node.right, 0)
        return f"({node.op} {left} {right})"
    if kind == "get":
        obj = fmt(node.target, col + 5)
        key = fmt(node.key, 0)
        return f"(get {obj} {key})"
    if kind == "call":
        return fmt_call(node, col)
    if kind == "map":
        return fmt_map(node, col)
    if kind == "if":
        return fmt_if(node, col)
    if kind == "do":
        return fmt_do(node, col)
    if kind == "let":
        return fmt_let(node, col)
    raise _err(node, "E_UNSUPPORTED_NODE", f"unsupported AST node {kind!r}")


def fmt_call(node: Any, col: int) -> str:
    args = list(node.args)
    if len(args) == 1 and getattr(args[0], "kind", None) == "map":
        inner_col = col + len(node.name) + 2
        arg = fmt(args[0], inner_col)
        return f"({node.name} {arg})"
    parts = [fmt(a, 0) for a in args]
    return "(" + node.name + ("" if not parts else " " + " ".join(parts)) + ")"


def fmt_map(node: Any, col: int) -> str:
    pairs = list(node.pairs)
    if not pairs:
        raise _err(node, "E_UNSUPPORTED_NODE", "empty map unsupported in Core lower")
    lines = []
    key_col = col + 1
    for i, pair in enumerate(pairs):
        if getattr(pair, "kind", None) != "pair":
            raise _err(pair, "E_UNSUPPORTED_NODE", "map child must be pair")
        key = pair.key
        vs = fmt(pair.value, key_col + len(key) + 1)
        piece = f"{key} {vs}"
        if i == 0:
            lines.append("{" + piece)
        else:
            lines.append(" " * key_col + piece)
    lines[-1] += "}"
    return "\n".join(lines)


def fmt_if(node: Any, col: int) -> str:
    cond = fmt(node.cond, col + 4)
    yes = fmt(node.yes, col + 2)
    no = fmt(node.no, col + 2)
    pad = " " * (col + 2)
    return f"(if {cond}\n{pad}{yes}\n{pad}{no})"


def fmt_do(node: Any, col: int) -> str:
    exprs = list(node.exprs)
    if not exprs:
        raise _err(node, "E_UNSUPPORTED_NODE", "empty do unsupported")
    lines = ["(do"]
    pad = " " * (col + 2)
    for i, expr in enumerate(exprs):
        line = pad + fmt(expr, col + 2)
        if i == len(exprs) - 1:
            line += ")"
        lines.append(line)
    return "\n".join(lines)


def fmt_let(node: Any, col: int) -> str:
    bindings = list(node.bindings)
    if not bindings:
        raise _err(node, "E_UNSUPPORTED_NODE", "empty let unsupported")
    open_ = "(let ["
    width = max(len(b.name) for b in bindings)
    base = col + len(open_)
    lines = []
    for i, b in enumerate(bindings):
        if getattr(b, "kind", None) != "binding":
            raise _err(b, "E_UNSUPPORTED_NODE", "let child must be binding")
        gap = " " * (width - len(b.name) + 1)
        vs = fmt(b.value, base + width + 1)
        line = f"{b.name}{gap}{vs}"
        if i == 0:
            line = open_ + line
        else:
            line = " " * base + line
        if i == len(bindings) - 1:
            line += "]"
        lines.append(line)
    lines.append(" " * (col + 2) + fmt(node.body, col + 2) + ")")
    return "\n".join(lines)


@dataclass(frozen=True)
class Do:
    kind: str
    exprs: tuple
    line: int
    column: int


@dataclass(frozen=True)
class Let:
    kind: str
    bindings: tuple
    body: Any
    line: int
    column: int


def body_node(body: Any) -> Any:
    if getattr(body, "kind", None) != "body":
        raise _err(body, "E_UNSUPPORTED_NODE", "expected body node")
    bindings = list(body.bindings)
    exprs = list(body.exprs)
    if not exprs:
        raise _err(body, "E_UNSUPPORTED_NODE", "body has no expressions")
    if len(exprs) == 1:
        inner: Any = exprs[0]
    else:
        inner = Do("do", tuple(exprs), body.line, body.column)
    if bindings:
        return Let("let", tuple(bindings), inner, body.line, body.column)
    return inner


def lower_module(mod: Module) -> str:
    if getattr(mod, "kind", None) != "module":
        raise _err(mod, "E_UNSUPPORTED_NODE", "expected module")
    forms = list(mod.forms)
    if len(forms) != 1:
        bad = forms[1] if len(forms) > 1 else (forms[0] if forms else mod)
        raise _err(
            bad,
            "E_UNSUPPORTED_NODE",
            "Core lower accepts exactly one top-level F",
        )
    defn = forms[0]
    if getattr(defn, "kind", None) != "defn":
        raise _err(defn, "E_UNSUPPORTED_NODE", "expected defn")
    rendered = fmt(body_node(defn.body), 2)
    params = " ".join(defn.params)
    return f"(defn {defn.name} [{params}]\n  {rendered})\n"


def lower_text(text: str) -> str:
    return lower_module(parse_tokens(lex(text)))


def lower_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return lower_text(f.read())


def lower_bytes(text: str) -> bytes:
    return lower_text(text).encode("utf-8")
