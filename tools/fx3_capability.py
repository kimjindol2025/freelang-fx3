#!/usr/bin/env python3
"""FX3 capability judgment (deny-first). Pure function; no filesystem I/O.

P4 contract alignment. See docs/CAPABILITY-CONTRACT.md.
Server supplies canonical_root; requesters cannot set root.
Optional in-memory content bytes enable size/UTF-8 checks without disk I/O.
"""

from __future__ import annotations

import json
import posixpath
from typing import Any, Optional, Tuple

SCHEMA = "fx3-capability@1"
MAX_BYTES = 262144

ALLOWABLE = frozenset({"source.read", "ir.inspect"})

ALWAYS_DENY = frozenset(
    {
        "source.write",
        "process.exec",
        "network.request",
        "runtime.execute",
        "filesystem.delete",
        "filesystem.rename",
    }
)

_ARGS_SPEC = {
    "source.read": frozenset({"path"}),
    "ir.inspect": frozenset({"path"}),
}

_EXTENSION = {
    "source.read": ".fx3",
    "ir.inspect": ".ir.json",
}

# Request JSON top-level keys only. root/canonical_root/others → invalid_argument.
_ALLOWED_TOP_LEVEL = frozenset({"capability", "args", "location"})

# Default server root for tests/tools when caller omits context.
# Real deployments must pass an explicit server-configured root.
DEFAULT_CANONICAL_ROOT = "/canonical/root"


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
    if raw is None:
        return None, None
    if not isinstance(raw, dict):
        return None, "invalid_location"
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
    if len(p) >= 2 and p[0].isalpha() and p[1] == ":":
        return True
    return False


def _path_escape_rel(path: str) -> bool:
    if not isinstance(path, str) or path == "":
        return True
    if "\0" in path or "\\" in path:
        return True
    if _is_absolute_path(path):
        return True
    return ".." in path.split("/")


def _has_wildcard(path: str) -> bool:
    """Reject glob / recursive path patterns (*, **, ?). No glob expansion."""
    if not isinstance(path, str):
        return True
    # '**' is covered by '*'
    return "*" in path or "?" in path


def _under_canonical_root(canonical_root: str, path: str) -> bool:
    """String-level confinement. No real FS, no symlink follow."""
    if _path_escape_rel(path):
        return False
    if not isinstance(canonical_root, str) or canonical_root == "" or "\0" in canonical_root:
        return False
    root_n = posixpath.normpath(canonical_root)
    joined = posixpath.normpath(posixpath.join(root_n, path))
    if joined == root_n:
        return False
    if root_n == "/":
        return joined.startswith("/") and joined != "/"
    prefix = root_n.rstrip("/") + "/"
    return joined.startswith(prefix)


def _extension_ok(capability: str, path: str) -> bool:
    suf = _EXTENSION[capability]
    base = posixpath.basename(path)
    return base.endswith(suf)


def decide(
    request: Any,
    *,
    canonical_root: str = DEFAULT_CANONICAL_ROOT,
    content: Optional[bytes] = None,
) -> dict:
    """Pure capability decision.

    canonical_root: server-configured fixed workspace root (not from request).
    content: optional in-memory bytes for MAX_BYTES / UTF-8 strict checks.
             Never reads or writes the filesystem.
    """
    if not isinstance(request, dict):
        return _result(
            decision="deny",
            capability="",
            reason="invalid_argument",
            path=None,
            location=None,
        )

    # Reject root, canonical_root, and any other unknown top-level keys first.
    extra_top = set(request.keys()) - _ALLOWED_TOP_LEVEL
    if extra_top:
        loc_probe, loc_err_probe = _normalize_location(request.get("location", None))
        loc_out = None if loc_err_probe else loc_probe
        cap = request.get("capability", "")
        return _result(
            decision="deny",
            capability=cap if isinstance(cap, str) else "",
            reason="invalid_argument",
            path=None,
            location=loc_out,
        )

    loc_out, loc_err = _normalize_location(request.get("location", None))
    if loc_err:
        cap = request.get("capability", "")
        return _result(
            decision="deny",
            capability=cap if isinstance(cap, str) else "",
            reason="invalid_location",
            path=None,
            location=None,
        )

    if not isinstance(canonical_root, str) or canonical_root == "":
        return _result(
            decision="deny",
            capability="",
            reason="invalid_argument",
            path=None,
            location=loc_out,
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

    # Always-deny: do not inspect args (rename source/destination untouched).
    if cap in ALWAYS_DENY:
        return _result(
            decision="deny",
            capability=cap,
            reason="deny_by_default",
            path=None,
            location=loc_out,
        )

    if cap not in ALLOWABLE:
        return _result(
            decision="deny",
            capability=cap,
            reason="unknown_capability",
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

    if set(args.keys()) != _ARGS_SPEC[cap]:
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=args.get("path") if isinstance(args.get("path"), str) else None,
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

    if _path_escape_rel(path) or not _under_canonical_root(canonical_root, path):
        return _result(
            decision="deny",
            capability=cap,
            reason="path_escape",
            path=path,
            location=loc_out,
        )

    if _has_wildcard(path):
        return _result(
            decision="deny",
            capability=cap,
            reason="invalid_argument",
            path=path,
            location=loc_out,
        )

    if not _extension_ok(cap, path):
        return _result(
            decision="deny",
            capability=cap,
            reason="extension_blocked",
            path=path,
            location=loc_out,
        )

    if content is not None:
        if not isinstance(content, (bytes, bytearray)):
            return _result(
                decision="deny",
                capability=cap,
                reason="invalid_argument",
                path=path,
                location=loc_out,
            )
        raw = bytes(content)
        if len(raw) > MAX_BYTES:
            return _result(
                decision="deny",
                capability=cap,
                reason="size_exceeded",
                path=path,
                location=loc_out,
            )
        try:
            raw.decode("utf-8")  # strict
        except UnicodeDecodeError:
            return _result(
                decision="deny",
                capability=cap,
                reason="encoding_invalid",
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


def decide_bytes(
    request: Any,
    *,
    canonical_root: str = DEFAULT_CANONICAL_ROOT,
    content: Optional[bytes] = None,
) -> bytes:
    return serialize_decision_bytes(
        decide(request, canonical_root=canonical_root, content=content)
    )
