# U2 스모크 결과 — 2026-09-29

```text
AGENDA=U2_SMOKE
LOCK=AI_USE_SUCCESS_V0
MODEL=GROK_BUILD_SESSION
AI_ENTRY=YES
PACK=CASE_01_03
REPAIR_ROUNDS_MAX=2
USED_ROUNDS=1
ESCAPE_TO_OTHER_DIALECT=NO
PYTHON_WALL_CLOCK=NO
FINAL_VALID=3/3
EDIT_LOCALITY_MEDIAN=0.016393
PACK_VERDICT=PASS
```

## 방법

1. `broken/`에 일부러 깨진 첫 출력을 둔다.
2. [AI-ENTRY.md](../../../AI-ENTRY.md)를 두고 같은 FX3 Core로만 고친다.
3. `repaired/` 한 라운드로 최종본을 만든다.
4. lower 후 기대 `.fl` 바이트 비교.
5. `EDIT_SPAN` / `EDIT_LOCALITY` = broken → repaired (difflib opcode 합 / 첫 길이).

## 깨진 방식

| CASE | 깨진 점 | lower 오류 |
|------|---------|------------|
| 01 | 함수 본문 `{` `}` 없음 | `기대 '{'` |
| 02 | 바인딩·식 사이 `;` 없음 | `본문 식이 없음` |
| 03 | 일반식 뒤 바인딩 | `첫 일반식 뒤의 바인딩은 오류` |

## 결과

| CASE | 최종 유효 | EDIT_SPAN | EDIT_LOCALITY | 탈출 |
|------|-----------|----------:|-------------:|------|
| 01 | PASS | 2 | 0.014184 | NO |
| 02 | PASS | 2 | 0.016393 | NO |
| 03 | PASS | 19 | 0.135714 | NO |

- 최종 유효 **3/3**
- `EDIT_LOCALITY` 중앙값 **0.016393** ≤ 0.25
- 묶음 **PASS**

## 한계

- 수리자도 이 세션 Grok이다. 다른 모델 CLI 재현은 아직이다.
- 깨진 입력을 사람이 설계했다. 실제 모델이 낸 실패 분포와 다를 수 있다.
- U3(질림)는 측정하지 않았다.

## 다음

U2 묶음은 닫는다. 다음 후보는 **U3 작은 실측**(AI-ENTRY 크기 유지·이름 축약 없음·재독 비용) 또는 다른 모델로 U1/U2 재현이다.
