# OUTPUT_TOKENS 재측정

```text
AGENDA=A4_OUTPUT_TOKENS
OUTPUT_TOKENS=MEASURED
TOKENIZER_INSTALL=NO
DATE=2026-10-01
```

기존 trial의 `ai-events.jsonl` `usage.output_tokens`만 사용했다. 토크나이저 패키지는 설치하지 않았다.

## 대상

| experiment | 경로 |
|------------|------|
| 01 | `bench/results/fx3-vs-python-timing/experiment-20260929-01` |
| 02 | `bench/results/fx3-vs-python-timing/experiment-20260929-02` |
| 03 | `bench/results/fx3-vs-python-timing/experiment-20260929-03` |

재현:

```bash
python3 bench/metrics/score_metrics.py experiment bench/results/fx3-vs-python-timing/experiment-20260929-01 -o bench/results/output-tokens-20261001/timing-exp01.tsv
```

## 요약

| 표면 | trials | mean | min | max |
|------|--------|------|-----|-----|
| FX3 | 9 | 429.2 | 241 | 509 |
| PYTHON | 6 | 240.0 | 183 | 351 |

상세 TSV: `timing-exp01.tsv` · `timing-exp02.tsv` · `timing-exp03.tsv`  
한 줄: `SUMMARY.env`

## 판정

```text
OUTPUT_TOKENS=MEASURED
SOURCE=ai-events usage
TOKENIZER_INSTALL=NO
```

로드맵 5 코퍼스 질량의 `OUTPUT_TOKENS=NOT_MEASURED`는 **코퍼스 질량 측정 시점**의 기록으로 남긴다. AI trial usage 재측정과는 별 축이다.
