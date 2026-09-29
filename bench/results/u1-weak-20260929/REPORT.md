# U1 약한 서명 재측정 — 2026-09-29

```text
TASK=U1_WEAK_SIGNATURE_RETEST
LOCK=AI_USE_SUCCESS_V0
CORE=NOT_V1
SMOKE=SAME_DAY
MODEL=GROK_BUILD_SESSION
AI_ENTRY=YES_UNCHANGED_3204B
FIRST_VALID=6/6
FINAL_VALID=6/6
ENTRY_OUTSIDE_LOOKUP=NO
ABBREVIATION_INVENTED=0
SEMANTIC_RESULT=PASS
ENTRY_BYTES_UNCHANGED=YES
SHAPE_DIVERSITY=6
OUTPUT_TOKENS=NOT_MEASURED
EDIT_SPAN=0
PACK_VERDICT=PASS
```

## 목적

강한 서명 U1은 재생성이 글자까지 같았다. 이 묶음은 **의미만 고정**하고 구현 모양·이름을 열어, 계약만으로 첫 시도가 버티는지 본다.

## 조건 준수

- 예제 정답 코드 없음
- AI-ENTRY 추가 설명 없음 / 파일 바이트 3204 유지
- 함수·변수명 미강제
- 수리 라운드 없음

## 의미 검사

`tools/lower.py` 후 `tools/eval_fl_min.py`로 입출력 검사. 전체 FX 런타임이 아니다. Core로 내린 `(defn|let|do|if|null?|get|산술·비교)` 부분집합만 평가한다.

## 결과

| CASE | LOWER | SEMANTIC | FIRST_VALID | 형태 요약 |
|------|-------|----------|-------------|-----------|
| 01 | PASS | PASS | PASS | 중첩 `?`, 곱 |
| 02 | PASS | PASS | PASS | 문자열 `==` 분기 |
| 03 | PASS | PASS | PASS | 앞쪽 바인딩 + `@` 합 |
| 04 | PASS | PASS | PASS | `>=` 분기 |
| 05 | PASS | PASS | PASS | 괄호 산술, 바인딩 없음 |
| 06 | PASS | PASS | PASS | `~` 널 분기 후 제곱 |

- `FIRST_VALID=6/6`
- `SHAPE_DIVERSITY=6` (정규화 키가 여섯 갈래)
- 축약 0, ENTRY 이탈 NO

## 한계

- 모델은 이 세션 Grok. 다른 모델 재현은 다음 순서다.
- `OUTPUT_TOKENS`는 이벤트 없어 `NOT_MEASURED`.
- `eval_fl_min`은 스모크용이다. FX 실행 단계(`NOT_OPENED`)를 대체하지 않는다.
- 형태 다양성은 과제 설계상 가능했고, 실제로 여섯 키가 갈렸다. “모든 약한 과제에서 항상 다양하다”는 일반화는 아니다.

## 순서상 다음

```text
강한 서명 PASS → 약한 서명 PASS → 다른 모델로 U1→U3 재현
```

이 묶음으로 약한 서명 U1은 당일 스모크로 닫는다.
