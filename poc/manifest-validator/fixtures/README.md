# manifest-validator fixtures

Each case:

| file | role |
|------|------|
| `NN-name.call` | `--call` S-expr (one line) |
| `NN-name.expect.json` | expected JSON result (eval ≡ native) |
| `NN-name.meta.json` | `ok` / `code` / `field` summary |

Error codes: `E_REQUIRED`, `E_UNKNOWN_KEY`, `E_BAD_TYPE`, `E_BAD_VALUE`, `E_BAD_VERSION`, `E_EMPTY_TASKS`.

These are **behavioral** result fixtures (code/field/message in the returned map).
Parse/lower location diagnostics stay in `fixtures/parse` / `fixtures/lower`.
