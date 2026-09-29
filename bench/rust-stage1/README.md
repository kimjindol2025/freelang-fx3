# Rust vs FX3 AI benchmark — Stage 1

This is a separate benchmark from the earlier FX-vs-FX3 stage2 run.

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
