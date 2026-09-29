# CASE-06 (MEDIUM)

TASK_TEXT: Define `choose-code` with `$payload`; return the nested `code` when numeric `ok` is at least 1, otherwise return `"rejected"`.
INPUT: `{"ok":1,"code":"A7"}`
EXPECTED_OUTPUT: `"A7"`
RUST_SIGNATURE: `fn choose_code(payload: &Payload) -> String`
RUST_REFERENCE: `../references/rust/case-06.rs`
FX3_REFERENCE: `../references/fx3/case-06.fx3`
EXPECTED_FL: `../expected/case-06.fl`
