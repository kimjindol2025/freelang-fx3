# U1 약한 서명 재측정

```text
TASK=U1_WEAK_SIGNATURE_RETEST
LOCK=AI_USE_SUCCESS_V0
CORE=NOT_V1
SMOKE=SAME_DAY
```

강한 서명 U1(01–06) PASS 다음에, **답이 한 줄로 고정되지 않은** 과제로 U1만 다시 누른다. 다른 모델 재현은 이 묶음 다음이다.

## 조건

- 정답 **의미**는 고정 (입출력)
- 구현 **모양**은 2~4개 이상 가능
- 함수/변수명 강제 최소화
- 예제 정답 코드 제공 금지
- [AI-ENTRY.md](../../AI-ENTRY.md) 그대로
- 추가 사전/설명 금지
- ENTRY 파일 바이트 불변

## 측정

`FIRST_VALID` `FINAL_VALID` `ENTRY_OUTSIDE_LOOKUP` `OUTPUT_TOKENS` `EDIT_SPAN` `SHAPE_DIVERSITY`

`FIRST_VALID` = lower PASS ∧ 의미 입출력 PASS ∧ 축약 0  
수리가 없으면 `FINAL_VALID=FIRST_VALID`, `EDIT_SPAN=0`  
`OUTPUT_TOKENS` = 이벤트 usage 없으면 `NOT_MEASURED`

## PASS

```text
FIRST_VALID=6/6
ENTRY_OUTSIDE_LOOKUP=NO
ABBREVIATION_INVENTED=0
SEMANTIC_RESULT=PASS
ENTRY_BYTES_UNCHANGED=YES
```
