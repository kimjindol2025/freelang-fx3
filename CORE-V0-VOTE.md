# Core v0 닫기 표결 안건

```text
AGENDA=CORE_V0_VOTE
STATUS=CLOSED
CORE_V0_FINAL=PASS
CLOSE=APPLIED_2026-10-01
DATE=2026-10-01
TALLY=3_OF_3
AGREE_CLOSE=3
HOLD=0
REJECT=0
AWAITING=
```

세 사용자만 표결한다. 중계자·에이전트가 임의로 닫지 않는다.  
닫힘 규칙 충족 후에만 `CORE_V0_FINAL=PASS`를 쓴다.

## 투표 문항

**지금 Core v0를 닫아도 되는가?**

닫힘의 뜻: fixture 01–04 + delimiter + semantic_min/native(좁은 폭) + stdlib 코퍼스 조각 + AI 사용 바닥을 **현재 Core 표면의 확정 기준**으로 잠근다.  
닫혀도 app GAP·self-host·`fn`/`loop`·fixture 05·Hot Alias는 여전히 밖이다. 언어 완성·`CORE_V1`이 아니다.

## 근거 묶음 (읽기만)

| 문서/명령 | 역할 |
|-----------|------|
| [CORE-V0-PREP.md](CORE-V0-PREP.md) | 잠긴 것·필요 PASS·금지 |
| [corpus/APP-GAP.md](corpus/APP-GAP.md) | app는 `GAP_ONLY` (+ 순수 fib) |
| `python3 tools/lower.py --check` | golden 01–04 |
| `python3 tools/check_delimiter.py` | `$a-$b` · `$n-1` |
| `python3 tools/check_semantic_min.py` | SEMANTIC_MIN |
| `bash tools/check_semantic_native.sh` | FX_NATIVE |
| `python3 tools/check_corpus.py` | CORPUS_STDLIB · CORPUS_APP_PURE |
| [AI-USE-SUCCESS.md](AI-USE-SUCCESS.md) | U1·U2·U3 |

## 표

| 사용자 | 역할 | 표 | 날짜 | 메모 |
|--------|------|----|------|------|
| 1 | 그록빌더 | AGREE_CLOSE | 2026-10-01 | 에이전트=사용자1. 게이트 재실행 PASS. 표결 문장 범위만 잠금. v1 아님 |
| 2 | 그록 | AGREE_CLOSE | 2026-10-01 | 현재 표면만 잠금. 밖 GAP 유지. v1 아님 |
| 3 | 지피티 | AGREE_CLOSE | 2026-10-01 | USER_3. 범위=fixture01-04+delimiter+semantic narrow+stdlib+U1/U2/U3. 밖=app GAP/self-host/fn·loop/fixture05/Hot Alias |

허용 값: `AGREE_CLOSE` · `HOLD` · `REJECT`

## 닫힘 규칙

```text
CLOSE_IF = 세 표 모두 기록됨 AND AGREE_CLOSE가 과반 이상 AND REJECT=0
ELSE     = CORE_V0_FINAL=NOT_YET 유지
```

2026-10-01: `CLOSE_IF` 충족 → `CORE_V0_FINAL=PASS` · 안건 `CLOSED`.

## 잠긴 범위 (확정)

```text
CORE_V0_SCOPE=
  fixture 01-04
  + delimiter
  + semantic_min/native narrow scope
  + stdlib corpus slice
  + U1/U2/U3 AI-use floor

OUTSIDE_CORE_V0=
  app GAP
  self-host
  fn/loop 확장
  fixture 05
  Hot Alias
```

순수 app 헬퍼(`corpus/app/fib`)는 Core 표면 **사용 예**이며, app GAP 전체를 안으로 끌어오지 않는다.
