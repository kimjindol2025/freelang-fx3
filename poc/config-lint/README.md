# POC #2 · FX3 config lint

Delegated-run only: `.fx3` → `fx3_lower` → `.fl` → eval/native.

```text
PROJECT=config-lint
RUN=DELEGATED
RUNTIME_OWNED=NONE
IO_CHANGE=NO
IR_EXEC=NO
```

## Source

- Program: [`../../src/config-lint.fx3`](../../src/config-lint.fx3) — `lint-config`
- Fixtures: [`fixtures/`](fixtures/)

## Rules

Allowed keys: `name`, `env`, `port`, `debug` (exactly these four).

| Field | Rule | Error |
|-------|------|-------|
| name | non-empty string | `E_REQUIRED` / `E_BAD_TYPE` / `E_BAD_VALUE` |
| env | `dev` \| `prod` \| `test` | `E_REQUIRED` / `E_BAD_TYPE` / `E_BAD_VALUE` |
| port | number `1..65535` | `E_REQUIRED` / `E_BAD_TYPE` / `E_BAD_PORT` |
| debug | boolean | `E_REQUIRED` / `E_BAD_TYPE` |
| other key | deny | `E_UNKNOWN_KEY` |

## Run

```bash
cd /home/kim/kim/platform/freelang-fx3

./bin/fx3 run src/config-lint.fx3 \
  --call "$(cat poc/config-lint/fixtures/01-ok.call)"

./bin/fx3 run src/config-lint.fx3 \
  --call "$(cat poc/config-lint/fixtures/01-ok.call)" \
  --engine=native
```

## Verify

```bash
bash poc/config-lint/scripts/verify.sh
# same:
python3 tools/check_poc.py poc/config-lint
```

## Notes

Same Core/delegation limits as manifest-validator (single `F`, `type-of`, native `==`→`=` adapter, `eval_fl_ext`).
Boolean fields exercise `true`/`false` call literals across eval and native.
