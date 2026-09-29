# CASE-02

TASK_PROMPT: Define `welcome-profile` with `$req`. Bind `$body` to `load-profile($req)`, bind `$name` to the uppercase value at `body.user.name`, and return `missing-name()` when `$name` is null; otherwise return `welcome($name)`.

EXPECTED_FX3: `../expected/case-02.fx3`
EXPECTED_FL: `../expected/case-02.fl`
