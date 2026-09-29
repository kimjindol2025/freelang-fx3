# Termux Rust linker receipt

## Diagnosis

`rustc -vV` reported:

```text
rustc 1.94.1 (e408947bf 2026-03-25) (built from a source tarball)
host: aarch64-linux-android
release: 1.94.1
LLVM version: 21.1.8
```

The initial link used `/usr/bin/cc` and `/usr/bin/ld` because `/usr/bin`
preceded Termux in `PATH`. That host linker could not resolve Android
`liblog` or the unwind library. Termux provides clang at
`/data/data/com.termux/files/usr/bin/clang`; Android `liblog.so` is present at
`/system/lib64/liblog.so`.

## Minimal correction

No sudo, package installation, symlink, global environment edit, or source
change was needed. Use the Termux clang driver for the Rust invocation:

```text
rustc -C linker=/data/data/com.termux/files/usr/bin/clang \
  bench/rust-stage1/validation/reference_harness.rs \
  -o /tmp/fx3-rust-stage1-reference
```

`RUSTC_LINKER` alone was not sufficient for this direct `rustc` invocation;
the explicit `-C linker=...` setting is the minimal reliable correction.
