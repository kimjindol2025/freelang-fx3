# FX3 문법 안내가 첫 시도 실패를 없애는지

```text
STATUS=PASS
FIRST_ATTEMPT_FAILURE_REMOVED=PASS
FIRST_TRIALS=3/3 PASS
FINAL_TRIALS=3/3 PASS
LANGUAGE_OR_LOWERER_CHANGED=NO
COMMIT=NOT_COMMITTED
PUSH=NOT_PERFORMED
```

## 변경 범위

기존 FX3 prompt 703바이트에 다음 두 규칙만 추가해 870바이트로 만들었다.

- `F name[$params]{본문}`: 함수 본문은 중괄호로 감싼다.
- 각 leading binding 식 뒤에는 `;`가 필수다.

주문 계산 정답 예제, 이전 생성 코드·오류·수정 내역은 제공하지 않았다.
언어 문법, lowerer, 테스트, Python 결과는 변경하지 않았다.

## 세 trial

| trial | 첫 코드의 `{}` | 첫 코드의 `;` | 첫 lowering | 첫 실행·테스트 | 수정 | active 전체 |
|---|---|---|---|---|---:|---:|
| guided-1 | 사용 | 사용 | PASS | 4/4 PASS | 0 | 32,397ms |
| guided-2 | 사용 | 사용 | PASS | 4/4 PASS | 0 | 22,942ms |
| guided-3 | 사용 | 사용 | PASS | 4/4 PASS | 0 | 27,183ms |

첫 시도 정답률은 3/3으로 개선됐다. 첫 lowering·실행·테스트가 모두
각 trial에서 exit 0이었다.

## 이전 결과 및 Python 비교

| 집단 | 첫 정답률 | 최종 정답률 | active 전체 중앙값 |
|---|---:|---:|---:|
| 기존 FX3 | 0/3 | 3/3 | 116,573ms |
| FX3 guided | 3/3 | 3/3 | 27,183ms |
| 기존 Python | 3/3 | 3/3 | 15,506ms |

문법 안내는 FX3의 첫 시도 실패를 제거했다. 그러나 guided FX3의 전체
완성 시간 중앙값은 Python보다 75.3% 길다(27,183ms 대 15,506ms). 정확성은
Python과 동률이므로, 완료 조건에 따라 다음 작업의 FX3 선택은 **NO**로
유지한다.

프롬프트 diff, 각 trial의 AI 이벤트·생성 코드·lowering·실행·테스트 로그와
해시는 이 디렉터리에 보존했다.
