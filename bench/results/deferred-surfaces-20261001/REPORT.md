# 보류 표면 관찰 기록

```text
DEFERRED_SURFACES=DOCUMENTED
DEFERRED_AS_CORE_GATE=NO
CORE_CUT=NO
DATE=2026-10-01
```

PLAN·그록 수정: 보류 표면을 Core 확정 **관문으로 올리지 않는다.** 관찰만 한다.

## 항목

| 표면 | 무엇 | 왜 보류 | 지금 열면 안 되는 이유 |
|------|------|---------|------------------------|
| 동적 인덱스 | 맵/벡터 키를 변수로만 잇는 단축 표기 확장 | Core `@` 경로는 정적 세그먼트 중심 | fixture·lower 계약을 흔듦. get 호출로 이미 표현 가능 |
| 반복 `?~` / 다중 분기 단축 | 같은 널 검사를 잇는 표면 압축 | 가독·생성 오류 측정 부족 | U1 바닥·01–04와 별 경쟁. 관문 승격 금지 |
| `fn` / 클로저 | FX `(fn …)` | v0 미포함 | APP-GAP. Core v1 PREP 이전 채택 없음 |
| `loop` / `recur` | 루프 표면 | v0 미포함 | 동일 |
| fixture 05 | 다섯 번째 golden | NO_FIXTURE_05 | 읽기·밀도 주기에서 discard |
| Hot Alias | `U`/`J` 등 | 밀도 경쟁 패배 | Core 밀도 변경 금지 |

## cycle3 이후 추가 관찰 (관문 아님)

| 관찰 | 무엇 | 왜 보류/제한 | 지금 열면 안 되는 이유 |
|------|------|--------------|------------------------|
| 식별자 끝 `?` | `result-ok?` 등 | lower가 `?`를 조건 시작으로 읽기 쉬움 | 이름 규칙·문법 확장 필요. Core 관문 금지 |
| `get-in-2` 식 이름 | 하이픈 뒤 숫자 | `$n-1`과 같이 `-`+digit는 뺄셈 | 이름은 `nested-get` / `get-in-or`로만 Core 표현 |
| `first-or` | 빈 컬렉션 `get(0)` | `eval_fl_min` IndexError | length/빈 검사 폭이 좁은 semantic_min 밖 |
| `last-item` | `length` 의존 | min eval에 length 없음 | 동일 |
| 원본 `get-in-2` | `json_safe_get` | FX std 의존 | Core 동등형은 nested `get` + `?~`만 |

이 표는 **관찰 기록**이다. Core 확정 관문으로 올리지 않는다.

## 판정 줄

```text
DEFERRED_AS_CORE_GATE=NO
OBSERVE_ONLY=YES
CYCLE3_PLUS_NOTES=YES
```
