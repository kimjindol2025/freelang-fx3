# Stage 1 AI prompt pairs

The same `TASK_PROMPT` from each file in `bench/tasks/` is used for both surfaces. No expected source example is included in either prompt.

## A — existing FX `.fl`

```text
Write the requested function in the existing FX `.fl` surface. Use only the syntax needed by the task and return only the source code.

TASK_PROMPT: <insert the exact TASK_PROMPT value from the case file>
```

## B — FX3 Core `.fx3`

```text
Write the requested function in the FX3 Core `.fx3` surface. Use only the syntax needed by the task and return only the source code.

TASK_PROMPT: <insert the exact TASK_PROMPT value from the case file>
```

PAIRING=READY
INFORMATIONAL_ASYMMETRY=NONE_BY_DESIGN
AI_GENERATED_OUTPUTS=NOT_PRESENT
