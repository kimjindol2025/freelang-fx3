# CASE-05 (MEDIUM)

TASK_TEXT: Define `order-total` with `$order`; bind `subtotal` and `tax` from the map and return their sum.
INPUT: `{"subtotal":100,"tax":18}`
EXPECTED_OUTPUT: `118`
RUST_SIGNATURE: `fn order_total(order: &Order) -> i64`
RUST_REFERENCE: `../references/rust/case-05.rs`
FX3_REFERENCE: `../references/fx3/case-05.fx3`
EXPECTED_FL: `../expected/case-05.fl`
