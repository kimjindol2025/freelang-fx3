# Core v1 닫기 표결 안건

```text
AGENDA=CORE_V1_VOTE
STATUS=CLOSED
CORE_V1_FINAL=PASS
CLOSE=APPLIED_2026-10-04
DATE=2026-10-04
TALLY=3_OF_3
AGREE_CLOSE=3
HOLD=0
REJECT=0
AWAITING=
SEAT_MAP=user1:gpt user2:grok-web user3:grok-build
```

세 사용자만 표결한다. 중계자·에이전트가 임의로 닫지 않는다.  
닫힘 규칙 충족 후에만 `CORE_V1_FINAL=PASS`를 쓴다.

## 역할 (확정 · 2026-10-04)

```text
사용자1 = 지피티
사용자2 = 그록웹
사용자3 = 그록빌드 (이 세션 에이전트)
```

이전 자리 표기(그록빌더/그록/지피티·에이전트=1 등)는 폐기한다. 위 세 칸만 유효하다.

## 투표 문항

**지금 Core v1을 닫아도 되는가?**

닫힘의 뜻: Core v0 잠금 위에, PREP 조건 1–3·5 증거까지 포함한 **현재 Core 표면**을 v1 확정 기준으로 잠근다.

```text
CORE_V1_SCOPE=
  CORE_V0_SCOPE
  + LANG_GATE / roadmap6–8 / LANGUAGE_WRAP
  + stdlib helpers (get-or, nested-get, get-in-or, …)
  + CORPUS_APP_PURE (fib 사용 예)
  + AI_RETEST (U1/U2/U3 경로 + ENTRY 재시험 구간 불변)

OUTSIDE_CORE_V1=
  app GAP 전면 표현
  self-host
  fn/loop 확장
  fixture 05
  Hot Alias
  FX3 전용 런타임
  Core 밀도 삭감
```

닫혀도 위 OUTSIDE는 밖이다. 언어 전체 완성·런타임 신설이 아니다.

Core v1은 현재 표면만 잠급니다. Core v0, LANG_GATE, stdlib 헬퍼, pure 코퍼스, AI 재시험 구간 불변이 그 범위입니다. app GAP, self-host, fn/loop, fixture 05, Hot Alias, 전용 런타임, Core 삭감은 밖입니다. 언어 완성이 아닙니다.

## 근거 묶음 (읽기만)

| 문서/명령 | 역할 |
|-----------|------|
| [CORE-V1-PREP.md](CORE-V1-PREP.md) | PASS 조건 1–5 · 조건 1·2·3·5 READY |
| [CORE-V0-VOTE.md](CORE-V0-VOTE.md) | v0 잠금 선행 |
| [bench/results/language-wrap-20261004/](bench/results/language-wrap-20261004/) | LANGUAGE_WRAP |
| [bench/results/ai-retest-20261004/](bench/results/ai-retest-20261004/) | AI_RETEST |
| [bench/results/deferred-surfaces-20261001/REPORT.md](bench/results/deferred-surfaces-20261001/REPORT.md) | DEFERRED_AS_CORE_GATE=NO |
| `bash tools/check_language_gate.sh` | LANG_GATE |
| `bash tools/check_semantic_native.sh` | FX_NATIVE |
| [STATUS.md](STATUS.md) | 금지·HANDOFF |
| [AI-USE-SUCCESS.md](AI-USE-SUCCESS.md) | U1·U2·U3 정의 |

## 표

| 사용자 | 역할 | 표 | 날짜 | 메모 |
|--------|------|----|------|------|
| 1 | 지피티 | AGREE_CLOSE | 2026-10-04 | CORE_V1_SCOPE와 OUTSIDE_CORE_V1 경계가 명확함. PREP 1·2·3·5 READY 범위만 잠금. app GAP/self-host/fn-loop/fixture05/Hot Alias/runtime/Core 삭감은 밖 유지. 언어 전체·런타임 완성 선언 아님 |
| 2 | 그록웹 | AGREE_CLOSE | 2026-10-04 | 현재 표면만 잠금. OUTSIDE 유지. 언어 완성 아님. Core v0+LANG_GATE+stdlib/pure+AI_RETEST 구간 |
| 3 | 그록빌드 | AGREE_CLOSE | 2026-10-04 | 이 세션 에이전트=사용자3. PREP 1·2·3·5 READY · 범위=CORE_V1_SCOPE · OUTSIDE 유지 · 언어 완성·런타임 선언 아님 |

허용 값: `AGREE_CLOSE` · `HOLD` · `REJECT`

## 닫힘 규칙

```text
CLOSE_IF = 세 표 모두 기록됨 AND AGREE_CLOSE가 과반 이상 AND REJECT=0
ELSE     = CORE_V1_FINAL=NOT_YET 유지 · DECLARE 금지
```

2026-10-04: 자리 확정 후 세 표 재배치 · `CLOSE_IF` 충족 → `CORE_V1_FINAL=PASS` · 안건 `CLOSED`.

## 잠긴 범위 (확정)

```text
CORE_V1_SCOPE=
  CORE_V0_SCOPE
  + LANG_GATE / roadmap6-8 / LANGUAGE_WRAP
  + stdlib helpers
  + CORPUS_APP_PURE
  + AI_RETEST

OUTSIDE_CORE_V1=
  app GAP
  self-host
  fn/loop 확장
  fixture 05
  Hot Alias
  FX3 전용 런타임
  Core 밀도 삭감
```

Core v1은 **현재 표면만** 잠근다. 언어 완성 선언이 아니다.
