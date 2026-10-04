# Core v1 닫기 표결 안건

```text
AGENDA=CORE_V1_VOTE
STATUS=OPEN
CORE_V1_FINAL=NOT_YET
DECLARE=FORBIDDEN_UNTIL_CLOSE
DATE=2026-10-04
TALLY=2_OF_3
AGREE_CLOSE=2
HOLD=0
REJECT=0
AWAITING=user1
IDENTITY_FIX=2026-10-04
```

세 사용자만 표결한다. 중계자·에이전트가 임의로 닫지 않는다.  
닫힘 규칙 충족 후에만 `CORE_V1_FINAL=PASS`를 쓴다.

## 역할 (정정 · 2026-10-04)

```text
사용자1 = 그록빌더
사용자2 = 그록
사용자3 = 이 에이전트 (Grok Build 세션)   ← 이전 기록 오류 정정
```

이전에는 에이전트 표를 사용자1에, 지피티 문구를 사용자3에 넣었고 `3/3`으로 닫았다.  
**사용자3=이 에이전트**로 바로잡으며 그 닫힘을 취소한다. `CORE_V1_FINAL=NOT_YET`로 되돌린다.

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
| 1 | 그록빌더 | | | 대기. 에이전트 표를 여기에 넣었던 기록을 비움 |
| 2 | 그록 | AGREE_CLOSE | 2026-10-04 | 현재 표면만 잠금. OUTSIDE 유지. 언어 완성 아님. Core v0+LANG_GATE+stdlib/pure+AI_RETEST 구간 |
| 3 | 이 에이전트 | AGREE_CLOSE | 2026-10-04 | 사용자3=이 에이전트(정정). PREP 1·2·3·5 READY · 범위=CORE_V1_SCOPE · OUTSIDE 유지 · 언어 완성·런타임 선언 아님 · 단독 닫기 금지 |

허용 값: `AGREE_CLOSE` · `HOLD` · `REJECT`

### 참고 (자리 오류로 옮긴 문구)

지피티 명의로 들어왔던 `AGREE_CLOSE` 근거 문장은 사용자3 자리가 에이전트임이 확정되어 **이 표의 유효 칸에서는 제거**했다. 사용자1(그록빌더) 표가 따로 오면 그때 기록한다.

## 닫힘 규칙

```text
CLOSE_IF = 세 표 모두 기록됨 AND AGREE_CLOSE가 과반 이상 AND REJECT=0
ELSE     = CORE_V1_FINAL=NOT_YET 유지 · DECLARE 금지
```

현재 `TALLY=2_OF_3` (사용자1 미기록) → `CORE_V1_FINAL=NOT_YET`.

## 표 넣는 법

사용자1(그록빌더)은 이 파일 표 칸만 채운다. `STATUS.md`의 `CORE_V1_FINAL`은 닫힘 규칙 충족 후에만 바꾼다.
