#!/usr/bin/env bash
# FX3 → lower → freelang-v11-fx ELF 의미 검증 (--no-net)
set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FX_ROOT="${FX_ROOT:-/home/kim/kim/platform/freelang-v11-fx}"
BUILD="$FX_ROOT/fl-build.sh"
LOWER=(python3 "$ROOT/tools/lower.py")
WORKDIR="${TMPDIR:-/tmp}/fx3-native-$$"
mkdir -p "$WORKDIR"
trap 'rm -rf "$WORKDIR"' EXIT

if [[ ! -x "$BUILD" ]]; then
  echo "FX_NATIVE=BLOCKED"
  echo "CAUSE=missing $BUILD" >&2
  exit 2
fi

# args: name fx3_src call_expr expect_stdout
run_case() {
  local name="$1" src="$2" call="$3" expect="$4"
  local fl="$WORKDIR/$name.fl"
  local bin="$WORKDIR/$name"
  {
    "${LOWER[@]}" <<<"$src"
    printf '(println %s)\n' "$call"
  } >"$fl"
  if ! bash "$BUILD" "$fl" "$bin" --no-net >"$WORKDIR/$name.build.log" 2>&1; then
    echo "FAIL $name build"
    tail -20 "$WORKDIR/$name.build.log" >&2
    return 1
  fi
  local got
  got="$("$bin" 2>/dev/null | tr -d '\r' | tail -n 1)"
  if [[ "$got" != "$expect" ]]; then
    echo "FAIL $name got=$got expect=$expect"
    return 1
  fi
  echo "PASS $name"
  return 0
}

failed=0
run_case sum 'F sum[$a,$b]{$a+$b;}' '(sum 2 3)' '5' || failed=1
run_case multiply 'F multiply[$left,$right]{$left*$right;}' '(multiply 4 5)' '20' || failed=1
run_case subtract 'F subtract[$first,$second]{$first-$second;}' '(subtract 10 3)' '7' || failed=1
run_case square 'F square-or-zero[$value]{?~$value{0}{$value*$value};}' '(square-or-zero 4)' '16' || failed=1
run_case madd 'F multiply-add[$a,$b,$c]{$a*$b+$c;}' '(multiply-add 2 3 4)' '10' || failed=1
run_case dpos 'F double-positive[$number]{?$number>0{$number*2}{0};}' '(double-positive 5)' '10' || failed=1
run_case dneg 'F double-positive[$number]{?$number>0{$number*2}{0};}' '(double-positive -1)' '0' || failed=1

if [[ "$failed" -ne 0 ]]; then
  echo "FX_NATIVE=FAIL"
  exit 1
fi
echo "FX_NATIVE=PASS"
exit 0
