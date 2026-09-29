# CASE-08 (MEDIUM)

TASK_TEXT: Define `indexed-code` with `$rows` and return the `code` field of the item at numeric index 1.
INPUT: `rows=[{"code":"A1"},{"code":"B2"}]`
EXPECTED_OUTPUT: `"B2"`
RUST_SIGNATURE: `fn indexed_code(rows: &[Row]) -> String`
RUST_REFERENCE: `../references/rust/case-08.rs`
FX3_REFERENCE: `../references/fx3/case-08.fx3`
EXPECTED_FL: `../expected/case-08.fl`
