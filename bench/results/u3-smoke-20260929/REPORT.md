# U3 스모크 결과 — 2026-09-29

```text
AGENDA=U3_SMOKE
LOCK=AI_USE_SUCCESS_V0
MODEL=GROK_BUILD_SESSION
AI_ENTRY_EXPAND=NO
PACK=CASE_01_06_REGEN
PYTHON_WALL_CLOCK=NO
ENTRY_SAME=YES
REGEN_VALID=6/6
NAME_ABBREV_TOTAL=0
DICT_BEYOND_ENTRY=NO
PACK_VERDICT=PASS
```

## 방법

1. `AI-ENTRY.md` 바이트·줄·프롬프트 조각 바이트를 `entry-baseline.env`에 둔다.
2. ENTRY 본문을 수정하지 않는다.
3. case 01–06을 이전 `u1-smoke` 성공 소스를 보지 않고 같은 ENTRY 계약으로 다시 쓴다.
4. lower ∧ 기대 `.fl` 바이트, 한 글자 opcode 호출(`U(` `J(` `L(` `R(`), ENTRY 불변을 검사한다.

## ENTRY 스냅샷

| 항목 | baseline | after |
|------|----------:|------:|
| AI-ENTRY 바이트 | 3204 | 3204 |
| AI-ENTRY 줄 | 84 | 84 |
| 프롬프트 조각 바이트 | 502 | 502 |

`ENTRY_SAME=YES`

## 결과

| CASE | LOWER | FL_BYTES | 축약 | REGEN 유효 |
|------|-------|----------|------|------------|
| 01–06 | PASS | PASS | NONE | PASS 6/6 |

- 재생성 유효 **6/6** (≥ 4/6)
- 이름 축약 **0**
- ENTRY 밖 사전 필요 **NO** (이 묶음)
- 묶음 **PASS**

참고: 재생성 바이트가 u1-smoke 첫 시도와 **6/6 동일**했다. 과제 서명이 강하고 같은 세션 모델이라서다. U3 PASS 조건은 동일성이 아니라 ENTRY 불변·축약 없음·유효 유지이다.

## 한계

- 며칠에 걸친 질림·ENTRY 비대화는 이 하루 묶음으로 증명되지 않는다.
- 다른 모델이 ENTRY를 늘리거나 `U`로 줄이는지는 미측정.
- 주관적 “질린다”는 USER-STUDY에 쌓을 수 있으나, 이번 채택 문장은 객관 검사 네 줄뿐이다.

## 다음

U1·U2·U3 스모크는 이 세션 모델 기준으로 닫혔다. 다음 후보는 **다른 모델/CLI로 U1–U3 재현**이거나, 서명이 약한 과제(의도적으로 여러 정답 모양)로 U1을 다시 눌러 보는 일이다.
