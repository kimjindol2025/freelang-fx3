#!/usr/bin/env python3
"""로드맵 6: 내린 .fl 과 원본 .fl 실행 결과 일치.

폭: corpus/stdlib + fixture 01–04 만.
app·self-host 표현 없음 (GAP_ONLY). 표면 변경 없음.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "tools/lower.py"
FX_BUILD = Path("/home/kim/kim/platform/freelang-v11-fx/fl-build.sh")

# fixture용 동일 스텁 — 두 소스에 같은 prelude
FIXTURE_STUBS = r"""
(defn str_upper [$s] $s)
(defn http-get-body [$url] "BODY")
(defn json-err [$m] {"err" $m})
(defn json-ok [$b] {"ok" $b})
(defn load-profile [$req] (get $req "profile"))
(defn missing-name [] "MISSING")
(defn welcome [$name] {"hi" $name})
(defn read-payload [$req] (get $req "payload"))
(defn accept [$kind] {"accept" $kind})
(defn reject [$kind] {"reject" $kind})
(defn start-audit [$x] $x)
(defn mark-pass [$x] ["pass" $x])
(defn mark-review [$x] ["review" $x])
(defn finish-audit [$x] $x)
"""


def normalize_fl(text: str) -> str:
    text = re.sub(r";.*?$", "", text, flags=re.M)
    return re.sub(r"\s+", " ", text.strip())


def lower_fx3(path: Path) -> str:
    proc = subprocess.run(
        [sys.executable, str(LOWER), str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8")


def eval_call(fl_src: str, args, call: str = "AUTO"):
    sys.path.insert(0, str(ROOT / "tools"))
    from eval_fl_min import call as ev_call, load_program  # noqa: WPS433

    fns = load_program(fl_src)
    return ev_call(fns, call, args)


def native_call(fl_src: str, call_expr: str) -> str:
    with tempfile.TemporaryDirectory(prefix="fx3-r6n-") as tmp:
        fl = Path(tmp) / "t.fl"
        bin_path = Path(tmp) / "t"
        fl.write_text(fl_src + f"\n(println {call_expr})\n", encoding="utf-8")
        log = Path(tmp) / "log"
        with log.open("w") as fh:
            proc = subprocess.run(
                ["bash", str(FX_BUILD), str(fl), str(bin_path), "--no-net"],
                stdout=fh,
                stderr=subprocess.STDOUT,
                check=False,
            )
        if proc.returncode != 0:
            raise RuntimeError(log.read_text(encoding="utf-8", errors="replace")[-600:])
        out = subprocess.check_output([str(bin_path)], stderr=subprocess.DEVNULL).decode()
        return out.strip().splitlines()[-1]


def pair_exec_match(name: str, fx3: Path, ref: Path, mode: str, args, call="AUTO", native_expr=None) -> None:
    got = lower_fx3(fx3)
    want = ref.read_text(encoding="utf-8")
    if normalize_fl(got) != normalize_fl(want):
        raise RuntimeError(f"{name}: lower≠ref (roadmap6 requires same program text)")
    print(f"PASS {name} lower=ref")

    if mode == "eval":
        a = eval_call(got, args, call=call)
        b = eval_call(want, args, call=call)
        if a != b:
            raise RuntimeError(f"{name}: eval mismatch lowered={a!r} original={b!r}")
        print(f"PASS {name} exec_eval match → {a!r}")
    elif mode == "eval-stub":
        a = eval_call(FIXTURE_STUBS + "\n" + got, args, call=call)
        b = eval_call(FIXTURE_STUBS + "\n" + want, args, call=call)
        if a != b:
            raise RuntimeError(f"{name}: stub-eval mismatch lowered={a!r} original={b!r}")
        print(f"PASS {name} exec_stub match → {a!r}")
    elif mode == "native":
        assert native_expr is not None
        a = native_call(got, native_expr)
        b = native_call(want, native_expr)
        if a != b:
            raise RuntimeError(f"{name}: native mismatch lowered={a!r} original={b!r}")
        print(f"PASS {name} exec_native match → {a!r}")
    else:
        raise RuntimeError(f"bad mode {mode}")


def main() -> int:
    failed = 0
    std = ROOT / "corpus/stdlib"
    exp = ROOT / "bench/expected"

    cases = [
        ("stdlib/identity", std / "identity.fx3", std / "identity.fl", "eval", [7], "identity", None),
        (
            "stdlib/req-body",
            std / "req-body.fx3",
            std / "req-body.fl",
            "eval",
            [{"body": "x"}],
            "req-body",
            None,
        ),
        (
            "stdlib/str-coerce",
            std / "str-coerce.fx3",
            std / "str-coerce.fl",
            "native",
            None,
            None,
            '(str-coerce "z")',
        ),
        (
            "fixture/case-01",
            exp / "case-01.fx3",
            exp / "case-01.fl",
            "eval-stub",
            [{"params": {"currency": "krw"}}],
            "fetch-rate",
            None,
        ),
        (
            "fixture/case-02",
            exp / "case-02.fx3",
            exp / "case-02.fl",
            "eval-stub",
            [{"profile": {"user": {"name": "Ada"}}}],
            "welcome-profile",
            None,
        ),
        (
            "fixture/case-03",
            exp / "case-03.fx3",
            exp / "case-03.fl",
            "eval-stub",
            [{"payload": {"ok": True, "meta": {"kind": "A"}}}],
            "route-payload",
            None,
        ),
        (
            "fixture/case-04",
            exp / "case-04.fx3",
            exp / "case-04.fl",
            "eval-stub",
            [90],
            "audit-score",
            None,
        ),
        (
            "fixture/case-04b",
            exp / "case-04.fx3",
            exp / "case-04.fl",
            "eval-stub",
            [50],
            "audit-score",
            None,
        ),
    ]

    for name, fx3, ref, mode, args, call, native_expr in cases:
        try:
            pair_exec_match(name, fx3, ref, mode, args, call=call or "AUTO", native_expr=native_expr)
        except Exception as err:  # noqa: BLE001
            print(f"FAIL {name}: {err}")
            failed += 1

    print("ROADMAP6_SCOPE=stdlib+fixture_01_04")
    print("ROADMAP6_APP=SKIP_GAP_ONLY")
    print("ROADMAP6_SELFHOST=SKIP")
    print("ROADMAP6_SURFACE_CHANGE=NO")
    if failed:
        print("ROADMAP6_EXEC=FAIL")
        return 1
    print("ROADMAP6_EXEC=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
