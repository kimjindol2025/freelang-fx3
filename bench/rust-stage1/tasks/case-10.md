# CASE-10 (COMPOSED)

TASK_TEXT: Define `side-product` with `$data`; bind `left.value` and `right.value` and return their product.
INPUT: `{"left":{"value":6},"right":{"value":7}}`
EXPECTED_OUTPUT: `42`
RUST_SIGNATURE: `fn side_product(data: &Sides) -> i64`
RUST_REFERENCE: `../references/rust/case-10.rs`
FX3_REFERENCE: `../references/fx3/case-10.fx3`
EXPECTED_FL: `../expected/case-10.fl`
