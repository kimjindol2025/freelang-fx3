# FX3 vs Python 실제 작업 비교 — experiment-20260929-01

상태: 실행 증거 수집 중

이번 실험은 Rust stage1 72회 결과와 별개다. 기존 기준 코드, golden fixture, 기존 AI 결과를 사용하지 않는다.

## 작업

주문 레코드 `{subtotal, shipping}`를 받아, subtotal이 5000 이상이면 배송비를 면제하고 그렇지 않으면 배송비를 더한 최종 금액을 반환한다.

- 같은 입력: JSON object
- 같은 검증: 4개 입력의 표준출력 정수 비교
- FX3 경로: `.fx3` → 기존 `tools/lower.py` → canonical `.fl` → 기존 FreeLang 실행기
- Python 경로: `python3`로 직접 실행
- AI 작성자: 동일 Codex/GPT-5 세션. 정확한 서비스 모델 ID와 생성 latency는 이 환경에서 노출되지 않으므로, 파일 저장 시각과 실행 시간만 증거로 남긴다.

## 판정 규칙

두 구현 모두 실제 입력·출력 케이스 4/4를 통과해야 한다. 첫 시도 실패 후 최종 수정이 통과하면 복구로 기록한다. 실행 로그, 해시, 수정 diff, 명령을 보존한다.
