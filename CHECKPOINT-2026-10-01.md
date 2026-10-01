# Checkpoint · 2026-10-01

## AIRC
- spec: SPEC.airc
- hot: task-fx3-native-fx-elf-or-corpus
- 완료: FX3 delimiter trailing-semi / hyphen-ident
- 다음: FX3 native FX ELF or corpus

## 다음 Grok에게
너는 FX3 delimiter(하이픈/ident)까지 끝난 상태다. 네이티브 FX ELF 의미 검증 또는 코퍼스를 하면 된다.
1) `python3 ~/.grok/skills/checkpoint/scripts/print-hot.py SPEC.airc` 만 실행
2) `python3 tools/check_delimiter.py` · `python3 tools/check_semantic_min.py` 재현

## 증거
- root cause: `$first-$second`에서 ident가 `-`를 `$` 앞까지 소비
- fix: `tools/lower.py` ident — `-`는 뒤가 이름 문자일 때만 포함
- PASS: lower --check, check_delimiter (ops 6/6), SEMANTIC_MIN=PASS
- native FX ELF: fl-build CGC/링크 BLOCKED → semantic_min으로 실행 안건 개방
