# CASE-03

TASK_PROMPT: Define `route-payload` with `$req`. Bind `$payload` to `read-payload($req)`, bind `$kind` to `payload.meta.kind`, and when `payload.ok` is true return `accept($kind)`; otherwise return `reject($kind)`.

EXPECTED_FX3: `../expected/case-03.fx3`
EXPECTED_FL: `../expected/case-03.fl`
