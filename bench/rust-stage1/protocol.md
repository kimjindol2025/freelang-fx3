# Rust vs FX3 AI benchmark — Stage 1 protocol

```text
TASK=FX3_VS_RUST_AI_BENCHMARK_STAGE1
CASES=12
TRIALS=72
RUST_TRIALS=36
FX3_TRIALS=36
MODEL=gpt-5.6-luna
REASONING_EFFORT=low
TEMPERATURE=CLI_DEFAULT_NOT_EXPLICITLY_CONFIGURED
SESSION=INDEPENDENT_EPHEMERAL_PROCESS
NO_DAEMON_FLAG=CLI_NOT_EXPOSED
PREVIOUS_OUTPUTS_SHOWN=NO
EXPECTED_CODE_SHOWN=NO
EXPECTED_OUTPUT_SHOWN=NO
CORE_CHANGED=NO
FIXTURE_01_04_CHANGED=NO
NEW_FX3_SYNTAX=NO
HOT_ALIAS=NO
FX3_RUNTIME_ADDED=NO
AI_TIME_LIMIT_SECONDS=120
MAX_REPAIR_ROUNDS=2
VALIDATION_TIME_LIMIT_SECONDS=30
RESULT_RECORDS=72
NO_FAKE_RESULTS=YES
NO_CHERRY_PICK=YES
PRE_MEASUREMENT_FREEZE=REQUIRED
HIDDEN_CASES_PER_TASK=1
CRITERIA=10
```

Rust validation is `AI output -> rustc -> harness -> expected output` using
only the standard library. FX3 validation is `AI output -> existing
tools/lower.py -> canonical .fl -> existing FX execution path -> expected
output`. No generated program is accepted as a pass without an actual
validation command.

The first generated output is checked before any correction. If repair is
run, the prompt and edit span are recorded; no failed answer is shown to a
later independent trial. Results are kept under a new run directory and are
not mixed with the discarded FX/FX3 stage2 artifacts.

The final report must use `OBSERVED_RUST_ADVANTAGES`,
`OBSERVED_FX3_ADVANTAGES`, and `NO_CLEAR_DIFFERENCE`; it must not emit a
`WINNER` field.

## Fixed measurements

Every trial is recorded in one TSV row and has a matching prompt file,
generated-source file, visible-validation log, hidden-validation log, event
log, and (when a repair is attempted) repair prompt/source/log plus rollback
before/after evidence. Missing evidence makes the row `UNVERIFIED` and it is
excluded from success rates. Existing reference files, expected files, and
lowering outputs are never counted as generated code.

## Frozen FX3 disposal criteria

These ten criteria are frozen before the first counted model call. A criterion
is a comparison of the FX3 value against the Rust value, except C09 and C10,
which are evidence gates. `PASS` means the criterion supports continuing FX3;
`FAIL` means it does not; `측정 불가` means the required denominator or evidence
is absent. A one-percentage-point advantage is the minimum useful difference.
For lower-is-better metrics, a 1% relative improvement is required.

```text
C01 FIRST_ATTEMPT_CORRECTNESS
    value = first-output trials passing BOTH visible and hidden tests / 36
    PASS if FX3 >= Rust + 1 percentage point; FAIL otherwise.

C02 FINAL_CORRECTNESS
    value = final-output trials passing BOTH visible and hidden tests / 36
    PASS if FX3 >= Rust + 1 percentage point; FAIL otherwise.

C03 AI_COMPLETION_TIME
    value = median AI_WORK_MS over all complete trials (36 per language)
    PASS if FX3 <= Rust * 0.99; FAIL otherwise.
    Compiler, lowerer, program, and hidden-test time are excluded.

C04 CORRECTION_COUNT
    value = mean submitted repair attempts over all complete trials
    PASS if FX3 <= Rust * 0.99; FAIL otherwise.
    A repair that fails or is rolled back still counts.

C05 ERROR_RECURRENCE
    value = repair attempts whose post-repair error class equals the
            immediately preceding error class / repair attempts with a
            recorded post-repair validation result
    PASS if FX3 <= Rust * 0.99; FAIL otherwise.
    If both denominators are zero, this criterion is 측정 불가.

C06 ROLLBACK_SUCCESS
    value = rollback attempts with YES / rollback attempts
    PASS if FX3 >= Rust + 1 percentage point; FAIL otherwise.
    YES requires byte restoration AND a separate post-restore validation.

C07 ROLLBACK_STATE_INTEGRITY
    value = rollback attempts with matching before/after source SHA256 and
            matching normalized validation outcome / rollback attempts
    PASS if FX3 >= Rust + 1 percentage point; FAIL otherwise.
    Missing before, after, or post-restore evidence is not success.

C08 HIDDEN_VALIDATION
    value = final-output trials passing the undisclosed extra test / 36
    PASS if FX3 >= Rust + 1 percentage point; FAIL otherwise.
    The hidden input/output is never placed in a generation or repair prompt.

C09 RAW_EVIDENCE_COMPLETENESS
    value = complete, independently re-readable trial rows / 72 planned rows
    PASS only if the value is 100% AND every row has all required hashes,
          timestamps, generated source, validation logs, and event evidence.
    Otherwise FAIL; if the run is interrupted before a denominator can be
    established, 측정 불가.

C10 TOOL_MAINTENANCE_TIME
    value = post-freeze milliseconds spent changing the benchmark, lowerer,
            compiler setup, or validator, recorded in tool-maintenance.tsv
    PASS if FX3 maintenance time <= Rust maintenance time * 0.99.
    An empty or missing maintenance log is 측정 불가, not zero.
```

For C01/C02/C08, a trial is counted only when its row is `RECORD_COMPLETE=YES`
and the corresponding validation evidence is independently re-read. C03-C05
use only complete rows. A language value is `측정 불가` when its required
denominator is zero; a comparison criterion is `측정 불가` if either language
value is unavailable. C09 is a run-level gate and is not converted into an
AI success rate.

```text
LANGUAGE
CASE
TRIAL
MODEL
PROMPT_SHA256
START_UTC
END_UTC
AI_WORK_MS
VALIDATION_MS
FIRST_PARSE_OR_COMPILE_PASS
FIRST_RUN_PASS
FIRST_OUTPUT_MATCH
FINAL_OUTPUT_MATCH
FIRST_HIDDEN_MATCH
FINAL_HIDDEN_MATCH
CORRECTION_ATTEMPTS
ROLLBACK_ATTEMPTS
ROLLBACK_SUCCESS
ROLLBACK_STATE_INTEGRITY
ERROR_RECURRED
TOOL_MAINTENANCE_MS
ERROR_TYPE
GENERATED_CODE_SHA256
VALIDATION_EXIT
RECORD_COMPLETE
```

`AI_WORK_MS` measures the generation and repair processes only. Compiler,
lowerer, and program execution time is recorded separately in
`VALIDATION_MS`; it is not counted as AI work time.

The initial prompt is run once per independent trial with a 120-second
timeout. A failed trial may receive at most two identical-format repair
rounds, each also limited to 120 seconds. A repair prompt contains only that
trial's current source and its validation error; it never receives another
trial's output or an expected source file.

The installed CLI exposes `--ephemeral` but does not expose a `--no-daemon`
flag. Each trial is therefore a newly spawned `codex exec` process with
`--ephemeral`; the unavailable flag is recorded rather than silently claimed.

Before every repair, the current source is copied to that trial's snapshot and
its source hash plus normalized visible/hidden validation outcome are written
to rollback evidence. If the repair fails, the snapshot is restored and the
restored source is validated again using a new validation log. `ROLLBACK_SUCCESS=YES`
is allowed only when the restored bytes and normalized validation result match
the recorded pre-repair state. `ROLLBACK_STATE_INTEGRITY=YES` additionally
requires matching before/after source hashes and both validation-result files.
A missing snapshot, restore, or revalidation is `UNVERIFIED`, never `YES`.

`CORRECTION_ATTEMPTS` counts submitted repair attempts, including failed
attempts. `ERROR_RECURRED=YES` is written when a repair's post-validation
error class is the same as the preceding failed validation; no repair attempt
means `NA`, not zero recurrence. `FIRST_OUTPUT_MATCH` and
`FIRST_HIDDEN_MATCH` are judged before any repair. `FINAL_OUTPUT_MATCH` and
`FINAL_HIDDEN_MATCH` are judged only after the last recorded validation.
`TOOL_MAINTENANCE_MS` comes from the frozen maintenance log and is not AI
work. Existing reference files, lowering outputs, and fixture outputs are
never counted as AI-generated successes.

## Evidence layout

Each fresh run is isolated below `bench/results/rust-stage1/<run-id>/`:

```text
prompts/<language>/case-XX-trial-N.txt
raw/<language>/case-XX-trial-N.out
events/<language>/case-XX-trial-N.jsonl
validation/<language>/case-XX-trial-N.log
validation/<language>/case-XX-trial-N-hidden.log
snapshots/<language>/case-XX-trial-N/repair-N.out
snapshots/<language>/case-XX-trial-N/repair-N-before.result
snapshots/<language>/case-XX-trial-N/repair-N-after.result
snapshots/<language>/case-XX-trial-N/repair-N-rollback.tsv
trials.tsv
tool-maintenance.tsv
summary.md
```

`trials.tsv` is the only aggregate input. It is independently re-read after
the run and its row count, hashes, validation exits, and record completeness
are checked before any comparison is reported.
