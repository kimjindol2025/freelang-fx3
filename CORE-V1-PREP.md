# Core v1 준비 체크리스트

```text
DOC=CORE_V1_PREP
CORE_V1_FINAL=NOT_YET
DECLARE=FORBIDDEN
DATE=2026-10-01
```

이 문서는 **확정 선언이 아니다.** v1 표결·`CORE_V1_FINAL=PASS`는 여기 조건이 모인 뒤 별 안건이다.

## v0에서 이미 PASS (다시 열지 않음)

| 관문 | 상태 |
|------|------|
| fixture 01–04 golden lower | PASS |
| delimiter / `$a-$b` / `$n-1` | PASS |
| SEMI_DISPLAY · WHITESPACE_SAME_FL | PASS |
| READ_FIXTURE_01_04 3/3 | PASS |
| semantic_min · native 좁은 폭 | PASS |
| stdlib 조각 · roadmap6 EXEC | PASS |
| 밀도 경쟁 · STOP_NO_CUT | PASS |
| Core v0 표결 3/3 | PASS |
| LANG_GATE (주기2) | PASS |

## v1을 닫으려면 추가로 필요한 것 (초안)

1. **코퍼스 EXEC 폭** — stdlib/app-pure를 roadmap6 수준으로 더 넓히되 GAP(`server_json` 등)은 밖
2. **AI 사용자 재시험** — U1·U2·U3 바닥 회귀 한 바퀴 (ENTRY 바이트 불변)
3. **보류 표면 방침** — 관찰 문서화 유지. **Core 관문으로 올리지 않음**
4. **세 사용자 표결** — v0와 같은 형식의 v1 닫기 표. 범위 문장 명시
5. **금지 준수** — fixture 05 · Hot Alias · Core 밀도 삭감 · 전용 런타임 없음

## 한 줄

```text
CORE_V1_PREP=READY
CORE_V1_FINAL=NOT_YET
```
