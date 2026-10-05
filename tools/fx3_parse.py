#!/usr/bin/env python3
"""FX3 Core parser: lexer token stream → AST with line/column.

P1 slice. Not a lowerer, not a runtime. Core grammar unchanged.
Consumes tokens from fx3_lex.lex; does not re-scan source text.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence, Union

from fx3_lex import Token, lex


@dataclass(frozen=True)
class ParseError(Exception):
    code: str
    message: str
    line: int
    column: int
    offset: int = -1

    def __str__(self) -> str:
        return f"{self.code} {self.line}:{self.column} {self.message}"


# --- AST nodes (every node carries line/column) ---


@dataclass(frozen=True)
class Module:
    kind: str
    forms: tuple
    line: int
    column: int


@dataclass(frozen=True)
class Defn:
    kind: str
    name: str
    params: tuple
    body: "Body"
    line: int
    column: int


@dataclass(frozen=True)
class Body:
    kind: str
    bindings: tuple
    exprs: tuple
    line: int
    column: int


@dataclass(frozen=True)
class Binding:
    kind: str
    name: str
    value: Any
    line: int
    column: int


@dataclass(frozen=True)
class Var:
    kind: str
    name: str
    line: int
    column: int


@dataclass(frozen=True)
class Sym:
    kind: str
    name: str
    line: int
    column: int


@dataclass(frozen=True)
class Num:
    kind: str
    value: str
    line: int
    column: int


@dataclass(frozen=True)
class Str:
    kind: str
    value: str
    line: int
    column: int


@dataclass(frozen=True)
class Call:
    kind: str
    name: str
    args: tuple
    line: int
    column: int


@dataclass(frozen=True)
class Op:
    kind: str
    op: str
    left: Any
    right: Any
    line: int
    column: int


@dataclass(frozen=True)
class If:
    kind: str
    cond: Any
    yes: Any
    no: Any
    line: int
    column: int


@dataclass(frozen=True)
class NullQ:
    kind: str
    value: Any
    line: int
    column: int


@dataclass(frozen=True)
class Get:
    kind: str
    target: Any
    key: Any
    line: int
    column: int


@dataclass(frozen=True)
class Map:
    kind: str
    pairs: tuple
    line: int
    column: int


@dataclass(frozen=True)
class MapPair:
    kind: str
    key: str
    value: Any
    line: int
    column: int


Expr = Union[Var, Sym, Num, Str, Call, Op, If, NullQ, Get, Map]


_BINOP_LEVELS = (
    ("==", "!="),
    (">=", "<=", ">", "<"),
    ("+", "-"),
    ("*", "/"),
)


class Parser:
    def __init__(self, tokens: Sequence[Token]):
        self.tokens = list(tokens)
        self.i = 0

    def parse(self) -> Module:
        start = self._loc_or_eof()
        forms = []
        while self.peek() is not None:
            forms.append(self.parse_defn())
            if self._punct(";"):
                self._eat_punct(";")
                continue
            if self.peek() is not None:
                t = self.peek()
                raise self._err(
                    "E_EXPECTED_SEMI",
                    "expected ';' between top-level forms",
                    t,
                )
        if not forms:
            raise self._err_at(
                "E_EXPECTED_F",
                "expected top-level F",
                start[0],
                start[1],
                -1,
            )
        return Module("module", tuple(forms), start[0], start[1])

    def parse_defn(self) -> Defn:
        t = self.peek()
        if not self._ident_val("F"):
            raise self._err("E_EXPECTED_F", "expected F", t)
        ft = self._eat()
        name_t = self._eat_ident()
        self._eat_punct("[")
        params = []
        if not self._punct("]"):
            params.append(self._eat_var().value)
            while self._punct(","):
                self._eat_punct(",")
                params.append(self._eat_var().value)
        self._eat_punct("]")
        body_l, body_c = self._loc()
        self._eat_punct("{")
        body = self.parse_body(body_l, body_c)
        self._eat_punct("}")
        return Defn("defn", name_t.value, tuple(params), body, ft.line, ft.column)

    def parse_body(self, line: int, column: int) -> Body:
        bindings = []
        exprs = []
        while self.peek() is not None and not self._punct("}"):
            if self._is_binding():
                if exprs:
                    t = self.peek()
                    raise self._err(
                        "E_BINDING_AFTER_EXPR",
                        "binding after expression",
                        t,
                    )
                bt = self.peek()
                name = self._eat_var().value
                self._eat_punct("=")
                bindings.append(
                    Binding("binding", name, self.parse_expr(), bt.line, bt.column)
                )
            else:
                exprs.append(self.parse_expr())
            if self._punct(";"):
                self._eat_punct(";")
                continue
            break
        if not exprs:
            t = self.peek()
            raise self._err("E_EMPTY_BODY", "body needs an expression", t)
        return Body("body", tuple(bindings), tuple(exprs), line, column)

    def parse_expr(self) -> Expr:
        return self._parse_binop(0)

    def _parse_binop(self, level: int) -> Expr:
        if level >= len(_BINOP_LEVELS):
            return self._parse_unary()
        left = self._parse_binop(level + 1)
        ops = _BINOP_LEVELS[level]
        while True:
            t = self.peek()
            if t is None or t.kind != "OP" or t.value not in ops:
                return left
            op_t = self._eat()
            right = self._parse_binop(level + 1)
            left = Op("op", op_t.value, left, right, op_t.line, op_t.column)

    def _parse_unary(self) -> Expr:
        if self._punct("?"):
            qt = self._eat()
            cond = self.parse_expr()
            self._eat_punct("{")
            yes = self.parse_expr()
            self._eat_punct("}")
            self._eat_punct("{")
            no = self.parse_expr()
            self._eat_punct("}")
            return If("if", cond, yes, no, qt.line, qt.column)
        if self._punct("~"):
            tt = self._eat()
            return NullQ("null?", self._parse_unary(), tt.line, tt.column)
        return self._parse_primary()

    def _parse_primary(self) -> Expr:
        if self._punct("@"):
            at = self._eat()
            node: Expr = self._parse_atom()
            while self._punct(".") or self._punct("["):
                if self._punct("."):
                    self._eat_punct(".")
                    key_t = self._eat_ident()
                    key = Str("str", '"' + key_t.value + '"', key_t.line, key_t.column)
                    node = Get("get", node, key, at.line, at.column)
                else:
                    self._eat_punct("[")
                    idx = self.parse_expr()
                    self._eat_punct("]")
                    node = Get("get", node, idx, at.line, at.column)
            return node
        if self._punct("{"):
            return self._parse_map()
        return self._parse_atom()

    def _parse_atom(self) -> Expr:
        t = self.peek()
        if t is None:
            raise self._err_eof("expected expression")
        if t.kind == "VAR":
            self._eat()
            return Var("var", t.value, t.line, t.column)
        if t.kind == "STRING":
            self._eat()
            return Str("str", t.value, t.line, t.column)
        if t.kind == "NUMBER":
            self._eat()
            return Num("num", t.value, t.line, t.column)
        if self._punct("("):
            self._eat_punct("(")
            node = self.parse_expr()
            self._eat_punct(")")
            return node
        if t.kind == "IDENT":
            name_t = self._eat()
            if self._punct("("):
                self._eat_punct("(")
                args = []
                if not self._punct(")"):
                    args.append(self.parse_expr())
                    while self._punct(","):
                        self._eat_punct(",")
                        args.append(self.parse_expr())
                self._eat_punct(")")
                return Call(
                    "call", name_t.value, tuple(args), name_t.line, name_t.column
                )
            return Sym("sym", name_t.value, name_t.line, name_t.column)
        raise self._err("E_UNEXPECTED_TOKEN", f"unexpected {t.value!r}", t)

    def _parse_map(self) -> Map:
        ot = self._eat_punct("{")
        pairs = []
        if not self._punct("}"):
            pairs.append(self._parse_pair())
            while self._punct(","):
                self._eat_punct(",")
                pairs.append(self._parse_pair())
        self._eat_punct("}")
        return Map("map", tuple(pairs), ot.line, ot.column)

    def _parse_pair(self) -> MapPair:
        t = self.peek()
        if t is None:
            raise self._err_eof("expected map key")
        if t.kind == "STRING":
            self._eat()
            key = t.value
            line, column = t.line, t.column
        elif t.kind == "IDENT":
            self._eat()
            key = '"' + t.value + '"'
            line, column = t.line, t.column
        else:
            raise self._err("E_UNEXPECTED_TOKEN", "expected map key", t)
        self._eat_punct(":")
        return MapPair("pair", key, self.parse_expr(), line, column)

    # --- token helpers ---

    def peek(self) -> Optional[Token]:
        if self.i >= len(self.tokens):
            return None
        return self.tokens[self.i]

    def _eat(self) -> Token:
        t = self.peek()
        if t is None:
            raise self._err_eof("unexpected end of input")
        self.i += 1
        return t

    def _punct(self, value: str) -> bool:
        t = self.peek()
        return t is not None and t.kind == "PUNCT" and t.value == value

    def _ident_val(self, value: str) -> bool:
        t = self.peek()
        return t is not None and t.kind == "IDENT" and t.value == value

    def _eat_punct(self, value: str) -> Token:
        t = self.peek()
        if t is None:
            raise self._err_eof(f"expected {value!r}")
        if not (t.kind == "PUNCT" and t.value == value):
            raise self._err(
                "E_EXPECTED_TOKEN",
                f"expected {value!r}",
                t,
            )
        return self._eat()

    def _eat_ident(self) -> Token:
        t = self.peek()
        if t is None:
            raise self._err_eof("expected name")
        if t.kind != "IDENT":
            raise self._err("E_EXPECTED_TOKEN", "expected name", t)
        return self._eat()

    def _eat_var(self) -> Token:
        t = self.peek()
        if t is None:
            raise self._err_eof("expected $name")
        if t.kind != "VAR":
            raise self._err("E_EXPECTED_TOKEN", "expected $name", t)
        return self._eat()

    def _is_binding(self) -> bool:
        """VAR followed by '=' (PUNCT), not '==' (OP)."""
        if self.i + 1 >= len(self.tokens):
            return False
        a = self.tokens[self.i]
        b = self.tokens[self.i + 1]
        return a.kind == "VAR" and b.kind == "PUNCT" and b.value == "="

    def _loc(self) -> tuple:
        t = self.peek()
        if t is None:
            return self._loc_or_eof()
        return t.line, t.column

    def _loc_or_eof(self) -> tuple:
        if self.tokens:
            if self.i < len(self.tokens):
                t = self.tokens[self.i]
                return t.line, t.column
            last = self.tokens[-1]
            return last.line, last.column + max(len(last.value), 1)
        return 1, 1

    def _err(self, code: str, message: str, token: Optional[Token]) -> ParseError:
        if token is None:
            return self._err_eof(message, code=code)
        return ParseError(code, message, token.line, token.column, token.offset)

    def _err_at(self, code: str, message: str, line: int, column: int, offset: int) -> ParseError:
        return ParseError(code, message, line, column, offset)

    def _err_eof(self, message: str, code: str = "E_UNEXPECTED_EOF") -> ParseError:
        line, column = self._loc_or_eof()
        return ParseError(code, message, line, column, -1)


def parse_tokens(tokens: Sequence[Token]) -> Module:
    return Parser(tokens).parse()


def parse_text(text: str) -> Module:
    return parse_tokens(lex(text))


def parse_file(path: str) -> Module:
    with open(path, "r", encoding="utf-8") as f:
        return parse_text(f.read())


def walk(node: Any):
    """Yield all AST nodes depth-first."""
    yield node
    kind = getattr(node, "kind", None)
    if kind == "module":
        for f in node.forms:
            yield from walk(f)
    elif kind == "defn":
        yield from walk(node.body)
    elif kind == "body":
        for b in node.bindings:
            yield from walk(b)
        for e in node.exprs:
            yield from walk(e)
    elif kind == "binding":
        yield from walk(node.value)
    elif kind == "call":
        for a in node.args:
            yield from walk(a)
    elif kind == "op":
        yield from walk(node.left)
        yield from walk(node.right)
    elif kind == "if":
        yield from walk(node.cond)
        yield from walk(node.yes)
        yield from walk(node.no)
    elif kind == "null?":
        yield from walk(node.value)
    elif kind == "get":
        yield from walk(node.target)
        yield from walk(node.key)
    elif kind == "map":
        for p in node.pairs:
            yield from walk(p)
    elif kind == "pair":
        yield from walk(node.value)
