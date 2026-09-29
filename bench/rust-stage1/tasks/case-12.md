# CASE-12 (COMPOSED)

TASK_TEXT: Define `matrix-cell` with `$matrix` and `$i`, and return the value at row index `$i` and column index 0.
INPUT: `matrix=[[10,11],[20,21]], i=1`
EXPECTED_OUTPUT: `20`
RUST_SIGNATURE: `fn matrix_cell(matrix: &[Vec<i64>], i: usize) -> i64`
RUST_REFERENCE: `../references/rust/case-12.rs`
FX3_REFERENCE: `../references/fx3/case-12.fx3`
EXPECTED_FL: `../expected/case-12.fl`
