#!/usr/bin/env python3
"""FX3 AST → deterministic IR/ABI (contract only; no executor).

P3 slice. See docs/IR-ABI-CONTRACT.md.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from fx3_lex import lex
from fx3_parse import parse_tokens

ABI_NAME = "fx3-ir"
ABI_VERSION = 1

ALLOWED_OPS = frozenset(
    {
        "program",
        "function",
        "binding",
        "variable",
        "literal",
        "call",
        "operator",
        "conditional",
        "null_check",
        "get",
        "map",
        "map_entry",
        "result",
    }
)

RESERVED_OPS = frozenset(
    {
        "list",
        "capability_request",
        "error",
        "array",
        "loop",
        "fn",
    }
)

LITERAL_KINDS = frozenset({"number", "string", "symbol"})


@dataclass(frozen=True)
class IrError(Exception):
    code: str
    message: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.code} {self.line}:{self.column} {self.message}"


def _loc_of(node: Any) -> Dict[str, int]:
    line = getattr(node, "line", None)
    column = getattr(node, "column", None)
    if line is None or column is None or line < 1 or column < 1:
        raise IrError(
            "E_UNSUPPORTED_NODE",
            "AST node missing location",
            line if isinstance(line, int) and line >= 1 else 1,
            column if isinstance(column, int) and column >= 1 else 1,
        )
    return {"line": line, "column": column}


def _err_node(node: Any, code: str, message: str) -> IrError:
    try:
        loc = _loc_of(node)
    except IrError as e:
        return IrError(code, message, e.line, e.column)
    return IrError(code, message, loc["line"], loc["column"])


def _err_loc(loc: Optional[dict], code: str, message: str) -> IrError:
    if not loc:
        return IrError(code, message, 1, 1)
    return IrError(
        code,
        message,
        int(loc.get("line", 1)),
        int(loc.get("column", 1)),
    )


def ast_to_ir(mod: Any) -> dict:
    """Convert located Module AST to IR dict."""
    if getattr(mod, "kind", None) != "module":
        raise _err_node(mod, "E_UNSUPPORTED_NODE", "expected module")
    functions = []
    for form in mod.forms:
        functions.append(_fn_from_defn(form))
    if not functions:
        raise _err_node(mod, "E_UNSUPPORTED_NODE", "program needs a function")
    return {
        "abi": ABI_NAME,
        "version": ABI_VERSION,
        "op": "program",
        "loc": _loc_of(mod),
        "functions": functions,
    }


def _fn_from_defn(defn: Any) -> dict:
    if getattr(defn, "kind", None) != "defn":
        raise _err_node(defn, "E_UNSUPPORTED_NODE", "expected defn")
    body = defn.body
    if getattr(body, "kind", None) != "body":
        raise _err_node(body, "E_UNSUPPORTED_NODE", "expected body")
    bindings = [_binding(b) for b in body.bindings]
    exprs = [_expr(e) for e in body.exprs]
    if not exprs:
        raise _err_node(body, "E_UNSUPPORTED_NODE", "function body empty")
    result_val = exprs[-1]
    return {
        "op": "function",
        "name": defn.name,
        "params": list(defn.params),
        "bindings": bindings,
        "body": exprs,
        "result": {
            "op": "result",
            "value": _clone(result_val),
            "loc": dict(result_val["loc"]),
        },
        "loc": _loc_of(defn),
    }


def _binding(b: Any) -> dict:
    if getattr(b, "kind", None) != "binding":
        raise _err_node(b, "E_UNSUPPORTED_NODE", "expected binding")
    return {
        "op": "binding",
        "name": b.name,
        "value": _expr(b.value),
        "loc": _loc_of(b),
    }


def _expr(node: Any) -> dict:
    kind = getattr(node, "kind", None)
    if kind == "var":
        return {"op": "variable", "name": node.name, "loc": _loc_of(node)}
    if kind == "num":
        return {
            "op": "literal",
            "kind": "number",
            "text": node.value,
            "loc": _loc_of(node),
        }
    if kind == "str":
        return {
            "op": "literal",
            "kind": "string",
            "text": node.value,
            "loc": _loc_of(node),
        }
    if kind == "sym":
        return {
            "op": "literal",
            "kind": "symbol",
            "text": node.name,
            "loc": _loc_of(node),
        }
    if kind == "call":
        return {
            "op": "call",
            "name": node.name,
            "args": [_expr(a) for a in node.args],
            "loc": _loc_of(node),
        }
    if kind == "op":
        return {
            "op": "operator",
            "name": node.op,
            "left": _expr(node.left),
            "right": _expr(node.right),
            "loc": _loc_of(node),
        }
    if kind == "if":
        return {
            "op": "conditional",
            "cond": _expr(node.cond),
            "then": _expr(node.yes),
            "else": _expr(node.no),
            "loc": _loc_of(node),
        }
    if kind == "null?":
        return {
            "op": "null_check",
            "value": _expr(node.value),
            "loc": _loc_of(node),
        }
    if kind == "get":
        return {
            "op": "get",
            "target": _expr(node.target),
            "key": _expr(node.key),
            "loc": _loc_of(node),
        }
    if kind == "map":
        return {
            "op": "map",
            "entries": [_map_entry(p) for p in node.pairs],
            "loc": _loc_of(node),
        }
    if kind in RESERVED_OPS or kind in {"do", "let", "loop", "fn", "future"}:
        raise _err_node(node, "E_UNSUPPORTED_NODE", f"unsupported AST node {kind!r}")
    raise _err_node(node, "E_UNSUPPORTED_NODE", f"unsupported AST node {kind!r}")


def _map_entry(pair: Any) -> dict:
    if getattr(pair, "kind", None) != "pair":
        raise _err_node(pair, "E_UNSUPPORTED_NODE", "expected map pair")
    return {
        "op": "map_entry",
        "key": pair.key,
        "value": _expr(pair.value),
        "loc": _loc_of(pair),
    }


def _clone(obj: Any) -> Any:
    return json.loads(json.dumps(obj, ensure_ascii=False, sort_keys=True))


def serialize_ir(ir: dict) -> str:
    """Deterministic JSON text (no trailing newline)."""
    return json.dumps(ir, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def serialize_ir_bytes(ir: dict) -> bytes:
    return serialize_ir(ir).encode("utf-8")


def validate_ir(ir: Any) -> None:
    if not isinstance(ir, dict):
        raise IrError("E_UNSUPPORTED_NODE", "IR root must be object", 1, 1)
    if ir.get("abi") != ABI_NAME:
        raise _err_loc(ir.get("loc"), "E_UNSUPPORTED_NODE", f"bad abi {ir.get('abi')!r}")
    if ir.get("version") != ABI_VERSION:
        raise _err_loc(
            ir.get("loc"),
            "E_UNSUPPORTED_NODE",
            f"bad version {ir.get('version')!r}",
        )
    _validate_node(ir, expected_op="program")


def _require_keys(node: dict, keys: Sequence[str]) -> None:
    for k in keys:
        if k not in node:
            raise _err_loc(node.get("loc"), "E_UNSUPPORTED_NODE", f"missing field {k!r}")


def _validate_loc(node: dict) -> None:
    loc = node.get("loc")
    if not isinstance(loc, dict):
        raise IrError("E_UNSUPPORTED_NODE", "missing loc", 1, 1)
    line = loc.get("line")
    column = loc.get("column")
    if not isinstance(line, int) or not isinstance(column, int) or line < 1 or column < 1:
        raise IrError(
            "E_UNSUPPORTED_NODE",
            "invalid loc",
            line if isinstance(line, int) else 1,
            column if isinstance(column, int) else 1,
        )
    # VERSION 1: reject unknown loc keys except reserved span absence
    extra = set(loc.keys()) - {"line", "column"}
    if extra:
        raise _err_loc(loc, "E_UNSUPPORTED_NODE", f"unknown loc fields {sorted(extra)}")


def _validate_node(node: Any, expected_op: Optional[str] = None) -> None:
    if not isinstance(node, dict):
        raise IrError("E_UNSUPPORTED_NODE", "node must be object", 1, 1)
    _require_keys(node, ["op", "loc"])
    _validate_loc(node)
    op = node["op"]
    if op in RESERVED_OPS:
        raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", f"reserved op {op!r}")
    if op not in ALLOWED_OPS:
        raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", f"unknown op {op!r}")
    if expected_op is not None and op != expected_op:
        raise _err_loc(
            node["loc"],
            "E_UNSUPPORTED_NODE",
            f"expected op {expected_op!r} got {op!r}",
        )

    if op == "program":
        _require_keys(node, ["abi", "version", "functions"])
        # only known root keys
        _reject_unknown(
            node,
            {"abi", "version", "op", "loc", "functions"},
        )
        fns = node["functions"]
        if not isinstance(fns, list) or not fns:
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "functions must be non-empty")
        for fn in fns:
            _validate_node(fn, expected_op="function")
        return

    if op == "function":
        _require_keys(node, ["name", "params", "bindings", "body", "result"])
        _reject_unknown(
            node,
            {"op", "loc", "name", "params", "bindings", "body", "result"},
        )
        if not isinstance(node["name"], str) or not node["name"]:
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad function name")
        if not isinstance(node["params"], list) or not all(
            isinstance(p, str) for p in node["params"]
        ):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad params")
        if not isinstance(node["bindings"], list):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad bindings")
        for b in node["bindings"]:
            _validate_node(b, expected_op="binding")
        body = node["body"]
        if not isinstance(body, list) or not body:
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "body must be non-empty")
        for e in body:
            _validate_expr(e)
        _validate_node(node["result"], expected_op="result")
        if node["result"]["value"] != body[-1]:
            raise _err_loc(
                node["result"]["loc"],
                "E_UNSUPPORTED_NODE",
                "result.value must equal body[-1]",
            )
        return

    if op == "binding":
        _require_keys(node, ["name", "value"])
        _reject_unknown(node, {"op", "loc", "name", "value"})
        if not isinstance(node["name"], str) or not node["name"].startswith("$"):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad binding name")
        _validate_expr(node["value"])
        return

    if op == "result":
        _require_keys(node, ["value"])
        _reject_unknown(node, {"op", "loc", "value"})
        _validate_expr(node["value"])
        return

    if op == "variable":
        _require_keys(node, ["name"])
        _reject_unknown(node, {"op", "loc", "name"})
        if not isinstance(node["name"], str) or not node["name"].startswith("$"):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad variable name")
        return

    if op == "literal":
        _require_keys(node, ["kind", "text"])
        _reject_unknown(node, {"op", "loc", "kind", "text"})
        if node["kind"] not in LITERAL_KINDS:
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", f"bad literal kind")
        if not isinstance(node["text"], str):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "literal text must be str")
        return

    if op == "call":
        _require_keys(node, ["name", "args"])
        _reject_unknown(node, {"op", "loc", "name", "args"})
        if not isinstance(node["name"], str) or not node["name"]:
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad call name")
        if not isinstance(node["args"], list):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad args")
        for a in node["args"]:
            _validate_expr(a)
        return

    if op == "operator":
        _require_keys(node, ["name", "left", "right"])
        _reject_unknown(node, {"op", "loc", "name", "left", "right"})
        if not isinstance(node["name"], str):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad operator name")
        _validate_expr(node["left"])
        _validate_expr(node["right"])
        return

    if op == "conditional":
        _require_keys(node, ["cond", "then", "else"])
        _reject_unknown(node, {"op", "loc", "cond", "then", "else"})
        _validate_expr(node["cond"])
        _validate_expr(node["then"])
        _validate_expr(node["else"])
        return

    if op == "null_check":
        _require_keys(node, ["value"])
        _reject_unknown(node, {"op", "loc", "value"})
        _validate_expr(node["value"])
        return

    if op == "get":
        _require_keys(node, ["target", "key"])
        _reject_unknown(node, {"op", "loc", "target", "key"})
        _validate_expr(node["target"])
        _validate_expr(node["key"])
        return

    if op == "map":
        _require_keys(node, ["entries"])
        _reject_unknown(node, {"op", "loc", "entries"})
        if not isinstance(node["entries"], list):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad entries")
        for e in node["entries"]:
            _validate_node(e, expected_op="map_entry")
        return

    if op == "map_entry":
        _require_keys(node, ["key", "value"])
        _reject_unknown(node, {"op", "loc", "key", "value"})
        if not isinstance(node["key"], str):
            raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", "bad map key")
        _validate_expr(node["value"])
        return

    raise _err_loc(node["loc"], "E_UNSUPPORTED_NODE", f"unhandled op {op!r}")


def _validate_expr(node: Any) -> None:
    if not isinstance(node, dict) or "op" not in node:
        raise IrError("E_UNSUPPORTED_NODE", "bad expr", 1, 1)
    op = node["op"]
    if op in {"program", "function", "binding", "result", "map_entry"}:
        raise _err_loc(node.get("loc"), "E_UNSUPPORTED_NODE", f"{op} not an expr")
    _validate_node(node)


def _reject_unknown(node: dict, allowed: set) -> None:
    extra = set(node.keys()) - allowed
    if extra:
        raise _err_loc(
            node.get("loc"),
            "E_UNSUPPORTED_NODE",
            f"unknown fields {sorted(extra)}",
        )


def ir_from_text(text: str) -> dict:
    ir = ast_to_ir(parse_tokens(lex(text)))
    validate_ir(ir)
    return ir


def ir_bytes_from_text(text: str) -> bytes:
    return serialize_ir_bytes(ir_from_text(text))


def ir_from_file(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return ir_from_text(f.read())
