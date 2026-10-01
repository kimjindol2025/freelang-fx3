#!/usr/bin/env python3
"""fixture 01–04만 canonical .fl 바이트로 내린다. 런타임이 아니다."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
PAIRS = [
    "handle-rate-single",
    "check-and-log",
    "make-result",
    "first-id",
]


class LowerError(Exception):
    pass


class Parser:
    def __init__(self, text: str):
        self.s = text
        self.i = 0
        self.n = len(text)

    def skip(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\r\n":
            self.i += 1

    def peek(self) -> str:
        self.skip()
        return self.s[self.i] if self.i < self.n else ""

    def starts(self, token: str) -> bool:
        self.skip()
        return self.s.startswith(token, self.i)

    def eat(self, token: str) -> None:
        self.skip()
        if not self.s.startswith(token, self.i):
            raise LowerError(f"기대 {token!r} 위치 {self.i}")
        self.i += len(token)

    def ident(self) -> str:
        # 케밥 이름(handle-rate)은 유지하고, `$a-$b`의 `-`는 뺄셈으로 남긴다.
        # `-`는 뒤에 이름 문자(letter/digit/_)가 올 때만 이름에 포함한다.
        self.skip()
        start = self.i
        if start >= self.n or not (self.s[start].isalpha() or self.s[start] == "_"):
            raise LowerError(f"이름 없음 위치 {self.i}")
        self.i += 1
        while self.i < self.n:
            c = self.s[self.i]
            if c.isalnum() or c == "_":
                self.i += 1
                continue
            # 케밥은 글자/_ 만 (`handle-rate`). `$n-1`의 `-`는 뺄셈이다.
            if c == "-" and self.i + 1 < self.n:
                nxt = self.s[self.i + 1]
                if nxt.isalpha() or nxt == "_":
                    self.i += 1
                    continue
            break
        return self.s[start : self.i]

    def number(self) -> str:
        self.skip()
        start = self.i
        if start >= self.n or not self.s[start].isdigit():
            raise LowerError(f"숫자 없음 위치 {self.i}")
        while self.i < self.n and self.s[self.i].isdigit():
            self.i += 1
        return self.s[start : self.i]

    def string(self) -> str:
        self.eat('"')
        out = ['"']
        while self.i < self.n:
            c = self.s[self.i]
            self.i += 1
            out.append(c)
            if c == "\\":
                if self.i >= self.n:
                    raise LowerError("문자열이 끝나지 않음")
                out.append(self.s[self.i])
                self.i += 1
                continue
            if c == '"':
                return "".join(out)
        raise LowerError("문자열이 끝나지 않음")

    def parse(self) -> list:
        forms = []
        while self.peek():
            if self.peek() != "F":
                raise LowerError("최소 구현은 최상위 F만 내린다")
            forms.append(self.parse_defn())
            if self.peek() == ";":
                self.eat(";")
        return forms

    def parse_defn(self) -> tuple:
        self.eat("F")
        name = self.ident()
        self.eat("[")
        params = []
        if self.peek() != "]":
            params.append(self.parse_param())
            while self.peek() == ",":
                self.eat(",")
                params.append(self.parse_param())
        self.eat("]")
        self.eat("{")
        body = self.parse_body()
        self.eat("}")
        return ("defn", name, params, body)

    def parse_param(self) -> str:
        self.eat("$")
        return "$" + self.ident()

    def is_binding(self) -> bool:
        mark = self.i
        try:
            self.skip()
            if self.peek() != "$":
                return False
            self.eat("$")
            self.ident()
            return self.peek() == "=" and not self.starts("==")
        finally:
            self.i = mark

    def parse_body(self) -> tuple:
        bindings = []
        exprs = []
        while self.peek() and self.peek() != "}":
            if self.is_binding():
                if exprs:
                    raise LowerError("첫 일반식 뒤의 바인딩은 오류")
                self.eat("$")
                name = "$" + self.ident()
                self.eat("=")
                bindings.append((name, self.parse_expr()))
            else:
                exprs.append(self.parse_expr())
            if self.peek() == ";":
                self.eat(";")
                continue
            break
        if not exprs:
            raise LowerError("본문 식이 없음")
        return ("body", bindings, exprs)

    def parse_expr(self):
        return self.parse_binop(0)

    def parse_binop(self, level: int):
        levels = [
            [("==", "=="), ("!=", "!=")],
            [(">=", ">="), ("<=", "<="), (">", ">"), ("<", "<")],
            [("+", "+"), ("-", "-")],
            [("*", "*"), ("/", "/")],
        ]
        if level >= len(levels):
            return self.parse_unary()
        left = self.parse_binop(level + 1)
        while True:
            found = None
            for op, fl in levels[level]:
                if self.starts(op):
                    found = (op, fl)
                    break
            if not found:
                return left
            self.eat(found[0])
            right = self.parse_binop(level + 1)
            left = ("op", found[1], left, right)

    def parse_unary(self):
        if self.peek() == "?":
            self.eat("?")
            cond = self.parse_expr()
            self.eat("{")
            yes = self.parse_expr()
            self.eat("}")
            self.eat("{")
            no = self.parse_expr()
            self.eat("}")
            return ("if", cond, yes, no)
        if self.peek() == "~":
            self.eat("~")
            return ("null?", self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        ch = self.peek()
        if ch == "@":
            self.eat("@")
            node = self.parse_atom()
            while self.peek() in ".[":
                if self.peek() == ".":
                    self.eat(".")
                    node = ("get", node, ("str", '"' + self.ident() + '"'))
                else:
                    self.eat("[")
                    idx = self.parse_expr()
                    self.eat("]")
                    node = ("get", node, idx)
            return node
        if ch == "{":
            return self.parse_map()
        return self.parse_atom()

    def parse_atom(self):
        ch = self.peek()
        if ch == "$":
            self.eat("$")
            return ("var", "$" + self.ident())
        if ch == '"':
            return ("str", self.string())
        if ch.isdigit():
            return ("num", self.number())
        if ch == "(":
            self.eat("(")
            node = self.parse_expr()
            self.eat(")")
            return node
        name = self.ident()
        if self.peek() == "(":
            self.eat("(")
            args = []
            if self.peek() != ")":
                args.append(self.parse_expr())
                while self.peek() == ",":
                    self.eat(",")
                    args.append(self.parse_expr())
            self.eat(")")
            return ("call", name, args)
        return ("sym", name)

    def parse_map(self):
        self.eat("{")
        pairs = []
        if self.peek() != "}":
            pairs.append(self.parse_pair())
            while self.peek() == ",":
                self.eat(",")
                pairs.append(self.parse_pair())
        self.eat("}")
        return ("map", pairs)

    def parse_pair(self):
        if self.peek() == '"':
            key = self.string()
        else:
            key = '"' + self.ident() + '"'
        self.eat(":")
        return (key, self.parse_expr())


def fmt(node, col: int) -> str:
    kind = node[0]
    if kind == "var":
        return node[1]
    if kind == "sym":
        return node[1]
    if kind == "num":
        return node[1]
    if kind == "str":
        return node[1]
    if kind == "null?":
        return "(null? " + fmt(node[1], col + 7) + ")"
    if kind == "op":
        left = fmt(node[2], col + len(node[1]) + 2)
        right = fmt(node[3], 0)
        return f"({node[1]} {left} {right})"
    if kind == "get":
        obj = fmt(node[1], col + 5)
        key = fmt(node[2], 0)
        return f"(get {obj} {key})"
    if kind == "call":
        return fmt_call(node[1], node[2], col)
    if kind == "map":
        return fmt_map(node[1], col)
    if kind == "if":
        return fmt_if(node, col)
    if kind == "do":
        return fmt_do(node[1], col)
    if kind == "let":
        return fmt_let(node[1], node[2], col)
    raise LowerError(f"출력 불가 {kind}")


def fmt_call(name: str, args: list, col: int) -> str:
    if len(args) == 1 and args[0][0] == "map":
        inner_col = col + len(name) + 2
        arg = fmt(args[0], inner_col)
        return f"({name} {arg})"
    parts = [fmt(a, 0) for a in args]
    return "(" + name + ("" if not parts else " " + " ".join(parts)) + ")"


def fmt_map(pairs: list, col: int) -> str:
    lines = []
    key_col = col + 1
    for i, (key, val) in enumerate(pairs):
        vs = fmt(val, key_col + len(key) + 1)
        piece = f"{key} {vs}"
        if i == 0:
            lines.append("{" + piece)
        else:
            lines.append(" " * key_col + piece)
    lines[-1] += "}"
    return "\n".join(lines)


def fmt_if(node, col: int) -> str:
    cond = fmt(node[1], col + 4)
    yes = fmt(node[2], col + 2)
    no = fmt(node[3], col + 2)
    pad = " " * (col + 2)
    return f"(if {cond}\n{pad}{yes}\n{pad}{no})"


def fmt_do(exprs: list, col: int) -> str:
    lines = ["(do"]
    pad = " " * (col + 2)
    for i, expr in enumerate(exprs):
        line = pad + fmt(expr, col + 2)
        if i == len(exprs) - 1:
            line += ")"
        lines.append(line)
    return "\n".join(lines)


def fmt_let(bindings: list, body, col: int) -> str:
    open_ = "(let ["
    width = max(len(name) for name, _ in bindings)
    base = col + len(open_)
    lines = []
    for i, (name, val) in enumerate(bindings):
        gap = " " * (width - len(name) + 1)
        vs = fmt(val, base + width + 1)
        line = f"{name}{gap}{vs}"
        if i == 0:
            line = open_ + line
        else:
            line = " " * base + line
        if i == len(bindings) - 1:
            line += "]"
        lines.append(line)
    lines.append(" " * (col + 2) + fmt(body, col + 2) + ")")
    return "\n".join(lines)


def body_node(body) -> tuple:
    _, bindings, exprs = body
    if len(exprs) == 1:
        inner = exprs[0]
    else:
        inner = ("do", exprs)
    if bindings:
        return ("let", bindings, inner)
    return inner


def lower_text(text: str) -> str:
    forms = Parser(text).parse()
    if len(forms) != 1:
        raise LowerError("최소 구현은 F 하나")
    _, name, params, body = forms[0]
    rendered = fmt(body_node(body), 2)
    return f"(defn {name} [{' '.join(params)}]\n  {rendered})\n"


def check() -> int:
    failed = 0
    for stem in PAIRS:
        src = (EXAMPLES / f"{stem}.fx3").read_text(encoding="utf-8")
        got = lower_text(src).encode("utf-8")
        want = (EXAMPLES / f"{stem}.fl").read_bytes()
        if got != want:
            failed += 1
            print(f"FAIL {stem}")
            print("--- got ---")
            print(got.decode())
            print("--- want ---")
            print(want.decode())
        else:
            print(f"PASS {stem}")
    return 1 if failed else 0


def main(argv: list[str]) -> int:
    if "--check" in argv:
        return check()
    paths = [a for a in argv[1:] if not a.startswith("-")]
    if not paths:
        sys.stdout.write(lower_text(sys.stdin.read()))
        return 0
    for path in paths:
        sys.stdout.write(lower_text(Path(path).read_text(encoding="utf-8")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except LowerError as err:
        print(f"ERROR {err}", file=sys.stderr)
        raise SystemExit(1)
