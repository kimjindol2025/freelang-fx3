#!/usr/bin/env python3
"""FX3 Core lexer skeleton: tokens + line/column + error codes.

P1 slice only. Not a parser, not a lowerer, not a runtime.
Core grammar symbols stay unchanged. lower.py is untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


# Single-char punct that is always its own token.
_PUNCT = set("{}[](),.;:@?~=")

# Multi-char operators longest-first.
_OPS = ("==", "!=", ">=", "<=", ">", "<", "+", "-", "*", "/")


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int
    offset: int


@dataclass(frozen=True)
class LexError(Exception):
    code: str
    message: str
    line: int
    column: int
    offset: int

    def __str__(self) -> str:
        return f"{self.code} {self.line}:{self.column} {self.message}"


class Lexer:
    def __init__(self, text: str):
        self.s = text
        self.n = len(text)
        self.i = 0
        self.line = 1
        self.col = 1

    def lex(self) -> List[Token]:
        out: List[Token] = []
        while True:
            self._skip_ws()
            if self.i >= self.n:
                return out
            out.append(self._next())

    def _mark(self) -> tuple:
        return self.i, self.line, self.col

    def _advance(self, n: int = 1) -> None:
        for _ in range(n):
            if self.i >= self.n:
                return
            ch = self.s[self.i]
            self.i += 1
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1

    def _skip_ws(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\r\n":
            self._advance(1)

    def _err(self, code: str, message: str, offset: int, line: int, column: int) -> LexError:
        return LexError(code, message, line, column, offset)

    def _next(self) -> Token:
        start_i, start_line, start_col = self._mark()
        ch = self.s[self.i]

        if ch == '"':
            return self._string(start_i, start_line, start_col)

        if ch == "$":
            return self._var(start_i, start_line, start_col)

        if ch.isdigit():
            return self._number(start_i, start_line, start_col)

        if ch.isalpha() or ch == "_":
            return self._ident(start_i, start_line, start_col)

        for op in _OPS:
            if self.s.startswith(op, self.i):
                self._advance(len(op))
                return Token("OP", op, start_line, start_col, start_i)

        if ch in _PUNCT:
            self._advance(1)
            return Token("PUNCT", ch, start_line, start_col, start_i)

        raise self._err(
            "E_UNEXPECTED_CHAR",
            f"unexpected {ch!r}",
            start_i,
            start_line,
            start_col,
        )

    def _string(self, start_i: int, start_line: int, start_col: int) -> Token:
        self._advance(1)  # opening "
        chars = ['"']
        while self.i < self.n:
            c = self.s[self.i]
            self._advance(1)
            chars.append(c)
            if c == "\\":
                if self.i >= self.n:
                    raise self._err(
                        "E_UNTERMINATED_STRING",
                        "string not terminated",
                        start_i,
                        start_line,
                        start_col,
                    )
                chars.append(self.s[self.i])
                self._advance(1)
                continue
            if c == '"':
                return Token("STRING", "".join(chars), start_line, start_col, start_i)
        raise self._err(
            "E_UNTERMINATED_STRING",
            "string not terminated",
            start_i,
            start_line,
            start_col,
        )

    def _var(self, start_i: int, start_line: int, start_col: int) -> Token:
        self._advance(1)  # $
        if self.i >= self.n:
            raise self._err("E_BAD_VAR", "expected name after $", start_i, start_line, start_col)
        c = self.s[self.i]
        if not (c.isalpha() or c == "_"):
            raise self._err("E_BAD_VAR", "expected name after $", start_i, start_line, start_col)
        name = self._read_ident_body()
        return Token("VAR", "$" + name, start_line, start_col, start_i)

    def _number(self, start_i: int, start_line: int, start_col: int) -> Token:
        while self.i < self.n and self.s[self.i].isdigit():
            self._advance(1)
        return Token("NUMBER", self.s[start_i : self.i], start_line, start_col, start_i)

    def _ident(self, start_i: int, start_line: int, start_col: int) -> Token:
        name = self._read_ident_body()
        # Leading F at call sites is still IDENT; parser decides keyword.
        return Token("IDENT", name, start_line, start_col, start_i)

    def _read_ident_body(self) -> str:
        """Same kebab rule as lower.py: '-' only before letter/_."""
        start = self.i
        # first char already validated by caller for ident/var
        self._advance(1)
        while self.i < self.n:
            c = self.s[self.i]
            if c.isalnum() or c == "_":
                self._advance(1)
                continue
            if c == "-" and self.i + 1 < self.n:
                nxt = self.s[self.i + 1]
                if nxt.isalpha() or nxt == "_":
                    self._advance(1)
                    continue
            break
        return self.s[start : self.i]


def lex(text: str) -> List[Token]:
    return Lexer(text).lex()


def lex_file(path: str) -> List[Token]:
    with open(path, "r", encoding="utf-8") as f:
        return lex(f.read())
