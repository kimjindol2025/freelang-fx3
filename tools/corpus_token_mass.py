#!/usr/bin/env python3
"""로드맵 5: FX/FX3 코퍼스 질량.

모델 토크나이저 패키지는 설치하지 않는다 ([bench/metrics/README.md](../bench/metrics/README.md)).
- UTF8_BYTES: 파일 바이트
- PROXY_UNITS: 비문자 경계 분할 단위 (모델 토큰 아님)
- OUTPUT_TOKENS: ai-events usage만. 없으면 NOT_MEASURED

FX 트리는 읽기만 한다. 수정하지 않는다.
"""

from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FX_ROOT = Path("/home/kim/kim/platform/freelang-v11-fx")
OUT_DIR = ROOT / "bench" / "results" / f"corpus-mass-{date.today().strftime('%Y%m%d')}"


def utf8_bytes(text: str) -> int:
    return len(text.encode("utf-8"))


def proxy_units(text: str) -> int:
    # 글자·숫자·$·_ 연속을 한 단위, 그 외 기호 각각 단위
    parts = re.findall(r"[A-Za-z0-9_$\u0080-\uffff]+|[^\s]", text)
    return len(parts)


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def pair_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for base in (ROOT / "corpus/stdlib", ROOT / "corpus/app"):
        if not base.is_dir():
            continue
        for fx3 in sorted(base.glob("*.fx3")):
            fl = fx3.with_suffix(".fl")
            if not fl.is_file():
                continue
            a = load(fx3).strip()
            b = load(fl).strip()
            ba, bb = utf8_bytes(a), utf8_bytes(b)
            pa, pb = proxy_units(a), proxy_units(b)
            rows.append(
                {
                    "SLICE": base.name,
                    "CASE": fx3.stem,
                    "FX3_BYTES": ba,
                    "FX_BYTES": bb,
                    "BYTE_RATIO_FX3_OVER_FX": round(ba / bb, 4) if bb else "NA",
                    "CHAR_REDUCTION_PERCENT": round((bb - ba) / bb * 100, 4) if bb else "NA",
                    "FX3_PROXY_UNITS": pa,
                    "FX_PROXY_UNITS": pb,
                    "PROXY_RATIO_FX3_OVER_FX": round(pa / pb, 4) if pb else "NA",
                    "OUTPUT_TOKENS": "NOT_MEASURED",
                    "NOTE": "PROXY_UNITS_NOT_MODEL_TOKENS",
                }
            )
    # expected fixtures 01-04 (Core locked)
    expected = ROOT / "bench/expected"
    for fx3 in sorted(expected.glob("case-0[1-4].fx3")):
        fl = fx3.with_suffix(".fl")
        if not fl.is_file():
            continue
        a, b = load(fx3).strip(), load(fl).strip()
        ba, bb = utf8_bytes(a), utf8_bytes(b)
        pa, pb = proxy_units(a), proxy_units(b)
        rows.append(
            {
                "SLICE": "fixture-core",
                "CASE": fx3.stem,
                "FX3_BYTES": ba,
                "FX_BYTES": bb,
                "BYTE_RATIO_FX3_OVER_FX": round(ba / bb, 4) if bb else "NA",
                "CHAR_REDUCTION_PERCENT": round((bb - ba) / bb * 100, 4) if bb else "NA",
                "FX3_PROXY_UNITS": pa,
                "FX_PROXY_UNITS": pb,
                "PROXY_RATIO_FX3_OVER_FX": round(pa / pb, 4) if pb else "NA",
                "OUTPUT_TOKENS": "NOT_MEASURED",
                "NOTE": "PROXY_UNITS_NOT_MODEL_TOKENS",
            }
        )
    return rows


def fx_tree_sample_rows() -> list[dict[str, object]]:
    """FX 쪽 읽기 전용 샘플 질량 (표현 쌍 없음 → FX3 열은 NA)."""
    samples = [
        FX_ROOT / "fx-std.fl",
        FX_ROOT / "fx-queue/server.fl",
        FX_ROOT / "templates/api-server/server.fl",
    ]
    rows = []
    for path in samples:
        if not path.is_file():
            continue
        text = load(path)
        rel = str(path.relative_to(FX_ROOT))
        rows.append(
            {
                "SLICE": "fx-readonly",
                "CASE": rel,
                "FX3_BYTES": "NA",
                "FX_BYTES": utf8_bytes(text),
                "BYTE_RATIO_FX3_OVER_FX": "NA",
                "CHAR_REDUCTION_PERCENT": "NA",
                "FX3_PROXY_UNITS": "NA",
                "FX_PROXY_UNITS": proxy_units(text),
                "PROXY_RATIO_FX3_OVER_FX": "NA",
                "OUTPUT_TOKENS": "NOT_MEASURED",
                "NOTE": "FX_TREE_READ_ONLY_NO_FX3_PAIR",
            }
        )
    return rows


def write_tsv(rows: list[dict[str, object]], path: Path) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def summary(rows: list[dict[str, object]]) -> str:
    paired = [r for r in rows if isinstance(r["FX3_BYTES"], int)]
    if not paired:
        return "NO_PAIRED_ROWS"
    fx3_b = sum(int(r["FX3_BYTES"]) for r in paired)
    fx_b = sum(int(r["FX_BYTES"]) for r in paired)
    fx3_p = sum(int(r["FX3_PROXY_UNITS"]) for r in paired)
    fx_p = sum(int(r["FX_PROXY_UNITS"]) for r in paired)
    lines = [
        "CORPUS_TOKEN_MASS=PASS",
        f"PAIRED_CASES={len(paired)}",
        f"PAIRED_FX3_BYTES={fx3_b}",
        f"PAIRED_FX_BYTES={fx_b}",
        f"PAIRED_BYTE_RATIO={round(fx3_b / fx_b, 4) if fx_b else 'NA'}",
        f"PAIRED_FX3_PROXY_UNITS={fx3_p}",
        f"PAIRED_FX_PROXY_UNITS={fx_p}",
        f"PAIRED_PROXY_RATIO={round(fx3_p / fx_p, 4) if fx_p else 'NA'}",
        "OUTPUT_TOKENS=NOT_MEASURED",
        "TOKENIZER_PACKAGE=NOT_INSTALLED",
        "FX_TREE_MODIFIED=NO",
    ]
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = pair_rows() + fx_tree_sample_rows()
    tsv = OUT_DIR / "mass.tsv"
    write_tsv(rows, tsv)
    text = summary(rows)
    (OUT_DIR / "SUMMARY.env").write_text(text + "\n", encoding="utf-8")
    report = OUT_DIR / "REPORT.md"
    report.write_text(
        "\n".join(
            [
                "# 코퍼스 질량 · 로드맵 5",
                "",
                "```text",
                text,
                "```",
                "",
                f"TSV: `{tsv.relative_to(ROOT)}`",
                "",
                "## 방법",
                "",
                "- 모델 토크나이저 미사용. `OUTPUT_TOKENS`는 usage 이벤트만 인정 → 이번 측정은 `NOT_MEASURED`.",
                "- `PROXY_UNITS`는 기호 경계 분할. **모델 토큰이 아니다.**",
                "- 쌍: `corpus/stdlib`, `corpus/app`, fixture 01–04.",
                "- FX 샘플: `fx-std.fl`, `fx-queue/server.fl`, `templates/api-server/server.fl` 읽기 전용.",
                "",
                "## 읽기",
                "",
                "FX3 표현 쌍에서 바이트·프록시 단위가 FX `.fl`보다 작은지 본다.",
                "밀도 경쟁(로드맵 7)·표면 추가 확정은 이 단계가 아니다.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(text)
    print(f"WROTE {tsv}")
    print(f"WROTE {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
