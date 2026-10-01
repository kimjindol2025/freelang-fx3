# 코퍼스 질량 · 로드맵 5

```text
CORPUS_TOKEN_MASS=PASS
PAIRED_CASES=8
PAIRED_FX3_BYTES=599
PAIRED_FX_BYTES=921
PAIRED_BYTE_RATIO=0.6504
PAIRED_FX3_PROXY_UNITS=261
PAIRED_FX_PROXY_UNITS=298
PAIRED_PROXY_RATIO=0.8758
OUTPUT_TOKENS=NOT_MEASURED
TOKENIZER_PACKAGE=NOT_INSTALLED
FX_TREE_MODIFIED=NO
```

TSV: `bench/results/corpus-mass-20261001/mass.tsv`

## 방법

- 모델 토크나이저 미사용. `OUTPUT_TOKENS`는 usage 이벤트만 인정 → 이번 측정은 `NOT_MEASURED`.
- `PROXY_UNITS`는 기호 경계 분할. **모델 토큰이 아니다.**
- 쌍: `corpus/stdlib`, `corpus/app`, fixture 01–04.
- FX 샘플: `fx-std.fl`, `fx-queue/server.fl`, `templates/api-server/server.fl` 읽기 전용.

## 읽기

FX3 표현 쌍에서 바이트·프록시 단위가 FX `.fl`보다 작은지 본다.
밀도 경쟁(로드맵 7)·표면 추가 확정은 이 단계가 아니다.
