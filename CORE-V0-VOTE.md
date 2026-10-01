# Core v0 닫기 표결 안건

```text
AGENDA=CORE_V0_VOTE
STATUS=OPEN
CORE_V0_FINAL=NOT_YET
CLOSE=FORBIDDEN_UNTIL_THREE_VOTES
DATE=2026-10-01
TALLY=1_OF_3
AGREE_CLOSE=1
HOLD=0
REJECT=0
AWAITING=USER_1_GROKBUILDER,USER_3_GPT
```

세 사용자만 표결한다. 중계자·에이전트가 임의로 닫지 않는다.  
표가 모이기 전에는 `CORE_V0_FINAL=PASS`를 쓰지 않는다.

## 투표 문항

**지금 Core v0를 닫아도 되는가?**

닫힘의 뜻: fixture 01–04 + delimiter + semantic_min/native(좁은 폭) + stdlib 코퍼스 조각 + AI 사용 바닥을 **현재 Core 표면의 확정 기준**으로 잠근다.  
닫혀도 app GAP·self-host·`fn`/`loop`·fixture 05·Hot Alias는 여전히 밖이다.

## 근거 묶음 (읽기만)

| 문서/명령 | 역할 |
|-----------|------|
| [CORE-V0-PREP.md](CORE-V0-PREP.md) | 잠긴 것·필요 PASS·금지 |
| [corpus/APP-GAP.md](corpus/APP-GAP.md) | app는 `GAP_ONLY` |
| `python3 tools/lower.py --check` | golden 01–04 |
| `python3 tools/check_delimiter.py` | `$a-$b` 등 |
| `python3 tools/check_semantic_min.py` | SEMANTIC_MIN |
| `bash tools/check_semantic_native.sh` | FX_NATIVE |
| `python3 tools/check_corpus.py` | CORPUS_STDLIB · CORPUS_APP=GAP_ONLY |
| [AI-USE-SUCCESS.md](AI-USE-SUCCESS.md) | U1·U2·U3 |

## 표

| 사용자 | 역할 | 표 | 날짜 | 메모 |
|--------|------|----|------|------|
| 1 | 그록빌더 | — | — | |
| 2 | 그록 | AGREE_CLOSE | 2026-10-01 | 현재 표면만 잠금. 밖 GAP 유지. v1 아님 |
| 3 | 지피티 | — | — | |

허용 값: `AGREE_CLOSE` · `HOLD` · `REJECT`

## 닫힘 규칙

```text
CLOSE_IF = 세 표 모두 기록됨 AND AGREE_CLOSE가 과반 이상 AND REJECT=0
ELSE     = CORE_V0_FINAL=NOT_YET 유지
```

`HOLD`만 있으면 안건은 OPEN으로 남긴다.  
순수 app 헬퍼는 이 표결과 **별 후보**다. 표결을 이유로 자동 개시하지 않는다.

## 기록 방법

표를 채울 때 이 파일의 표 칸만 고친다. STATUS의 `CORE_V0_FINAL`은 닫힘 규칙이 만족된 뒤에만 바꾼다.
