# 다른 모델 U1→U3 재현

```text
TASK=OTHER_MODEL_REPLAY_U1_U2_U3
LOCK=AI_USE_SUCCESS_V0
PREVIOUS_MODEL=GROK_BUILD_SESSION
REPLAY_CLI=codex
REPLAY_MODEL=gpt-5.6-luna
```

Grok 세션 스모크와 **다른 모델**로 같은 게이트를 다시 누른다.

## 순서

1. **U1 weak** — `bench/u1-weak-signature` case 01–06  
2. **U2** — `bench/results/u2-smoke-20260929/broken` 01–03 수리  
3. **U3** — AI-ENTRY 불변 + weak 01–06 재생성 (ENTRY 확장 없음)

## PASS (묶음)

- U1: FIRST_VALID ≥ 4/6, ABBREV=0, ENTRY_OUTSIDE=NO, SEMANTIC 기준 동일  
- U2: FINAL_VALID 3/3, EDIT_LOCALITY median ≤ 0.25, 탈출 NO  
- U3: ENTRY bytes unchanged, regen FIRST_VALID ≥ 4/6, ABBREV=0  

당일 스모크다. Core v1이 아니다.
