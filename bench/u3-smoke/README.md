# U3 작은 실측

```text
AGENDA=U3_SMOKE
LOCK=AI_USE_SUCCESS_V0
PACK=CASE_01_06_REGEN
AI_ENTRY_EXPAND=NO
NAME_ABBREVIATION=NO
PYTHON_WALL_CLOCK=NO
```

[AI-USE-SUCCESS.md](../../AI-USE-SUCCESS.md)의 **U3만** 잰다.

## 규칙

1. 측정 전 `AI-ENTRY.md` 바이트·줄 수를 스냅샷한다. 측정 중 ENTRY 본문을 늘리지 않는다.
2. U1에서 쓴 case 01–06을 **이전 성공 소스를 보지 않고** 같은 ENTRY 조각으로 다시 생성한다.
3. 출력에 Core 금지 한 글자 opcode(`U` `J` `L` `R`를 builtin 축약으로 쓰기)가 있으면 FAIL.
4. 재생성 결과가 lower ∧ 기대 `.fl` 바이트를 유지해야 한다 (U1 유지).
5. 측정 후 ENTRY 스냅샷이 바뀌면 FAIL.

## PASS

- ENTRY 바이트·조각 바이트 불변
- 재생성 유효 ≥ 4/6
- 이름 축약 0건
- “ENTRY 밖 사전이 더 필요했다” = NO (이 묶음 기록)
