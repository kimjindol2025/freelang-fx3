# CASE-07 (MEDIUM)

TASK_TEXT: Define `fallback-email` with `$profile`; return `"none"` when the `email` field is null or missing, otherwise return the email unchanged.
INPUT: `{}`
EXPECTED_OUTPUT: `"none"`
RUST_SIGNATURE: `fn fallback_email(profile: &EmailProfile) -> String`
RUST_REFERENCE: `../references/rust/case-07.rs`
FX3_REFERENCE: `../references/fx3/case-07.fx3`
EXPECTED_FL: `../expected/case-07.fl`
