# AI 지표 측정 틀

기준일: 2026-09-29

```text
PURPOSE=AI_SUCCESS_METRICS
BASELINE_LANGUAGE=FX_FL
SURFACE=FX3_CORE
WALL_CLOCK_VS_PYTHON=OUT_OF_SCOPE_HERE
```

파이썬과의 벽시계 비교는 이 틀의 기준이 아니다. 여기서 재는 것은 FX3가 설계상 노린 지표다.

| 지표 | 정의 | 출처 |
|------|------|------|
| `OUTPUT_BYTES` | 최종 소스 UTF-8 바이트(개행 포함) | 파일 |
| `OUTPUT_TOKENS` | 완료 이벤트의 `output_tokens` | `ai-events.jsonl` usage. 없으면 `NOT_MEASURED` |
| `REASONING_TOKENS` | `reasoning_output_tokens` | 同上 |
| `FIRST_PASS_VALID` | 첫 소스가 해당 표면 문법·lowering·기대와 맞는지 | lower/cmp/테스트 로그 |
| `CORRECTION_COUNT` | 첫 소스 → 최종 소스까지 수정 라운드 수 | 시험 기록 |
| `EDIT_SPAN` | 첫 소스와 최종 소스의 문자 단위 치환 길이(difflib opcode 합) | 두 파일 |
| `EDIT_LOCALITY` | `EDIT_SPAN / max(len(first),1)` | 파생 |
| `CHAR_REDUCTION_VS_FX` | `(FX_BYTES - FX3_BYTES) / FX_BYTES` | `bench/expected` 쌍 |

토크나이저 패키지는 설치하지 않는다. 모델이 남긴 usage만 `OUTPUT_TOKENS`로 인정한다.

## 명령

```bash
# expected 12쌍의 바이트 절감
python3 bench/metrics/score_metrics.py baseline

# 로드맵 5: 코퍼스 질량 (바이트 + PROXY_UNITS; 모델 토큰 아님)
python3 tools/corpus_token_mass.py

# 한 trial 디렉터리 (first.* / final.* / ai-events.jsonl)
python3 bench/metrics/score_metrics.py trial PATH

# 실험 루트의 fx3·python trial 일괄
python3 bench/metrics/score_metrics.py experiment PATH
```
