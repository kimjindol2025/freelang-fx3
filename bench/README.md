# FX3 vs FX AI surface benchmark — Stage 1

This directory is an experiment harness, not part of the FX3 language contract.

```text
BENCHMARK=FX3_VS_FX_AI_SURFACE_BENCHMARK_STAGE1
BENCH_CASES=12
CONTRACT_FIXTURES_CHANGED=0
FIXTURE_05=NO
FX3_RUNTIME=NO
FX_EXECUTION=NOT_OPENED
```

## Scope

The benchmark compares two authoring surfaces for the same target meaning:

- A: write existing FX `.fl` directly.
- B: write FX3 Core `.fx3`, then lower it with the existing `tools/lower.py`.

Cases 01–03 vary the leading-binding / nested-get / conditional pattern, 04–06 vary sequential blocks and comparisons, 07–09 vary map construction, and 10–12 vary indexed and nested access. They use only forms already present in the locked 01–04 surface. They are not golden fixtures and do not create fixture 05.

Each task file contains the three case fields `TASK_PROMPT`, `EXPECTED_FX3`, and `EXPECTED_FL`; the two expected paths point to the exact source and canonical target artifacts in `bench/expected/`.

## Deterministic baseline

`bench/results/baseline.tsv` records UTF-8 file bytes including the final newline. `CHAR_REDUCTION_PERCENT` is:

```text
(FX_BYTES - FX3_BYTES) / FX_BYTES * 100
```

The weighted aggregate is `1093` FX3 bytes versus `1610` FX bytes: `517` fewer bytes and `32.11%` reduction. Token counts are `NOT_MEASURED`; no model-specific tokenizer was available in the repository/environment, and no tokenizer dependency was installed.

## Lowering check

The existing lowerer is unchanged. To repeat the case checks:

```bash
for f in bench/expected/case-*.fx3; do
  python3 tools/lower.py "$f" | cmp -s "${f%.fx3}.fl" || exit 1
done
```

The recorded result is `FX3_EXPECTED_LOWERING=12/12 PASS` and `EXPECTED_FL_BYTE_MATCH=12/12 PASS`.

## AI trial preparation

`bench/prompts.md` defines the paired prompts. The task wording is shared; only the requested surface changes. No fabricated model outputs are included. `bench/results/ai-trial-schema.json` defines the later per-trial fields:

```text
FIRST_PASS_VALID
LOWERING_PASS
TARGET_MATCH
CORRECTION_COUNT
EDIT_SPAN
OUTPUT_BYTES
OUTPUT_TOKENS
GENERATION_ERROR_TYPE
```

`AI_TRIALS=NOT_RUN` for this stage.
