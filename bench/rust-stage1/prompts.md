# Stage 1 prompt pairs

For each `case-XX.md`, insert the exact `TASK_TEXT` and `INPUT` values. Do not
include `EXPECTED_OUTPUT`, `RUST_REFERENCE`, `FX3_REFERENCE`, or `EXPECTED_FL`
in either prompt.

## Rust

```text
Write only the Rust function requested below. Use stable rustc and the
standard library only. Do not add crates, file I/O, network calls, or a main
function. Return source code only.

LANGUAGE: Rust
TASK_TEXT: <case TASK_TEXT>
INPUT: <case INPUT>
EXPECTED_OUTPUT: withheld from the model
```

## FX3

```text
Write only the requested function in the FX3 Core `.fx3` surface. Use only
the Core syntax described below and return source code only. Do not use a
loop, async, network, database, file I/O, external library, Hot Alias, or a
new runtime feature.

LANGUAGE: FX3 Core
TASK_TEXT: <case TASK_TEXT>
INPUT: <case INPUT>
EXPECTED_OUTPUT: withheld from the model
```

The FX3 minimum surface is: `F`, leading `$name=expr` bindings, `?`, `~`,
`@` nested/index get, function calls, maps, arithmetic/comparison operators,
variables, and sequential expressions separated by `;`.

For Rust, the case's `RUST_SIGNATURE` is the only type/API context added;
the harness provides the named input types. This is recorded information,
not an expected implementation or example.
