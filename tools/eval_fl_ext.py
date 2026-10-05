#!/usr/bin/env python3
"""Eval extension for delegated fx3 run — stdlib shims over eval_fl_min.

Does not modify eval_fl_min.py. Adds keys/length/type-of/str_length and
safe vector get (oob → None) so Core-lowered programs that call existing FX
builtins can run equivalently on --engine=eval.

Not an owned FX3 VM.
"""

from __future__ import annotations

from typing import Any

import eval_fl_min as base

EvalError = base.EvalError
tokenize = base.tokenize
parse = base.parse

_base_ev = base.ev


def _type_of(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, dict):
        return "map"
    if isinstance(value, (list, tuple)):
        return "array"
    return "unknown"


def _length(value: Any) -> int:
    if isinstance(value, (list, tuple, dict, str)):
        return len(value)
    raise EvalError(f"length on bad value {_type_of(value)}")


def _keys(value: Any) -> list[Any]:
    if not isinstance(value, dict):
        raise EvalError("keys on non-map")
    return list(value.keys())


def _str_length(value: Any) -> int:
    if not isinstance(value, str):
        raise EvalError("str_length on non-string")
    return len(value)


def ev(node: Any, env: dict[str, Any], fns: dict[str, Any]) -> Any:
    if isinstance(node, list) and node:
        head = node[0]
        if isinstance(head, tuple) and head[0] == "sym":
            op = head[1]
            if op == "keys":
                if len(node) != 2:
                    raise EvalError("keys arity")
                return _keys(ev(node[1], env, fns))
            if op == "length":
                if len(node) != 2:
                    raise EvalError("length arity")
                return _length(ev(node[1], env, fns))
            if op == "type-of":
                if len(node) != 2:
                    raise EvalError("type-of arity")
                return _type_of(ev(node[1], env, fns))
            if op == "str_length":
                if len(node) != 2:
                    raise EvalError("str_length arity")
                return _str_length(ev(node[1], env, fns))
            if op == "get":
                if len(node) != 3:
                    raise EvalError("get arity")
                obj = ev(node[1], env, fns)
                key = ev(node[2], env, fns)
                if isinstance(obj, dict):
                    return obj.get(key)
                if isinstance(obj, (list, tuple)) and isinstance(key, int):
                    if key < 0 or key >= len(obj):
                        return None
                    return obj[key]
                return None
    return _base_ev(node, env, fns)


# Ensure recursive evaluation inside eval_fl_min hits the extended builtins.
base.ev = ev


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
