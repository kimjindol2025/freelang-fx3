#!/usr/bin/env python3
"""로드맵 7: 통과 후보만 밀도 경쟁. 진 표기는 Core에 넣지 않고 버린다.

경쟁 폭 = 로드맵 6과 동일: corpus/stdlib + fixture 01–04.
app·self-host·fixture 05·Hot Alias·극단 압축은 Core 채택 경쟁에서 탈락(기록만).
Core 밀도 문장·표면은 바꾸지 않는다 (깎기는 로드맵 8).
"""

from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "bench" / "results" / f"density-{date.today().strftime('%Y%m%d')}"


def utf8_bytes(text: str) -> int:
    return len(text.encode("utf-8"))


def proxy_units(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9_$\u0080-\uffff]+|[^\s]", text))


def pairs() -> list[tuple[str, Path, Path]]:
    rows: list[tuple[str, Path, Path]] = []
    std = ROOT / "corpus/stdlib"
    for name in ("identity", "req-body", "str-coerce"):
        rows.append((f"stdlib/{name}", std / f"{name}.fx3", std / f"{name}.fl"))
    exp = ROOT / "bench/expected"
    for i in range(1, 5):
        stem = f"case-0{i}"
        rows.append((f"fixture/{stem}", exp / f"{stem}.fx3", exp / f"{stem}.fl"))
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    table: list[dict[str, object]] = []
    wins = 0
    for case, fx3, fl in pairs():
        if not fx3.is_file() or not fl.is_file():
            print(f"FAIL missing {case}")
            return 1
        a = fx3.read_text(encoding="utf-8").strip()
        b = fl.read_text(encoding="utf-8").strip()
        ba, bb = utf8_bytes(a), utf8_bytes(b)
        pa, pb = proxy_units(a), proxy_units(b)
        byte_win = ba < bb
        proxy_win = pa <= pb
        # Core FX3 vs FX: 바이트에서 이기면 밀도 승. 프록시는 보조.
        verdict = "WIN_FX3" if byte_win else "WIN_FX"
        if verdict == "WIN_FX3":
            wins += 1
        table.append(
            {
                "CASE": case,
                "FX3_BYTES": ba,
                "FX_BYTES": bb,
                "BYTE_RATIO": round(ba / bb, 4) if bb else "NA",
                "CHAR_REDUCTION_PERCENT": round((bb - ba) / bb * 100, 4) if bb else "NA",
                "FX3_PROXY": pa,
                "FX_PROXY": pb,
                "PROXY_RATIO": round(pa / pb, 4) if pb else "NA",
                "BYTE_WINNER": "FX3" if byte_win else "FX",
                "PROXY_FX3_LE": "YES" if proxy_win else "NO",
                "VERDICT": verdict,
            }
        )

    tsv = OUT / "density.tsv"
    fields = list(table[0].keys())
    with tsv.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in table:
            w.writerow(row)

    # 진 표기 (Core 미채택)
    discarded = [
        {
            "CANDIDATE": "Hot Alias (U/J/…)",
            "RESULT": "DISCARD_FROM_CORE",
            "NOTE": "후보 기록만. Core 밀도 변경 금지",
        },
        {
            "CANDIDATE": "극단 압축 표기",
            "RESULT": "DISCARD_FROM_CORE",
            "NOTE": "PLAN 경쟁 후보. 이 단계 승자로 채택하지 않음",
        },
        {
            "CANDIDATE": "fixture 05",
            "RESULT": "DISCARD_FROM_CORE",
            "NOTE": "NO_FIXTURE_05",
        },
        {
            "CANDIDATE": "app/self-host 표현",
            "RESULT": "OUT_OF_SCOPE",
            "NOTE": "GAP_ONLY. 로드맵6·7 폭 밖",
        },
    ]
    disc_path = OUT / "discarded.tsv"
    with disc_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["CANDIDATE", "RESULT", "NOTE"], delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in discarded:
            w.writerow(row)

    n = len(table)
    all_win = wins == n
    summary = "\n".join(
        [
            f"ROADMAP7_DENSITY={'PASS' if all_win else 'FAIL'}",
            f"SCOPE=stdlib+fixture_01_04",
            f"PAIRED={n}",
            f"FX3_BYTE_WINS={wins}",
            f"FX_BYTE_WINS={n - wins}",
            "CORE_SURFACE_CHANGED=NO",
            "HOT_ALIAS_ADOPTED=NO",
            "EXTREME_COMPRESS_ADOPTED=NO",
            "LOSING_NOTATION=DISCARDED_FROM_CORE",
            "NEXT=ROADMAP_8_SURFACE_CUT_OR_STOP",
        ]
    )
    (OUT / "SUMMARY.env").write_text(summary + "\n", encoding="utf-8")
    (OUT / "REPORT.md").write_text(
        "\n".join(
            [
                "# 로드맵 7 · 밀도 경쟁",
                "",
                "```text",
                summary,
                "```",
                "",
                f"표: `{tsv.relative_to(ROOT)}`",
                f"진 표기: `{disc_path.relative_to(ROOT)}`",
                "",
                "## 규칙",
                "",
                "- 통과 후보만: 로드맵 6 EXEC PASS 범위 (stdlib + fixture 01–04).",
                "- 지표: UTF-8 바이트(주), PROXY_UNITS(보조). 모델 토큰 아님.",
                "- FX3 Core 표기가 FX `.fl`보다 바이트가 작으면 `WIN_FX3`.",
                "- Hot Alias·극단 압축·fixture 05는 **Core에 넣지 않고 버린다** (기록만).",
                "- 표면을 더 깎지 않는다 (로드맵 8).",
                "",
                "## 결과 요지",
                "",
                f"- {wins}/{n} 쌍에서 FX3가 바이트 승.",
                "- Core 채택 표기 변경 없음. 이긴 것은 **이미 잠긴 Core 표면**이다.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(summary)
    for row in table:
        print(f"{row['VERDICT']} {row['CASE']} ratio={row['BYTE_RATIO']}")
    return 0 if all_win else 1


if __name__ == "__main__":
    raise SystemExit(main())
