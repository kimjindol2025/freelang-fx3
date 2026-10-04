# FX3 언어 마무리 · Core v0 범위

```text
DATE=2026-10-04
AGENDA=FX3_LANGUAGE_WRAP_CORE_V0
LANGUAGE_WRAP=CLOSED
CORE_V1_FINAL=NOT_YET
DECLARE=FORBIDDEN
```

## 범위

잠긴 **Core v0** 표면의 언어 설계·검증 마무리다.

- 포함: fixture 01–04, delimiter, SEMI_DISPLAY, semantic_min/native, stdlib corpus, roadmap 1–8, LANG_CYCLE2·3, A1–A4
- 제외: Core v1 선언, fixture 05, Hot Alias, app GAP 전면 표현, self-host, FX3 전용 런타임

## 재검증 (2026-10-04)

| 관문 | 결과 |
|------|------|
| `bash tools/check_language_gate.sh` | `LANG_GATE=PASS` |
| `bash tools/check_semantic_native.sh` | `FX_NATIVE=PASS` |
| Core 삭감 | 없음 |
| fixture 05 / Hot Alias | 열지 않음 |

로그: `lang-gate.log`

## CORE_V1_PREP 동기화

| # | 조건 | 이 마무리 시점 |
|---|------|----------------|
| 1 코퍼스 EXEC 폭 | READY (`CORPUS_STDLIB`·`APP_PURE`·roadmap6 PASS, 헬퍼 반영) |
| 2 AI 사용자 재시험 | 미착수 (별 안건) |
| 3 보류 표면 방침 | READY (`DEFERRED_AS_CORE_GATE=NO`) |
| 4 세 사용자 표결 | 열지 않음 |
| 5 금지 준수 | 유지 |

→ `CORE_V1_PREP=READY` 유지 · `CORE_V1_FINAL=NOT_YET` · 표결 안건 미개설

## stale handoff

A1–A4 닫힌 뒤 hot/STATUS가 `fl-git GitLab`으로 넘어가 있었다. 언어 본체 마무리와 무관한 교차 프로젝트 안내이므로 이 패키지에서 정리한다. fl-git 작업은 별 저장소·별 안건이다.

## 한 줄

```text
LANGUAGE_WRAP=CLOSED
CORE_V0_SCOPE_COMPLETE=YES
CORE_V1_FINAL=NOT_YET
NEXT=NEW_AGENDA_ONLY
```
