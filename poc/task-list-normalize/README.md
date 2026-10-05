# POC #3 · FX3 task-list normalize

Proves **fixed array unroll**, **duplicate id check**, and **normalize output**
on the delegated rail (eval ≡ native).

```text
PROJECT=task-list-normalize
RUN=DELEGATED
RUNTIME_OWNED=NONE
```

## Source

- `src/task-list-normalize.fx3` — `normalize-tasks`
- Fixtures: `fixtures/` (12 cases)

## Rules

Root map: only key `tasks` (array, max length 3).

Each task (when present) needs `id` (non-empty string), `name` (non-empty string),
`enabled` (boolean). Extra task keys are stripped in the result.

| Result | Shape |
|--------|--------|
| success | `{ok:true,count:N,t0?:{id,name,enabled},t1?:...,t2?:...}` |
| failure | `{ok:false,code,field,message}` |

Codes: `E_REQUIRED`, `E_UNKNOWN_KEY`, `E_BAD_TYPE`, `E_BAD_VALUE`, `E_DUP_ID`, `E_TOO_MANY`.

### Why `t0..t2` not a new `[]`

Core FX3 **does not lower vector literals**. Normalized lists are emitted as
`count` + slots. Documented in `docs/FX3-DELEGATED-LIMITS.md`.

## Verify

```bash
bash poc/task-list-normalize/scripts/verify.sh
python3 tools/check_poc.py poc/task-list-normalize
```
