# CASE-11 (COMPOSED)

TASK_TEXT: Define `score-band` with `$data`; bind `a`, `b`, and `c`, calculate their sum, and return `"high"` when the sum is at least 100 or `"low"` otherwise.
INPUT: `{"a":40,"b":35,"c":30}`
EXPECTED_OUTPUT: `"high"`
RUST_SIGNATURE: `fn score_band(data: &Metrics) -> &'static str`
RUST_REFERENCE: `../references/rust/case-11.rs`
FX3_REFERENCE: `../references/fx3/case-11.fx3`
EXPECTED_FL: `../expected/case-11.fl`
