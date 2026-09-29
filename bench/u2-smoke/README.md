# U2 작은 실측

```text
AGENDA=U2_SMOKE
LOCK=AI_USE_SUCCESS_V0
PACK=CASE_01_03
REPAIR_ROUNDS_MAX=2
PYTHON_WALL_CLOCK=NO
ESCAPE_TO_OTHER_DIALECT=NO
```

[AI-USE-SUCCESS.md](../../AI-USE-SUCCESS.md)의 **U2만** 잰다.

## 규칙

1. `broken/case-0N.fx3`는 일부러 깨진 첫 출력이다 (중괄호 또는 `;` 누락 등).
2. 수리 전 [AI-ENTRY.md](../../AI-ENTRY.md)를 둔다. 방언을 바꾸지 않는다.
3. 수리본은 `repaired/case-0N.fx3`. 최대 2라운드.
4. 최종본을 lower한 뒤 기대 `.fl`과 바이트 비교한다.
5. `EDIT_SPAN` / `EDIT_LOCALITY`는 broken → repaired 문자 치환 길이로 잰다 (`bench/metrics/score_metrics.py`와 동일 정의).

## PASS

3과제 모두 최종 유효(lower ∧ `.fl` 바이트)이고, 통과 trial의 `EDIT_LOCALITY` 중앙값 **≤ 0.25**.
