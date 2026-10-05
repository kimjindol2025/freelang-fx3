#!/usr/bin/env python3
"""FX3 capability judgment (deny-first). Pure function; no I/O.

P4 contract only. Does not execute IR, touch files, spawn processes, or network.
See docs/CAPABILITY-CONTRACT.md.
"""

from __future__ import annotations

import json
import posixpath
from typing import Any, Dict, Optional, Tuple

SCHEMA = "fx3-capability@1"

# Allowable only when args/path/root validate.
ALLOWABLE = frozenset({"source.read", "ir.inspect"})

# Always deny in this stage (even if someone lists them as "known").
ALWAYS_DENY = frozenset(
    {
        "source.write",
        "process.exec",
        "network.request",
        "runtime.execute",
        "filesystem.delete",
    }
)

# Args contracts for allowable caps: required keys only; no extras.
_ARGS_SPEC = {
    "source.read": frozenset({"path"}),
    "ir.inspect": frozenset({"path"}),
}


def serialize_decision(decision: dict) -> str:
    return json.dumps(decision, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def serialize_decision_bytes(decision: dict) -> bytes:
    return serialize_decision(decision).encode("utf-8")


def _result(
    *,
    decision: str,
    capability: Any,
    reason: str,
    path: Any,
    location: Any,
) -> dict:
    return {
        "schema": SCHEMA,
        "decision": decision,
        "capability": capability if isinstance(capability, str) else "",
        "reason": reason,
        "path": path,
        "location": location,
    }


def _normalize_location(raw: Any) -> Tuple[Optional[dict], Optional[str]]:
    """Return (location_or_null, error_reason). Missing/null → (None, None)."""
    if raw is None:
        return None, None
    if not isinstance(raw, dict):
        return None, "invalid_location"
    # reject unknown keys
    if set(raw.keys()) - {"line", "column"}:
        return None, "invalid_location"
    if "line" not in raw or "column" not in raw:
        return None, "invalid_location"
    line = raw["line"]
    column = raw["column"]
    if type(line) is not int or type(column) is not int:
        return None, "invalid_location"
    if line < 1 or column < 1:
        return None, "invalid_location"
    return {"line": line, "column": column}, None


def _is_absolute_path(p: str) -> bool:
    if p.startswith("/"):
        return True
    # Windows-ish drive: C:\ or C:/
    if len(p) >= 2 and p[0].isalpha() and p[1] == ":":
        return True
    return False


def _path_escape(path: str) -> bool:
    if not isinstance(path, str) or path == "":
        return True
    if "\0" in path:
        return True
    if "\\" in path:
        return True
    if _is_absolute_path(path):
        return True
    parts = path.replace("\\", "/").split("/")
    if ".." in parts:
        return True
    return False


def _under_root(root: str, path: str) -> bool:
    """String-level containment after posix normpath. No real FS."""
    if _path_escape(root) or _path_escape(path):
        return False
    # root must be relative non-empty
    if not root or _is_absolute_path(root):
        return False
    joined = posixpath.normpath(posixpath.join(root, path))
    root_n = posixpath.normpath(root)
    if joined == root_n:
        # path resolved to root itself — treat as not a file under root for read
        return False
    prefix = root_n + "/"
    return joined.startswith(prefix)


def decide(request: Any) -> dict:
    """Pure capability decision. Never performs I/O."""
    if not isinstance(request, dict):
        return _result(
            decision="deny",
            capability="",
            reason="invalid_argument",
            path=None,
            location=None,
        )

    # location first so invalid location always wins with clear reason
    loc_out, loc_err = _normalize_location(request.get("location", None))
    if loc_err:
        cap = request.get("capability", "")
        path_val = None
        args = request.get("args")
        if isinstance(args, dict) and isinstance(args.get("path"), str):
            path_val = args.get("path")
        return _result(
            decision="deny",
            capability=cap if isinstance(cap, str) else "",
            reason="invalid_location",
            path=path_val,
            location=None,
        )

    cap = request.get("capability", None)
    if cap is None:
        return _result(
            decision="deny",
            capability="",
            reason="deny_by_default",
            path=None,
            location=loc_out,
        )
    if not isinstance(cap, str):
        return _result(
            decision="deny",
            capability="",
            reason="invalid_argument",
            path=None,
            location=loc_out,
        )
    if cap == "":
        return _result(
            decision="deny",
            capability="",
            reason="empty_capability",
            path=None,
            location=loc_out,
        )

    args = request.get("args", {})
    if args is None:
        args = {}
    if not isinstance(args, dict):
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=None,
            location=loc_out,
        )

    path_val = args.get("path") if "path" in args else None
    if path_val is not None and not isinstance(path_val, str):
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=None,
            location=loc_out,
        )

    # Always-deny list
    if cap in ALWAYS_DENY:
        return _result(
            decision="deny",
            capability=cap,
            reason="deny_by_default",
            path=path_val if isinstance(path_val, str) else None,
            location=loc_out,
        )

    # Unknown
    if cap not in ALLOWABLE:
        return _result(
            decision="deny",
            capability=cap,
            reason="unknown_capability",
            path=path_val if isinstance(path_val, str) else None,
            location=loc_out,
        )

    # Args contract
    allowed_keys = _ARGS_SPEC[cap]
    if set(args.keys()) != allowed_keys:
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=path_val if isinstance(path_val, str) else None,
            location=loc_out,
        )

    path = args["path"]
    if not isinstance(path, str) or path == "":
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=path if isinstance(path, str) else None,
            location=loc_out,
        )

    root = request.get("root", None)
    if not isinstance(root, str) or root == "":
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=path,
            location=loc_out,
        )

    if _path_escape(path) or _path_escape(root) or not _under_root(root, path):
        return _result(
            decision="deny",
            capability=cap,
            reason="path_escape",
            path=path,
            location=loc_out,
        )

    return _result(
        decision="allow",
        capability=cap,
        reason="explicit_allow",
        path=path,
        location=loc_out,
    )


def decide_bytes(request: Any) -> bytes:
    return serialize_decision_bytes(decide(request))
