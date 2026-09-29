# CASE-01

TASK_PROMPT: Define `fetch-rate` with `$req`. Bind `$currency` to the uppercase value at `req.params.currency`, bind `$body` to `http-get-body(RATE_URL)`, and return `json-err("missing rate")` when `$body` is null; otherwise return `json-ok($body)`.

EXPECTED_FX3: `../expected/case-01.fx3`
EXPECTED_FL: `../expected/case-01.fl`
