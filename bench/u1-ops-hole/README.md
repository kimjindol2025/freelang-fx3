# U1 연산 구멍 보강

```text
TASK=U1_OPS_HOLE_RETEST
LOCK=AI_USE_SUCCESS_V0
MODEL=gpt-5.6-luna
AI_ENTRY_EXPAND=NO
FOCUS=ARITHMETIC_AND_NULL_WITHOUT_INVENTED_CALLS
```

다른 모델 재현에서 case-06이 `multiply(...)`를 발명했다. ENTRY에 연산을 추가하지 않고, **같은 실패 유형**만 과제 폭을 넓혀 U1을 다시 누른다.

## PASS

```text
FIRST_VALID>=5/6
ABBREVIATION_INVENTED=0
INVENTED_ARITH_CALL=0
ENTRY_BYTES_UNCHANGED=YES
SEMANTIC_RESULT 기준 동일
```

`INVENTED_ARITH_CALL`: lower는 되지만 `+ - * /` 자리에 알 수 없는 호출 이름을 쓴 경우.
