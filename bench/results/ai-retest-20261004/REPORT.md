# CORE_V1_PREP · AI 사용자 재시험 · 2026-10-04

```text
AGENDA=CORE_V1_PREP_AI_RETEST
LANGUAGE_WRAP=CLOSED
CORE_CUT=NO
FIXTURE_05=NO
HOT_ALIAS=NO
RUNTIME=NO
ENTRY_SAME_DURING_RETEST=YES
ARTIFACT_RECHECK=PASS
PACK_VERDICT=PASS
```

## 목적

[CORE-V1-PREP.md](../../../CORE-V1-PREP.md) 조건 2 증거:

1. U1·U2·U3 결과 디렉터리 경로
2. `AI-ENTRY.md` 바이트·해시 불변 기록 (이 재시험 구간)

Core 표면·ENTRY 본문을 이 안건에서 바꾸지 않는다.

## 경로

| ID | 경로 | 당시 판정 |
|----|------|-----------|
| U1 | `bench/results/u1-smoke-20260929` | PASS 6/6 |
| U2 | `bench/results/u2-smoke-20260929` | PASS 3/3 · EDIT_LOCALITY median 0.016393 |
| U3 | `bench/results/u3-smoke-20260929` | PASS 6/6 · ENTRY_SAME=YES |
| U1 ops | `bench/results/u1-ops-20260930` | PASS 5/6 (별 모델 보강) |

## ENTRY 스냅샷 (재시험 구간)

| 항목 | before | after |
|------|-------:|------:|
| bytes | 3373 | 3373 |
| lines | 85 | 85 |
| sha256 | `94f0d80a697eb58a0e0ec82f26c347691f4afa644de09bedd65712c17c89114e` | `94f0d80a697eb58a0e0ec82f26c347691f4afa644de09bedd65712c17c89114e` |
| fragment bytes | 503 | 503 |

`ENTRY_SAME_DURING_RETEST=YES`

### U3 당시 baseline과의 비교 (역사)

U3(`2026-09-29`) baseline은 bytes **3204** / lines **84** / fragment **502**였다.  
현재 ENTRY는 bytes **3373** / lines **85** / fragment **503** 이다 (`DELTA=169`).

이는 재시험 중 팽창이 아니라, delimiter·규칙 10(`$n-1`) 정리 이후 문서가 늘어난 **누적 상태**다. 이번 안건에서 ENTRY를 추가로 늘리거나 Hot Alias를 넣지 않았다.

## 산출물 재검증

기존 U1 `first/` · U2 `repaired/` · U3 `regen/` `.fx3`를 다시 lower해 `bench/expected/case-0N.fl`과 비교했다.

- 총 15건 · 실패 0건 → **PASS**
- 상세: `recheck.tsv`

## 한계

- 새 모델에 과제 재생성 호출을 다시 돌리지는 않았다. 증거는 **경로 고정 + ENTRY 불변 + 산출물 lower 재검증**이다.
- 다른 모델 CLI 재현·약한 서명 과제는 별 안건이다.
- `CORE_V1_FINAL` 표결은 열지 않는다.

## 한 줄

```text
AI_RETEST=PASS
CORE_V1_PREP_CONDITION_2=READY
CORE_V1_FINAL=NOT_YET
DECLARE=FORBIDDEN
```
