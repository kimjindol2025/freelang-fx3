# Stage 1 prompt pairs

For each `case-XX.md`, insert the exact `TASK_TEXT` and `INPUT` values. Do not
include `EXPECTED_OUTPUT`, `RUST_REFERENCE`, `FX3_REFERENCE`, or `EXPECTED_FL`
in either prompt.

The two prompts expose declaration context at the same level: Rust receives
`RUST_SIGNATURE`, and FX3 receives `FX3_SIGNATURE`. `FX3_SIGNATURE` is only the
function header (`F name[$param,...]`); it contains no body, expected source,
or validation value. `INPUT` is the visible call input for that case. Hidden
validation inputs and outputs are never inserted into either prompt.

## Rust

```text
Write only the Rust function requested below. Use stable rustc and the
standard library only. Do not add crates, file I/O, network calls, or a main
function. Return source code only.

LANGUAGE: Rust
TASK_TEXT: <case TASK_TEXT>
RUST_SIGNATURE: <case RUST_SIGNATURE>
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
FX3_SIGNATURE: <case FX3_SIGNATURE>
INPUT: <case INPUT>
EXPECTED_OUTPUT: withheld from the model
```

The FX3 minimum surface is: `F`, leading `$name=expr` bindings, `?`, `~`,
`@` nested/index get, function calls, maps, arithmetic/comparison operators,
variables, and sequential expressions separated by `;`.

The frozen FX3 declaration headers are:

```text
01 F pick-name[$profile]
02 F add-points[$score,$bonus]
03 F status-label[$score]
04 F upper-city[$city]
05 F order-total[$order]
06 F choose-code[$payload]
07 F fallback-email[$profile]
08 F indexed-code[$rows]
09 F profile-band[$profile]
10 F side-product[$data]
11 F score-band[$data]
12 F matrix-cell[$matrix,$i]
```

For Rust, the case's `RUST_SIGNATURE` is the only type/API context added;
the harness provides the named input types. For FX3, the case's
`FX3_SIGNATURE` is the only declaration context added; the visible `INPUT`
provides the named values and shape. These are recorded inputs, not expected
implementations or examples.
