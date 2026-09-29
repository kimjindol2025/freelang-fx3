# Stage 1 AI prompt pairs

The same `TASK_PROMPT` from each file in `bench/tasks/` is used for both surfaces. No expected source example is included in either prompt.

## A — existing FX `.fl`

```text
Write the requested function in the existing FX `.fl` surface. Use only the syntax needed by the task and return only the source code.

TASK_PROMPT: <insert the exact TASK_PROMPT value from the case file>
```

## B — FX3 Core `.fx3`

FX3 생성 프롬프트에는 [AI-ENTRY.md](../AI-ENTRY.md)의 최소 조각을 넣는다. 안내 없는 프롬프트는 첫 시도에서 `{}`와 `;`를 빠뜨리는 실패가 재현됐다 (`experiment-20260929-02`).

```text
Write the requested function in the FX3 Core `.fx3` surface. Use only the syntax needed by the task and return only the source code.

DIALECT: FX3 Core (.fx3). Meaning lowers to existing FX .fl. No new runtime.
Rules:
- Function form: F name[$params]{body}. Body braces are required.
- Every leading binding `$name=expr` must end with `;`.
- Bindings only at the start of a block. Names stay full (no one-letter opcodes).
- Expression end is `;`. Newlines are not meaningful.
Example:
F handle-rate-single[$req]{$cur=str_upper(@$req.params.currency);$body=http-get-body(RATE_URL);?~$body{json-err("환율 API 오류")}{json-ok($body)}}

TASK_PROMPT: <insert the exact TASK_PROMPT value from the case file>
```

PAIRING=READY
INFORMATIONAL_ASYMMETRY=FX3_ENTRY_CONTRACT_ONLY
AI_ENTRY=AI-ENTRY.md
AI_GENERATED_OUTPUTS=NOT_PRESENT
