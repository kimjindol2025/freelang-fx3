# Rust vs FX3 AI benchmark — Stage 1

This is a separate benchmark from the earlier FX-vs-FX3 stage2 run.

## Controlled baseline

The counted run uses `run_stage1_locked.sh` only. Before any model call it
verifies `freeze-manifest.tsv`, which fixes the prompt specification, the FX3
declaration headers, the C10 calculation, and the protected task/reference/
golden/lowering bytes.

Prompt inspection does not call the model:

```bash
bash bench/rust-stage1/run_stage1_locked.sh /tmp/fx3-stage1-check prompt FX3 01
```

C10 is calculated from an evidence-backed `tool-maintenance.tsv`:

```bash
bash bench/rust-stage1/run_stage1_locked.sh RUN_ROOT c10
```

When both language totals are zero, C10 is `측정 불가`; zero is
never treated as a passing maintenance comparison. Positive maintenance rows
must include elapsed milliseconds and evidence.

```text
TASK=FX3_VS_RUST_AI_BENCHMARK_STAGE1
CASES=12
EASY=4
MEDIUM=4
COMPOSED=4
TRIALS=72
RUST_TRIALS=36
FX3_TRIALS=36
CORE_CHANGED=NO
FIXTURE_01_04_CHANGED=NO
NEW_FX3_SYNTAX=NO
HOT_ALIAS=NO
FX3_RUNTIME_ADDED=NO
```

Each case has one requirement, input, expected output, Rust reference, FX3
reference, and canonical `.fl` target. The reference files are evaluation
criteria only and are never included in generation prompts.

The paired prompts differ only in the requested surface and the minimum
language-specific type/API information needed to produce runnable code. Every
trial is independent and uses a fresh CLI process. Previous outputs and
expected source are not shown.

No result table is included until the 72 generations and both validation
pipelines have actually run. A failed or unavailable validation is recorded as
`FAIL` or `BLOCKED`, never as a fabricated pass.

## Harness fixes (post run-20260929-02)

`run-20260929-02` stays as historical evidence. These runner bugs contaminated
that score and are fixed in `run_stage1_locked.sh` for the next measured run:

1. Rust hidden sources used `$w.hidden.rs`, so `rustc` rejected crate names
   containing `.` (example: `case_01_trial_1_initial.rs.hidden`). Hidden
   sources now use `case-XX-trial-N-tag-hidden.rs`.
2. Row `validation_ms` stayed `0` because the runner never copied
   `VALIDATION_MS`. It now accumulates after each validate call.
3. FX3 visible lowering failures skipped the hidden log, so
   `row_complete` stayed `NO`. A `HIDDEN_SKIPPED` hidden log is always written.
4. The row `printf` format had an extra `%s`; field count is now 25.
