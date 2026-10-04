# Core v1 준비 체크리스트

```text
DOC=CORE_V1_PREP
CORE_V1_FINAL=NOT_YET
DECLARE=FORBIDDEN
AGENDA=A1_CHECKLIST_ONLY
DATE=2026-10-01
```

이 문서는 **확정 선언이 아니다.** v1 표결·`CORE_V1_FINAL=PASS`는 여기 조건이 모인 뒤 **별 안건**이다.

## v0에서 이미 PASS (다시 열지 않음)

| 관문 | 상태 | 증거 |
|------|------|------|
| fixture 01–04 golden lower | PASS | `python3 tools/lower.py --check` |
| delimiter / `$a-$b` / `$n-1` | PASS | `python3 tools/check_delimiter.py` |
| SEMI_DISPLAY · WHITESPACE_SAME_FL | PASS | `check_semi_display.py` · whitespace 검사 |
| READ_FIXTURE_01_04 3/3 | PASS | `bench/results/read-fixture-01-04/READ-VOTE.md` |
| semantic_min · native 좁은 폭 | PASS | `check_semantic_min.py` · `check_semantic_native.sh` |
| stdlib 조각 · roadmap6 EXEC | PASS | `check_corpus.py` · `check_roadmap6_exec.py` |
| 밀도 경쟁 · STOP_NO_CUT | PASS | `bench/results/density-20261001/` · `roadmap8-20261001/` |
| Core v0 표결 3/3 | PASS | `CORE-V0-VOTE.md` |
| LANG_GATE (주기2·3) | PASS | `bash tools/check_language_gate.sh` |

## v1을 닫으려면 추가로 필요한 것 (PASS 조건)

각 항목은 **증거 형식**이 갖춰져야 표결 안건을 연다. 이 표만으로 `CORE_V1_FINAL`을 바꾸지 않는다.

| # | 조건 | PASS 증거 형식 | 현재 |
|---|------|----------------|------|
| 1 | **코퍼스 EXEC 폭** | `check_corpus.py` → `CORPUS_STDLIB=PASS` · `CORPUS_APP_PURE=PASS`; roadmap6 재실행 PASS; 케이스 목록이 STATUS/APP-GAP과 동기. GAP(`server_json` 등)은 밖 | READY (A3 헬퍼·2026-10-04 LANG_GATE 재검증) |
| 2 | **AI 사용자 재시험** | U1·U2·U3 결과 디렉터리 경로 + `ENTRY` 바이트 불변 기록. AI-ENTRY.md 바이트 해시 또는 크기 비교 | READY (`bench/results/ai-retest-20261004/` · ENTRY 재시험 구간 불변 · 산출물 15/15 re-lower) |
| 3 | **보류 표면 방침** | `bench/results/deferred-surfaces-*/REPORT.md`에 `DEFERRED_AS_CORE_GATE=NO`; Core.md 밀도 문장 미변경 | READY |
| 4 | **세 사용자 표결** | `CORE-V1-VOTE.md`(신설 안건) · 허용표 `AGREE_CLOSE`/`HOLD`/`REJECT` · 사용자1=그록빌더·2=그록·3=지피티 · 전원 기록 + AGREE_CLOSE 과반 + REJECT=0 | OPEN · 1/3 (사용자1 AGREE_CLOSE · 2·3 대기) |
| 5 | **금지 준수** | fixture 05 · Hot Alias · Core 밀도 삭감 · 전용 런타임 · app GAP 전면 표현 · self-host 없음이 STATUS에 명시 | 유지 |

## 표결 (OPEN · 2026-10-04)

1. 위 1–3·5 READY 확인됨
2. 안건: [CORE-V1-VOTE.md](CORE-V1-VOTE.md) · 범위 문장 고정
3. 세 표 기록 후 닫기 규칙 충족 시에만 `CORE_V1_FINAL=PASS` · 현재 `TALLY=1_OF_3`

## 한 줄

```text
CORE_V1_PREP=READY
CORE_V1_VOTE=OPEN
CORE_V1_FINAL=NOT_YET
DECLARE=FORBIDDEN
PASS_CONDITIONS=DOCUMENTED
TALLY=1_OF_3
```
