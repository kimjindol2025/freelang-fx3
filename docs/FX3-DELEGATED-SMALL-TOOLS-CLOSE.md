# FX3 delegated small-tools tier close

상태: `CLOSED_PASS`

이 문서는 FX3의 작은 업무 도구 위임 레일을 종료한다. 같은 패턴의 POC를
더 추가하지 않고, 다음 기능은 별도 `NEW_ROAD` 안건으로만 연다.

## 닫힌 범위

| 항목 | 근거 | 판정 |
|---|---|---|
| CLI + delegated run | `./bin/fx3`, `docs/FX3-RUN.md` | PASS |
| map schema validation | `poc/manifest-validator`, `poc/config-lint` | PASS |
| 공통 POC rail | `tools/check_poc.py`, `poc/*/poc.json` | PASS |
| array unroll/duplicate/normalization | `poc/task-list-normalize` | PASS |
| eval/native behavior equivalence | 각 POC `verify.sh` | PASS |
| deterministic output | POC gate | PASS |

검증 명령:

```bash
python3 tools/check_poc.py all
bash poc/manifest-validator/scripts/verify.sh
bash poc/config-lint/scripts/verify.sh
bash poc/task-list-normalize/scripts/verify.sh
```

## 남은 구멍과 경계

POC #3가 `count`와 `t0..t2` 슬롯으로 배열을 우회한 것은 업무 도구의 문제가
아니라 Core lowering이 벡터 리터럴을 아직 내리지 못하기 때문이다. 따라서 다음
작업은 새 업무 POC로 해결하지 않는다.

- Core vector literal: `[]`의 정식 surface/lowering 안건
- capability read I/O: 별도 capability 안건
- dedicated VM/IR execution: 현재 열지 않음

고정 경계:

```text
RUNTIME_OWNED=NONE
RUN=DELEGATED
IO_CHANGE=NO
IR_EXEC=NO
SELF_HOST=NO
PUSH=별도 승인
```

## 다음 선택지 (기록)

```text
A) Core vector literal
B) capability read I/O smoke
C) 정지 — 제품은 FreeLangScript/AFJ, FX3는 delegated tools만 유지
```

## 선택 · 2026-10-07

```text
CHOICE=C
DELEGATED_SMALL_TOOLS_NEXT=C_STOP
FX3_SESSION=CLOSED
```

**C(정지)** 를 선택했다. 제품 본체는 FreeLangScript/AFJ/FX를 쓰고, FX3는
이미 닫힌 위임 작은 도구 레일만 유지한다. A/B는 나중에 새 task·새 gate로만
다시 연다. 이 종료 상태를 덮어쓰지 않는다.

세션 실수·미완·성과·다음 에이전트 주의:
[FX3-MISTAKES-AND-HANDOFF-2026-10-06.md](FX3-MISTAKES-AND-HANDOFF-2026-10-06.md).
