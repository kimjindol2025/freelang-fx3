# POC · FX3 project manifest validator

Delegated-run only: `.fx3` → `fx3_lower` → `.fl` → eval/native.

```text
PROJECT=manifest-validator
RUN=DELEGATED
RUNTIME_OWNED=NONE
IO_CHANGE=NO
IR_EXEC=NO
```

## Source

- Program: [`../../src/manifest-validator.fx3`](../../src/manifest-validator.fx3)
- Single Core `F` (AST lower accepts one top-level form)
- Fixtures: [`fixtures/`](fixtures/) (`*.call` / `*.expect.json` / `*.meta.json`)

## Rules

Allowed keys: `name`, `version`, `language`, `tasks`.

| Check | Error code | field |
|-------|------------|-------|
| unknown key | `E_UNKNOWN_KEY` | key name |
| missing required | `E_REQUIRED` | field |
| wrong type | `E_BAD_TYPE` | field |
| empty name / bad language | `E_BAD_VALUE` | field |
| version outside `[1.0.0, 2.0.0)` (string order) | `E_BAD_VERSION` | version |
| empty tasks array | `E_EMPTY_TASKS` | tasks |

Success map: `{ok:true,name,version,language,tasks}`  
Failure map: `{ok:false,code,field,message}`

## Run

```bash
cd /home/kim/kim/platform/freelang-fx3

./bin/fx3 run src/manifest-validator.fx3 \
  --call "$(cat poc/manifest-validator/fixtures/01-ok.call)"

./bin/fx3 run src/manifest-validator.fx3 \
  --call "$(cat poc/manifest-validator/fixtures/01-ok.call)" \
  --engine=native
```

## Verify

```bash
bash poc/manifest-validator/scripts/verify.sh
# same:
python3 tools/check_poc.py poc/manifest-validator
```

## Known limitations

- One top-level `F` only.
- `?` branches cannot hold leading bindings (bind at function head).
- `string?` / `vector?` surface forms unavailable (`?` token) → use `type-of`.
- FX3 lowers `==`; native CGC wants `=` → CLI adapts for `--engine=native`.
- Version compare is lexicographic string order.
- Eval path uses `tools/eval_fl_ext.py` shims; `eval_fl_min.py` is not edited.
- No file/network/process I/O in the FX3 program.
