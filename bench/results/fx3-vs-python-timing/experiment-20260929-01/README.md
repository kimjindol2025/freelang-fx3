# FX3·Python 실제 완성 시간 실험

6개 독립 AI trial: FX3 3회, Python 3회.

각 scratch 디렉터리는 이전 생성 코드와 수정 내역 없이 시작한다. Codex
호출 wall time을 AI 생성/수정 시간으로 기록하고, evaluator의 lowering·실행·
테스트 시간을 별도로 기록한다. 첫 출력과 최종 출력, 명령, 종료 코드,
코드·로그 해시는 trial별로 보존한다.

기존 `fx3-vs-python/experiment-20260929-01` 및 Rust 72회 결과는 시간 집계에
포함하지 않는다.
