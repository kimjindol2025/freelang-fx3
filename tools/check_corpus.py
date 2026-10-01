#!/usr/bin/env python3
"""좁은 코퍼스: .fx3 → lower 후 참조 .fl과 정규화 비교 + 가능하면 semantic_min/native."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOWER = ROOT / "tools/lower.py"
EVAL = ROOT / "tools/eval_fl_min.py"
NATIVE = ROOT / "tools/check_semantic_native.sh"
CORPUS_STDLIB = ROOT / "corpus/stdlib"
CORPUS_APP = ROOT / "corpus/app"

CASES = [
    {
        "name": "identity",
        "class": "stdlib",
        "dir": CORPUS_STDLIB,
        "source": "freelang-v11-fx/fx-std.fl",
        "eval": {"args": [42], "expect": 42},
        "native_call": "(identity 42)",
        "native_expect": "42",
    },
    {
        "name": "req-body",
        "class": "stdlib",
        "dir": CORPUS_STDLIB,
        "source": "freelang-v11-fx/fx-std.fl",
        "eval": {"args": [{"body": "hi"}], "expect": "hi"},
        "native_call": None,  # map literal 호출은 하네스 밖
        "native_expect": None,
    },
    {
        "name": "str-coerce",
        "class": "stdlib",
        "dir": CORPUS_STDLIB,
        "source": "freelang-v11-fx/fx-std.fl",
        "eval": None,  # eval_fl_min에 str 없음
        "native_call": '(str-coerce "ok")',
        "native_expect": "ok",
    },
    {
        "name": "req-param",
        "class": "stdlib",
        "dir": CORPUS_STDLIB,
        "source": "freelang-v11-fx/fx-std.fl",
        "eval": {"args": [{"params": {"id": "7"}}, "id"], "expect": "7"},
        "native_call": None,
        "native_expect": None,
    },
    {
        "name": "req-query",
        "class": "stdlib",
        "dir": CORPUS_STDLIB,
        "source": "freelang-v11-fx/fx-std.fl",
        "eval": {"args": [{"query": {"q": "x"}}, "q"], "expect": "x"},
        "native_call": None,
        "native_expect": None,
    },
    {
        "name": "fib",
        "class": "app-pure",
        "dir": CORPUS_APP,
        "source": "freelang-v11-fx/fx-queue/server.fl",
        "eval": {"args": [10], "expect": 55},
        "native_call": "(fib 10)",
        "native_expect": "55",
    },
]


def normalize_fl(text: str) -> str:
    text = re.sub(r";.*?$", "", text, flags=re.M)
    text = re.sub(r"\s+", " ", text.strip())
    return text


def lower_file(path: Path) -> str:
    proc = subprocess.run(
        [sys.executable, str(LOWER), str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8")


def eval_min(fl: str, args, expect) -> None:
    import json

    with tempfile.TemporaryDirectory(prefix="fx3-corp-") as tmp:
        p = Path(tmp) / "t.fl"
        p.write_text(fl, encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(EVAL),
                str(p),
                "--args-json",
                json.dumps(args),
                "--expect-json",
                json.dumps(expect),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.decode("utf-8", "replace") or proc.stdout.decode())


def native_one(name: str, fx3: str, call: str, expect: str) -> None:
    with tempfile.TemporaryDirectory(prefix="fx3-corp-n-") as tmp:
        script = Path(tmp) / "run.sh"
        # reuse native build pattern inline to avoid whole suite
        fx_root = Path("/home/kim/kim/platform/freelang-v11-fx")
        fl = Path(tmp) / f"{name}.fl"
        bin_path = Path(tmp) / name
        lowered = subprocess.check_output([sys.executable, str(LOWER)], input=fx3.encode()).decode()
        fl.write_text(lowered + f"\n(println {call})\n", encoding="utf-8")
        log = Path(tmp) / "build.log"
        with log.open("w") as fh:
            proc = subprocess.run(
                ["bash", str(fx_root / "fl-build.sh"), str(fl), str(bin_path), "--no-net"],
                stdout=fh,
                stderr=subprocess.STDOUT,
                check=False,
            )
        if proc.returncode != 0:
            raise RuntimeError(log.read_text(encoding="utf-8", errors="replace")[-800:])
        got = subprocess.check_output([str(bin_path)], stderr=subprocess.DEVNULL).decode().strip().splitlines()[-1]
        if got != expect:
            raise RuntimeError(f"got={got!r} expect={expect!r}")


def main() -> int:
    failed = 0
    for case in CASES:
        name = case["name"]
        base = case["dir"]
        fx3 = base / f"{name}.fx3"
        ref = base / f"{name}.fl"
        print(f"== {name} ({case['class']}) ==")
        if not fx3.is_file() or not ref.is_file():
            print(f"FAIL {name}: missing files")
            failed += 1
            continue
        try:
            got = lower_file(fx3)
        except RuntimeError as err:
            print(f"FAIL {name} lower: {err}")
            failed += 1
            continue
        want = ref.read_text(encoding="utf-8")
        if normalize_fl(got) != normalize_fl(want):
            print(f"FAIL {name} normalize mismatch")
            print("--- got ---")
            print(got)
            print("--- want ---")
            print(want)
            failed += 1
            continue
        print(f"PASS {name} lower~ref")

        if case.get("eval"):
            try:
                eval_min(got, case["eval"]["args"], case["eval"]["expect"])
                print(f"PASS {name} semantic_min")
            except RuntimeError as err:
                print(f"FAIL {name} semantic_min: {err}")
                failed += 1
        else:
            print(f"SKIP {name} semantic_min")

        if case.get("native_call"):
            try:
                native_one(name, fx3.read_text(encoding="utf-8"), case["native_call"], case["native_expect"])
                print(f"PASS {name} native")
            except Exception as err:  # noqa: BLE001
                print(f"FAIL {name} native: {err}")
                failed += 1
        else:
            print(f"SKIP {name} native")

    # density snapshot (chars), not LLM tokens
    print("== density ==")
    for case in CASES:
        name = case["name"]
        base = case["dir"]
        fx3 = (base / f"{name}.fx3").read_text(encoding="utf-8").strip()
        fl = (base / f"{name}.fl").read_text(encoding="utf-8").strip()
        ratio = (len(fx3) / len(fl)) if fl else 0
        print(f"DENSITY {name} fx3={len(fx3)} fl={len(fl)} ratio={ratio:.3f}")

    if failed:
        print("CORPUS_STDLIB=FAIL")
        return 1
    print("CORPUS_STDLIB=PASS")
    print("CORPUS_APP=GAP_ONLY")
    print("CORPUS_APP_PURE=PASS")
    print("CORPUS_SELFHOST=NOT_STARTED")
    print("CORPUS_GAP=server_json,mariadb,fn/closure,loop")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
