#!/usr/bin/env python3
"""P4 capability gate: deny-first judgment only (no filesystem I/O execution)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fx3_capability import (  # noqa: E402
    ALWAYS_DENY,
    DEFAULT_CANONICAL_ROOT,
    MAX_BYTES,
    SCHEMA,
    decide,
    decide_bytes,
    serialize_decision_bytes,
)

ALLOW = ROOT / "fixtures" / "capability" / "allow"
DENY = ROOT / "fixtures" / "capability" / "deny"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_content(folder: Path, name: str):
    hex_path = folder / f"{name}.content.hex"
    len_path = folder / f"{name}.content_len.txt"
    if hex_path.exists():
        return bytes.fromhex(hex_path.read_text(encoding="utf-8").strip())
    if len_path.exists():
        n = int(len_path.read_text(encoding="utf-8").strip())
        return b"x" * n
    return None


def check_fixtures(folder: Path, expect_decision: str) -> list:
    fails = []
    for req_path in sorted(folder.glob("*.request.json")):
        name = req_path.name[: -len(".request.json")]
        dec_path = folder / f"{name}.decision.json"
        if not dec_path.exists():
            fails.append(f"FAIL {folder.name}/{name}: missing decision fixture")
            continue
        req = load_json(req_path)
        content = load_content(folder, name)
        want = dec_path.read_bytes()
        got = decide_bytes(
            req, canonical_root=DEFAULT_CANONICAL_ROOT, content=content
        )
        if got != want:
            fails.append(
                f"FAIL {folder.name}/{name}: decision byte mismatch "
                f"got={got.decode()} want={want.decode()}"
            )
            continue
        data = json.loads(got.decode("utf-8"))
        if data.get("schema") != SCHEMA:
            fails.append(f"FAIL {folder.name}/{name}: schema")
            continue
        if data.get("decision") != expect_decision:
            fails.append(
                f"FAIL {folder.name}/{name}: decision want {expect_decision} "
                f"got {data.get('decision')}"
            )
            continue
        if expect_decision == "deny" and not data.get("reason"):
            fails.append(f"FAIL {folder.name}/{name}: deny without reason")
            continue
        if ("location" not in req or req.get("location") is None) and data.get(
            "reason"
        ) != "invalid_location":
            if data.get("location") is not None:
                fails.append(f"FAIL {folder.name}/{name}: location should be null")
                continue
        print(
            f"PASS {folder.name}/{name} {data['decision']} {data['reason']} "
            f"loc={data.get('location')}"
        )
    return fails


def check_root_confinement() -> list:
    fails = []
    ok = {
        "capability": "source.read",
        "args": {"path": "valid/x.fx3"},
        "location": {"line": 1, "column": 1},
    }
    d = decide(ok, canonical_root=DEFAULT_CANONICAL_ROOT)
    if d["decision"] != "allow":
        fails.append(f"FAIL relative-under-root: {d}")
    else:
        print("PASS relative-under-root")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "/etc/passwd"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "path_escape":
        fails.append(f"FAIL absolute-path: {d}")
    else:
        print("PASS absolute-path deny")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "../x.fx3"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "path_escape":
        fails.append(f"FAIL dotdot: {d}")
    else:
        print("PASS ../ traversal deny")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "root": "evil",
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "invalid_argument":
        fails.append(f"FAIL request-root: {d}")
    else:
        print("PASS request root argument deny")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "canonical_root": "/hacked",
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "invalid_argument":
        fails.append(f"FAIL request-canonical_root: {d}")
    else:
        print("PASS request top-level canonical_root deny")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "grant": True,
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "invalid_argument":
        fails.append(f"FAIL unknown-toplevel: {d}")
    else:
        print("PASS unknown top-level key deny")

    # keyword-only server injection still allows
    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "allow":
        fails.append(f"FAIL keyword canonical_root allow: {d}")
    else:
        print("PASS keyword-only canonical_root normal allow")

    try:
        decide(
            {
                "capability": "source.read",
                "args": {"path": "valid/x.fx3"},
            },
            DEFAULT_CANONICAL_ROOT,
        )
        fails.append("FAIL positional canonical_root accepted")
    except TypeError:
        print("PASS positional canonical_root rejected")
    return fails


def check_file_boundary() -> list:
    fails = []
    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "a.ir.json"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "extension_blocked":
        fails.append(f"FAIL wrong-ext source.read: {d}")
    else:
        print("PASS wrong extension deny")

    d = decide(
        {
            "capability": "ir.inspect",
            "args": {"path": "a.fx3"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "extension_blocked":
        fails.append(f"FAIL wrong-ext ir.inspect: {d}")
    else:
        print("PASS ir.inspect rejects .fx3")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "a.fx3"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
        content=b"ok",
    )
    if d["decision"] != "allow":
        fails.append(f"FAIL utf8-ok: {d}")
    else:
        print("PASS UTF-8 valid content allow")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "a.fx3"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
        content=b"\xff\xfe",
    )
    if d["decision"] != "deny" or d["reason"] != "encoding_invalid":
        fails.append(f"FAIL utf8-invalid: {d}")
    else:
        print("PASS UTF-8 invalid deny")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "a.fx3"},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
        content=b"x" * (MAX_BYTES + 1),
    )
    if d["decision"] != "deny" or d["reason"] != "size_exceeded":
        fails.append(f"FAIL size: {d}")
    else:
        print(f"PASS size > {MAX_BYTES} deny")

    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "a.fx3", "extra": 1},
            "location": {"line": 1, "column": 1},
        },
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "deny" or d["reason"] != "invalid_argument":
        fails.append(f"FAIL unknown-arg: {d}")
    else:
        print("PASS unknown argument deny")
    return fails


def check_rename_deny() -> list:
    fails = []
    accessed = {"args": False}

    class Probe(dict):
        def get(self, key, default=None):
            if key == "args":
                accessed["args"] = True
            return super().get(key, default)

        def __contains__(self, key):
            if key == "args":
                accessed["args"] = True
            return super().__contains__(key)

    req = Probe(
        {
            "capability": "filesystem.rename",
            "args": {
                "source": "/should/not/touch",
                "destination": "/also/not/touch",
            },
            "location": {"line": 1, "column": 1},
        }
    )
    d = decide(req, canonical_root=DEFAULT_CANONICAL_ROOT)
    if d["decision"] != "deny" or d["reason"] != "deny_by_default":
        fails.append(f"FAIL rename deny: {d}")
    elif d.get("path") is not None:
        fails.append(f"FAIL rename should not surface path: {d}")
    elif accessed["args"]:
        fails.append("FAIL rename inspected args (source/destination)")
    else:
        print("PASS filesystem.rename always deny_by_default")
        print("PASS rename source/destination not accessed")

    if "filesystem.rename" not in ALWAYS_DENY:
        fails.append("FAIL filesystem.rename missing from ALWAYS_DENY")
    else:
        print("PASS filesystem.rename in ALWAYS_DENY")
    return fails


def check_deny_first() -> list:
    fails = []
    d = decide({}, canonical_root=DEFAULT_CANONICAL_ROOT)
    if d["decision"] != "deny" or d["reason"] != "deny_by_default":
        fails.append(f"FAIL deny-first empty: {d}")
    else:
        print("PASS deny-first empty request")
    for cap in sorted(ALWAYS_DENY):
        d = decide(
            {"capability": cap, "location": {"line": 1, "column": 1}},
            canonical_root=DEFAULT_CANONICAL_ROOT,
        )
        if d["decision"] != "deny" or d["reason"] != "deny_by_default":
            fails.append(f"FAIL always-deny {cap}: {d}")
            continue
        print(f"PASS always-deny {cap}")
    return fails


def check_determinism() -> list:
    fails = []
    samples = list(ALLOW.glob("*.request.json")) + list(DENY.glob("*.request.json"))
    for req_path in samples:
        name = req_path.name[: -len(".request.json")]
        folder = req_path.parent
        req = load_json(req_path)
        content = load_content(folder, name)
        a = decide_bytes(req, canonical_root=DEFAULT_CANONICAL_ROOT, content=content)
        b = decide_bytes(req, canonical_root=DEFAULT_CANONICAL_ROOT, content=content)
        if a != b:
            fails.append(f"FAIL determinism {req_path.name}")
    print(f"PASS determinism requests={len(samples)}")
    return fails


def check_order_independence() -> list:
    fails = []
    caps = [
        {"capability": "source.write"},
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "location": {"line": 1, "column": 1},
        },
        {"capability": "network.request"},
        {"capability": "filesystem.rename", "args": {"source": "a", "destination": "b"}},
        {"capability": "magic.x"},
    ]
    forward = [
        serialize_decision_bytes(decide(c, canonical_root=DEFAULT_CANONICAL_ROOT))
        for c in caps
    ]
    backward = [
        serialize_decision_bytes(decide(c, canonical_root=DEFAULT_CANONICAL_ROOT))
        for c in reversed(caps)
    ]

    def by_cap(seq, src):
        out = {}
        for b, c in zip(seq, src):
            out[c["capability"]] = b
        return out

    f = by_cap(forward, caps)
    bmap = by_cap(backward, list(reversed(caps)))
    for k in f:
        if f[k] != bmap[k]:
            fails.append(f"FAIL order-independence {k}")
    if not fails:
        print("PASS order-independence")
    return fails


def check_location_null() -> list:
    fails = []
    d = decide(
        {"capability": "source.read", "args": {"path": "valid/x.fx3"}},
        canonical_root=DEFAULT_CANONICAL_ROOT,
    )
    if d["decision"] != "allow" or d["location"] is not None:
        fails.append(f"FAIL location-null: {d}")
    else:
        print("PASS location-null allow")
    return fails


def check_no_side_effects() -> list:
    fails = []
    import fx3_capability as m

    banned = {"open", "system", "Popen", "urlopen", "execute_ir", "run", "rename"}
    leaked = banned & set(dir(m))
    if leaked:
        fails.append(f"FAIL side-effect symbols {leaked}")
    else:
        print("PASS no-exec-symbols-in-module")
    # ensure module never imports os.rename-style helpers via source scan
    src = (ROOT / "tools" / "fx3_capability.py").read_text(encoding="utf-8")
    for needle in ("os.open", "Path(", "open(", "urlopen", "subprocess", "os.rename"):
        if needle in src:
            fails.append(f"FAIL I/O needle in fx3_capability.py: {needle}")
    if not any(f.startswith("FAIL I/O") for f in fails):
        print("PASS no filesystem I/O calls in capability module")
    return fails


def main() -> int:
    fails: list = []
    fails.extend(check_fixtures(ALLOW, "allow"))
    fails.extend(check_fixtures(DENY, "deny"))
    fails.extend(check_root_confinement())
    fails.extend(check_file_boundary())
    fails.extend(check_rename_deny())
    fails.extend(check_deny_first())
    fails.extend(check_determinism())
    fails.extend(check_order_independence())
    fails.extend(check_location_null())
    fails.extend(check_no_side_effects())
    if fails:
        for f in fails:
            print(f)
        print("CAPABILITY_GATE=FAIL")
        print("CAPABILITY_IMPLEMENTATION=FAIL")
        return 1
    print("CAPABILITY_GATE=PASS")
    print("CAPABILITY_IMPLEMENTATION=PASS")
    print("ROOT_CONFINEMENT=PASS")
    print("FILE_BOUNDARY=PASS")
    print("RENAME_DENY=PASS")
    print("FIXTURE_REGRESSION=PASS")
    print("DETERMINISM=PASS")
    print(f"CAPABILITY_SCHEMA={SCHEMA}")
    print("IO_CHANGE=NO")
    print("RUNTIME_CHANGE=NO")
    print("IR_CHANGE=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
