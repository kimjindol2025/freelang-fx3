# FX3 delegated POC rail

작은 업무 도구를 **위임 실행**으로만 검증하는 자리. 전용 VM 없음.

## 새 POC 추가

1. `src/<tool>.fx3` — 단일 top-level `F`, 순수 검증/변환
2. `poc/<tool>/poc.json`

```json
{
  "name": "<tool>",
  "source": "src/<tool>.fx3",
  "pass_tag": "POC_<TOOL>",
  "min_cases": 6
}
```

3. `poc/<tool>/fixtures/` — `NN-name.call` / `.expect.json` / `.meta.json`
4. `poc/<tool>/scripts/verify.sh` → `python3 tools/check_poc.py poc/<tool>`
5. `bash poc/<tool>/scripts/verify.sh` 또는 `python3 tools/check_poc.py all`

한계: [docs/FX3-DELEGATED-LIMITS.md](../docs/FX3-DELEGATED-LIMITS.md).

## 현재 POC

| name | source | verify |
|------|--------|--------|
| manifest-validator | `src/manifest-validator.fx3` | `poc/manifest-validator/scripts/verify.sh` |
| config-lint | `src/config-lint.fx3` | `poc/config-lint/scripts/verify.sh` |
| task-list-normalize | `src/task-list-normalize.fx3` | `poc/task-list-normalize/scripts/verify.sh` |
