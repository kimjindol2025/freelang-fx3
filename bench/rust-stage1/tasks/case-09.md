# CASE-09 (COMPOSED)

TASK_TEXT: Define `profile-band` with `$profile`; bind `name` and `score` from the nested profile, and return `name` when score is at least 70 or `"unrated"` otherwise.
INPUT: `{"name":"Mina","score":81}`
EXPECTED_OUTPUT: `"Mina"`
RUST_SIGNATURE: `fn profile_band(profile: &ScoredProfile) -> String`
RUST_REFERENCE: `../references/rust/case-09.rs`
FX3_REFERENCE: `../references/fx3/case-09.fx3`
EXPECTED_FL: `../expected/case-09.fl`
