# FX3·Python 실제 작업 비교 보고서

```text
EXPERIMENT=fx3-vs-python/experiment-20260929-01
STATUS=BLOCKED
EXECUTION_VALIDATION=PASS
DECISION=판단 보류
RUST_RESULTS_MIXED=NO
COMMIT=NOT_COMMITTED
PUSH=NOT_PERFORMED
```

## 작업과 동일 조건

주문 `{subtotal, shipping}`의 최종 금액을 계산했다. `subtotal >= 5000`이면 배송비를 면제하고, 아니면 배송비를 더한다. 두 구현은 같은 4개 입력과 같은 기대 출력으로 검사했다.

- FX3: AI 함수 `.fx3` → `tools/lower.py` → canonical `.fl` → FreeLang 실행기
- Python: AI 함수 → Python 3 실행기
- AI 작성자: 같은 Codex/GPT-5 세션
- 기존 기준 코드·golden fixture·Rust 72회 결과: 사용하지 않음

## 결과

| 항목 | FX3 | Python |
|---|---:|---:|
| 첫 시도 정답 | lowering 실패 | 2/4 |
| 최종 실제 입출력 | 4/4 PASS | 4/4 PASS |
| 수정 횟수 | 1 | 1 |
| 복구 전후 | `ERROR 기대 '}'` → lowering PASS | 2개 조건 오류 → 4/4 PASS |
| 최종 AI 코드 바이트 | 126 | 193 |

최종 소스 바이트만 보면 FX3가 34.72% 짧다. 그러나 이것은 모델 토큰·작성 시간의 직접 측정이 아니다.

일괄 실행 시간은 Python 100ms, FX3 실행 143ms였다. FX3의 lowering 142ms까지 포함하면 전체 경로는 285ms로, 이번 작업에서는 실행 경로 비용 이점이 확인되지 않았다.

## 판정

**다음 같은 작업에서 AI가 FX3를 쓸 것인가: 판단 보류**

정확성은 유지됐지만, 수정 횟수는 동률이고 FX3는 첫 시도에서 lowering 오류가 났다. 모델 생성 latency가 이 세션에 노출되지 않아 작성 시간 기반의 1% 이상 비용 이점을 검증할 수 없다. 따라서 짧은 소스만으로 FX3 선택을 확정하지 않는다.

## 증거 한계

AI 서비스의 실제 생성 latency는 계측되지 않았다. `logs/authoring-timing.tsv`에는 파일 저장 시각만 기록되어 있으며, 이를 작성 시간으로 오인하지 않는다. 이 필수 비용 증거가 빠졌으므로 전체 비교 상태는 `BLOCKED`다.

모든 실행 로그와 해시는 `logs/`에 있다. `logs/evidence-sha256.tsv`는 주요 입력, 프롬프트, 첫·최종 코드, lowering, 실행, 수정 diff를 다시 읽을 수 있게 고정한다.
