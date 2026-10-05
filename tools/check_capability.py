#!/usr/bin/env python3
"""P4 capability gate: deny-first judgment only (no I/O execution)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fx3_capability import (  # noqa: E402
    ALWAYS_DENY,
    SCHEMA,
    decide,
    decide_bytes,
    serialize_decision_bytes,
)

ALLOW = ROOT / "fixtures" / "capability" / "allow"
DENY = ROOT / "fixtures" / "capability" / "deny"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_fixtures(folder: Path, expect_decision: str) -> list:
    fails = []
    for req_path in sorted(folder.glob("*.request.json")):
        name = req_path.name[: -len(".request.json")]
        dec_path = folder / f"{name}.decision.json"
        if not dec_path.exists():
            fails.append(f"FAIL {folder.name}/{name}: missing decision fixture")
            continue
        req = load_json(req_path)
        want = dec_path.read_bytes()
        got = decide_bytes(req)
        if got != want:
            fails.append(f"FAIL {folder.name}/{name}: decision byte mismatch")
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


def check_deny_first() -> list:
    fails = []
    # bare empty request
    d = decide({})
    if d["decision"] != "deny" or d["reason"] != "deny_by_default":
        fails.append(f"FAIL deny-first empty: {d}")
    else:
        print("PASS deny-first empty request")
    for cap in sorted(ALWAYS_DENY):
        d = decide(
            {
                "capability": cap,
                "args": {"path": "x"},
                "root": "fixtures",
                "location": {"line": 1, "column": 1},
            }
        )
        if d["decision"] != "deny":
            fails.append(f"FAIL always-deny allow? {cap}")
            continue
        if d["reason"] != "deny_by_default":
            fails.append(f"FAIL always-deny reason {cap}: {d['reason']}")
            continue
        print(f"PASS always-deny {cap}")
    # write/exec/network aliases already in ALWAYS_DENY
    return fails


def check_determinism() -> list:
    fails = []
    samples = list(ALLOW.glob("*.request.json")) + list(DENY.glob("*.request.json"))
    for req_path in samples:
        req = load_json(req_path)
        a = decide_bytes(req)
        b = decide_bytes(req)
        if a != b:
            fails.append(f"FAIL determinism {req_path.name}")
            continue
    print(f"PASS determinism requests={len(samples)}")
    return fails


def check_order_independence() -> list:
    """Capability list order must not change per-request decisions."""
    fails = []
    caps = [
        {"capability": "source.write", "args": {"path": "a"}, "root": "fixtures"},
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "root": "fixtures",
            "location": {"line": 1, "column": 1},
        },
        {"capability": "network.request", "args": {"path": "a"}, "root": "fixtures"},
        {"capability": "magic.x", "args": {"path": "a"}, "root": "fixtures"},
    ]
    forward = [serialize_decision_bytes(decide(c)) for c in caps]
    backward = [serialize_decision_bytes(decide(c)) for c in reversed(caps)]
    # map by capability name
    def by_cap(seq, src):
        out = {}
        for b, c in zip(seq, src):
            out[c["capability"]] = b
        return out

    f = by_cap(forward, caps)
    b = by_cap(backward, list(reversed(caps)))
    for k in f:
        if f[k] != b[k]:
            fails.append(f"FAIL order-independence {k}")
    if not fails:
        print("PASS order-independence")
    return fails


def check_location_null() -> list:
    fails = []
    d = decide(
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "root": "fixtures",
        }
    )
    if d["decision"] != "allow" or d["location"] is not None:
        fails.append(f"FAIL location-null: {d}")
    else:
        print("PASS location-null allow")
    d2 = decide(
        {
            "capability": "source.read",
            "args": {"path": "valid/x.fx3"},
            "root": "fixtures",
            "location": None,
        }
    )
    if d2["location"] is not None or d2["decision"] != "allow":
        fails.append(f"FAIL location-explicit-null: {d2}")
    else:
        print("PASS location-explicit-null")
    return fails


def check_no_side_effects() -> list:
    """Sanity: module must not expose exec helpers; judgment stays pure."""
    fails = []
    import fx3_capability as m

    banned = {"open", "system", "Popen", "urlopen", "request", "execute_ir", "run"}
    leaked = banned & set(dir(m))
    if leaked:
        fails.append(f"FAIL side-effect symbols {leaked}")
    else:
        print("PASS no-exec-symbols-in-module")
    return fails


def main() -> int:
    fails: list = []
    fails.extend(check_fixtures(ALLOW, "allow"))
    fails.extend(check_fixtures(DENY, "deny"))
    fails.extend(check_deny_first())
    fails.extend(check_determinism())
    fails.extend(check_order_independence())
    fails.extend(check_location_null())
    fails.extend(check_no_side_effects())
    if fails:
        for f in fails:
            print(f)
        print("CAPABILITY_GATE=FAIL")
        return 1
    print("CAPABILITY_GATE=PASS")
    print("DENY_FIRST=PASS")
    print("DETERMINISM=PASS")
    print("LOCATION_PRESERVATION=PASS")
    print(f"CAPABILITY_SCHEMA={SCHEMA}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
