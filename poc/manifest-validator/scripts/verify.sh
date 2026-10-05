#!/usr/bin/env bash
# FX3 delegated-run POC: manifest-validator fixture gate.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
FX3="$ROOT/bin/fx3"
SRC="$ROOT/src/manifest-validator.fx3"
FIX="$ROOT/poc/manifest-validator/fixtures"
cd "$ROOT"

if [[ ! -f "$FX3" ]]; then
  echo "FAIL missing $FX3" >&2
  exit 1
fi
if [[ ! -f "$SRC" ]]; then
  echo "FAIL missing $SRC" >&2
  exit 1
fi

json_eq() {
  python3 -c 'import json,sys; a=json.loads(sys.argv[1]); b=json.loads(sys.argv[2]); sys.exit(0 if a==b else 1)' "$1" "$2"
}

run_engine() {
  local engine="$1" call="$2"
  if [[ "$engine" == "eval" ]]; then
    "$FX3" run "$SRC" --call "$call"
  else
    "$FX3" run "$SRC" --call "$call" --engine=native
  fi
}

failed=0
case_count=0

shopt -s nullglob
for call_file in "$FIX"/*.call; do
  base="$(basename "$call_file" .call)"
  expect_file="$FIX/$base.expect.json"
  meta_file="$FIX/$base.meta.json"
  if [[ ! -f "$expect_file" ]]; then
    echo "FAIL $base missing expect.json" >&2
    failed=1
    continue
  fi
  call="$(tr -d '\n' < "$call_file")"
  want="$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1])),separators=(",",":"),sort_keys=True))' "$expect_file")"
  case_count=$((case_count + 1))

  got_eval="$(run_engine eval "$call")"
  got_native="$(run_engine native "$call")"

  if ! json_eq "$got_eval" "$want"; then
    echo "FAIL $base eval got=$got_eval want=$want" >&2
    failed=1
    continue
  fi
  if ! json_eq "$got_native" "$want"; then
    echo "FAIL $base native got=$got_native want=$want" >&2
    failed=1
    continue
  fi
  if ! json_eq "$got_eval" "$got_native"; then
    echo "FAIL $base eval/native mismatch" >&2
    failed=1
    continue
  fi

  if [[ -f "$meta_file" ]]; then
    meta_ok="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("ok"))' "$meta_file")"
    got_ok="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("ok"))' "$got_eval")"
    if [[ "$meta_ok" != "$got_ok" ]]; then
      echo "FAIL $base meta ok mismatch meta=$meta_ok got=$got_ok" >&2
      failed=1
      continue
    fi
    if [[ "$meta_ok" == "False" ]]; then
      meta_code="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("code"))' "$meta_file")"
      got_code="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("code"))' "$got_eval")"
      meta_field="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("field"))' "$meta_file")"
      got_field="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("field"))' "$got_eval")"
      if [[ "$meta_code" != "$got_code" || "$meta_field" != "$got_field" ]]; then
        echo "FAIL $base code/field meta=$meta_code/$meta_field got=$got_code/$got_field" >&2
        failed=1
        continue
      fi
    fi
  fi
  echo "PASS $base"
done

if [[ "$case_count" -lt 6 ]]; then
  echo "FAIL too few fixtures: $case_count" >&2
  failed=1
fi

# determinism
call_ok="$(tr -d '\n' < "$FIX/01-ok.call")"
r1="$(run_engine eval "$call_ok")"
r2="$(run_engine eval "$call_ok")"
r3="$(run_engine eval "$call_ok")"
if [[ "$r1" == "$r2" && "$r2" == "$r3" ]]; then
  echo "PASS determinism-eval"
else
  echo "FAIL determinism-eval" >&2
  failed=1
fi
n1="$(run_engine native "$call_ok")"
n2="$(run_engine native "$call_ok")"
if [[ "$n1" == "$n2" ]]; then
  echo "PASS determinism-native"
else
  echo "FAIL determinism-native" >&2
  failed=1
fi

# CLI usage
set +e
"$FX3" run "$SRC" >/tmp/fx3-poc-usage.out 2>/tmp/fx3-poc-usage.err
rc=$?
set -e
if [[ "$rc" -eq 2 ]]; then
  echo "PASS cli-usage-missing-call"
else
  echo "FAIL cli-usage want 2 got $rc" >&2
  failed=1
fi

# No forbidden I/O in FX3 source / eval shim (static)
if rg -n 'open\(|Path\(|write_text|urlopen|socket\.|subprocess|http' \
  "$SRC" "$ROOT/tools/eval_fl_ext.py" >/tmp/fx3-poc-io.txt; then
  echo "FAIL forbidden I/O symbols found:" >&2
  cat /tmp/fx3-poc-io.txt >&2
  failed=1
else
  echo "PASS no-forbidden-io-static"
fi

if [[ "$failed" -ne 0 ]]; then
  echo "POC_MANIFEST_VALIDATOR=FAIL"
  exit 1
fi
echo "POC_MANIFEST_VALIDATOR=PASS cases=$case_count"
exit 0
