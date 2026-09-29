# U1 연산 구멍 보강 — 2026-09-30

```text
TASK=U1_OPS_HOLE_RETEST
LOCK=AI_USE_SUCCESS_V0
MODEL=gpt-5.6-luna
AI_ENTRY_EXPAND=NO
ENTRY_BYTES=3204
FIRST_VALID=5/6
INVENTED_ARITH_CALL_COUNT=0
ABBREVIATION_INVENTED=0
PACK_VERDICT=PASS
```

## 목적

다른 모델 재현에서 case-06이 `multiply(...)`를 발명했다. ENTRY에 연산을 넣지 않고, 산술·널 과제를 넓혀 같은 구멍을 다시 눌렀다.

## 결과

| CASE | FIRST_VALID | 비고 |
|------|-------------|------|
| 01 sum | PASS | `+` |
| 02 product | PASS | `*` |
| 03 subtract | **FAIL** | `{$first-$second;}` — 본문 끝 여분 `;`로 lower `기대 '}'` |
| 04 null→square | PASS | `~` + `*` (채점기 `null?` 오인 수정 후) |
| 05 (a*b)+c | PASS | |
| 06 >0 → *2 | PASS | |

- **INVENTED_ARITH_CALL=0** — 이번 묶음에서 `multiply`류 발명은 없었다.
- ENTRY 불변, 축약 0.
- 묶음 **PASS** (임계 ≥5/6).

## 남은 구멍

실패는 연산 발명이 아니라 **`;` 과다**다. 강한 서명·U2에서 보던 delimiter 계열과 같다. 연산 구멍은 이번 표본에서 닫혔고, trailing `;`는 별 줄로 남긴다.

## 채점 수정

첫 채점에서 `(null? …)`를 `null` 발명으로 오인했다. `null?` 전체 토큰 매칭으로 고친 뒤 동일 출력을 재채점했다. AI 재호출 없음.

## 다음 후보

- trailing `;` / delimiter만 모은 작은 U1·U2
- FX 실행 단계 (여전히 별 안건)
