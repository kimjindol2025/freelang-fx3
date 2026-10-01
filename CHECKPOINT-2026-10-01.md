# Checkpoint · 2026-10-01

## AIRC
- spec: SPEC.airc
- hot: task-fx3-corpus-app-gap-or-core-v0-prep
- 완료: FX3 corpus stdlib slice
- 다음: FX3 corpus app gap or Core v0 prep

## 다음 Grok에게
너는 stdlib 코퍼스 조각까지 끝난 상태다. app GAP 정리 또는 Core v0 준비 체크리스트를 하면 된다.
1) `python3 ~/.grok/skills/checkpoint/scripts/print-hot.py SPEC.airc` 만 실행
2) `python3 tools/check_corpus.py` 재현

## 증거
- `CORPUS_STDLIB=PASS` (identity / req-body / str-coerce)
- `CORPUS_APP=NOT_STARTED` · `CORPUS_SELFHOST=NOT_STARTED`
- GAP: server_json, mariadb, fn/closure, loop
- 상세: corpus/CORPUS-2026-10-01.md
