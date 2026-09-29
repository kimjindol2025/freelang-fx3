#!/usr/bin/env bash
set -u

# Minimal orchestration adapter: Codex CLI, rustc, and the existing FX runner
# are external tools, so this runner intentionally remains a shell boundary.

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
RUN_ROOT=${1:?usage: run_stage1.sh RUN_ROOT}
CLI=/root/.nvm/versions/node/v24.15.0/bin/codex
MODEL=gpt-5.6-luna
AI_LIMIT=120
VALIDATION_LIMIT=30
LINKER=/data/data/com.termux/files/usr/bin/clang
mkdir -p "$RUN_ROOT/rows"

now_ms() { date +%s%3N; }
now_utc() { date -u +%FT%TZ; }
field() { sed -n "s/^$1: //p" "$2" | sed 's/^`//;s/`$//'; }

fx3_signature() {
  case "$1" in
    01) printf '%s' 'F pick-name[$profile]' ;;
    02) printf '%s' 'F add-points[$score,$bonus]' ;;
    03) printf '%s' 'F status-label[$score]' ;;
    04) printf '%s' 'F upper-city[$city]' ;;
    05) printf '%s' 'F order-total[$order]' ;;
    06) printf '%s' 'F choose-code[$payload]' ;;
    07) printf '%s' 'F fallback-email[$profile]' ;;
    08) printf '%s' 'F indexed-code[$rows]' ;;
    09) printf '%s' 'F profile-band[$profile]' ;;
    10) printf '%s' 'F side-product[$data]' ;;
    11) printf '%s' 'F score-band[$data]' ;;
    12) printf '%s' 'F matrix-cell[$matrix,$i]' ;;
    *) return 1 ;;
  esac
}

make_prompt() {
  local lang=$1 case_id=$2 out=$3 task="$ROOT/bench/rust-stage1/tasks/case-$case_id.md"
  local task_text input rust_sig fx3_sig
  task_text=$(field TASK_TEXT "$task")
  input=$(field INPUT "$task")
  rust_sig=$(field RUST_SIGNATURE "$task")
  fx3_sig=$(fx3_signature "$case_id")
  {
    if [ "$lang" = RUST ]; then
      printf '%s\n' 'Write only the Rust function requested below. Use stable rustc and the standard library only. Do not add crates, file I/O, network calls, or a main function. Return source code only.'
      printf 'LANGUAGE: Rust\nRUST_SIGNATURE: %s\nTASK_TEXT: %s\nINPUT: %s\nEXPECTED_OUTPUT: withheld from the model\n' "$rust_sig" "$task_text" "$input"
    else
      printf '%s\n' 'Write only the requested function in the FX3 Core .fx3 surface. Use only F, leading bindings, ?, ~, @ nested/index get, maps, function calls, arithmetic/comparison operators, variables, and ;. Do not use loops, async, network, database, file I/O, external libraries, Hot Alias, or new syntax. Return source code only.'
      printf 'LANGUAGE: FX3 Core\nFX3_SIGNATURE: %s\nTASK_TEXT: %s\nINPUT: %s\nEXPECTED_OUTPUT: withheld from the model\n' "$fx3_sig" "$task_text" "$input"
    fi
  } > "$out"
}

run_ai() {
  local lang=$1 case_id=$2 trial=$3 prompt=$4 out=$5 events=$6 workdir=$7
  mkdir -p "$workdir"
  local start end exit_code
  start=$(now_ms)
  timeout --foreground "${AI_LIMIT}s" "$CLI" exec --ephemeral --ignore-user-config \
    --model "$MODEL" -c model_reasoning_effort=low --skip-git-repo-check \
    --cd "$workdir" --json --output-last-message "$out" - \
    < "$prompt" > "$events" 2>&1
  exit_code=$?
  end=$(now_ms)
  [ -e "$out" ] || : > "$out"
  AI_MS=$((end-start))
  AI_EXIT=$exit_code
}

rust_prefix() {
  local case_id=$1 out=$2
  case "$case_id" in
    01) printf '%s\n' 'struct Profile { name: String }' > "$out" ;;
    02|03|04) : > "$out" ;;
    05) printf '%s\n' 'struct Order { subtotal: i64, tax: i64 }' > "$out" ;;
    06) printf '%s\n' 'struct Payload { ok: i64, code: String }' > "$out" ;;
    07) printf '%s\n' 'struct EmailProfile { email: Option<String> }' > "$out" ;;
    08) printf '%s\n' 'struct Row { code: String }' > "$out" ;;
    09) printf '%s\n' 'struct ScoredProfile { name: String, score: i64 }' > "$out" ;;
    10) printf '%s\n' 'struct Side { value: i64 }' > "$out"; printf '%s\n' 'struct Sides { left: Side, right: Side }' >> "$out" ;;
    11) printf '%s\n' 'struct Metrics { a: i64, b: i64, c: i64 }' > "$out" ;;
    12) : > "$out" ;;
  esac
}

rust_suffix() {
  local case_id=$1 out=$2
  case "$case_id" in
    01) printf '%s\n' 'fn main() { assert_eq!(pick_name(&Profile { name: "Ada".into() }), "Ada"); println!("BENCH_PASS"); }' > "$out" ;;
    02) printf '%s\n' 'fn main() { assert_eq!(add_points(7, 5), 12); println!("BENCH_PASS"); }' > "$out" ;;
    03) printf '%s\n' 'fn main() { assert_eq!(status_label(72), "pass"); println!("BENCH_PASS"); }' > "$out" ;;
    04) printf '%s\n' 'fn main() { assert_eq!(upper_city("seoul"), "SEOUL"); println!("BENCH_PASS"); }' > "$out" ;;
    05) printf '%s\n' 'fn main() { assert_eq!(order_total(&Order { subtotal: 100, tax: 18 }), 118); println!("BENCH_PASS"); }' > "$out" ;;
    06) printf '%s\n' 'fn main() { assert_eq!(choose_code(&Payload { ok: 1, code: "A7".into() }), "A7"); println!("BENCH_PASS"); }' > "$out" ;;
    07) printf '%s\n' 'fn main() { assert_eq!(fallback_email(&EmailProfile { email: None }), "none"); println!("BENCH_PASS"); }' > "$out" ;;
    08) printf '%s\n' 'fn main() { assert_eq!(indexed_code(&[Row { code: "A1".into() }, Row { code: "B2".into() }]), "B2"); println!("BENCH_PASS"); }' > "$out" ;;
    09) printf '%s\n' 'fn main() { assert_eq!(profile_band(&ScoredProfile { name: "Mina".into(), score: 81 }), "Mina"); println!("BENCH_PASS"); }' > "$out" ;;
    10) printf '%s\n' 'fn main() { assert_eq!(side_product(&Sides { left: Side { value: 6 }, right: Side { value: 7 } }), 42); println!("BENCH_PASS"); }' > "$out" ;;
    11) printf '%s\n' 'fn main() { assert_eq!(score_band(&Metrics { a: 40, b: 35, c: 30 }), "high"); println!("BENCH_PASS"); }' > "$out" ;;
    12) printf '%s\n' 'fn main() { assert_eq!(matrix_cell(&vec![vec![10, 11], vec![20, 21]], 1), 20); println!("BENCH_PASS"); }' > "$out" ;;
  esac
}

fx3_call() {
  case "$1" in
    01) printf '%s\n' '(println (pick-name {"name" "Ada"}))' ;;
    02) printf '%s\n' '(println (add-points 7 5))' ;;
    03) printf '%s\n' '(println (status-label 72))' ;;
    04) printf '%s\n' '(println (upper-city "seoul"))' ;;
    05) printf '%s\n' '(println (order-total {"subtotal" 100 "tax" 18}))' ;;
    06) printf '%s\n' '(println (choose-code {"ok" 1 "code" "A7"}))' ;;
    07) printf '%s\n' '(println (fallback-email {}))' ;;
    08) printf '%s\n' '(println (indexed-code [{"code" "A1"} {"code" "B2"}]))' ;;
    09) printf '%s\n' '(println (profile-band {"name" "Mina" "score" 81}))' ;;
    10) printf '%s\n' '(println (side-product {"left" {"value" 6} "right" {"value" 7}}))' ;;
    11) printf '%s\n' '(println (score-band {"a" 40 "b" 35 "c" 30}))' ;;
    12) printf '%s\n' '(println (matrix-cell [[10 11] [20 21]] 1))' ;;
  esac
}

expected() {
  case "$1" in
    01) printf '%s' 'Ada' ;; 02) printf '%s' '12' ;; 03) printf '%s' 'pass' ;;
    04) printf '%s' 'SEOUL' ;; 05) printf '%s' '118' ;; 06) printf '%s' 'A7' ;;
    07) printf '%s' 'none' ;; 08) printf '%s' 'B2' ;; 09) printf '%s' 'Mina' ;;
    10) printf '%s' '42' ;; 11) printf '%s' 'high' ;; 12) printf '%s' '20' ;;
  esac
}

classify() {
  local log=$1
  if grep -q 'timed out\|TIMEOUT' "$log"; then printf '%s' TIMEOUT
  elif grep -q 'lower.py\|LowerError\|기대' "$log"; then printf '%s' LOWERING
  elif grep -q 'error\|Error\|error:' "$log"; then printf '%s' COMPILE
  else printf '%s' OTHER; fi
}

validate_rust() {
  local case_id=$1 source=$2 log=$3 tag=$4
  local wrapper="$RUN_ROOT/validation/rust/case-$case_id-trial-$TRIAL-$tag.rs"
  local bin="/tmp/fx3-rust-stage1-rust-$case_id-$TRIAL-$tag"
  local prefix="$wrapper.prefix" suffix="$wrapper.suffix" start end
  rust_prefix "$case_id" "$prefix"; rust_suffix "$case_id" "$suffix"
  cat "$prefix" "$source" "$suffix" > "$wrapper"
  start=$(now_ms)
  rustc -C linker="$LINKER" "$wrapper" -o "$bin" > "$log" 2>&1
  local compile_exit=$?
  if [ "$compile_exit" -eq 0 ]; then
    timeout --foreground "${VALIDATION_LIMIT}s" "$bin" >> "$log" 2>&1
    RUN_EXIT=$?
  else RUN_EXIT=$compile_exit; fi
  end=$(now_ms); VALIDATION_MS=$((end-start)); VALIDATION_EXIT=$RUN_EXIT
  if [ "$compile_exit" -eq 0 ] && [ "$RUN_EXIT" -eq 0 ] && grep -q 'BENCH_PASS' "$log"; then
    VALIDATION_STATUS=PASS; PARSE_PASS=YES; RUN_PASS=YES; MATCH=YES
  elif [ "$compile_exit" -eq 0 ]; then
    VALIDATION_STATUS=FAIL; PARSE_PASS=YES; RUN_PASS=NO; MATCH=NO
  else
    VALIDATION_STATUS=FAIL; PARSE_PASS=NO; RUN_PASS=NO; MATCH=NO
  fi
  rm -f "$bin" "$wrapper" "$prefix" "$suffix"
}

validate_fx3() {
  local case_id=$1 source=$2 log=$3 tag=$4
  local lower="$RUN_ROOT/validation/fx3/case-$case_id-trial-$TRIAL-$tag.fl"
  local wrapper="$RUN_ROOT/validation/fx3/case-$case_id-trial-$TRIAL-$tag-run.fl"
  local start end compile_exit run_exit actual
  start=$(now_ms)
  python3 "$ROOT/tools/lower.py" "$source" > "$lower" 2> "$log"
  compile_exit=$?
  if [ "$compile_exit" -eq 0 ]; then
    cat "$lower" > "$wrapper"; fx3_call "$case_id" >> "$wrapper"
    timeout --foreground "${VALIDATION_LIMIT}s" /root/lang/freelang-v11/bin/fl run "$wrapper" >> "$log" 2>&1
    run_exit=$?; actual=$(tail -1 "$log")
  else run_exit=$compile_exit; actual=; fi
  end=$(now_ms); VALIDATION_MS=$((end-start)); VALIDATION_EXIT=$run_exit
  if [ "$compile_exit" -eq 0 ] && [ "$run_exit" -eq 0 ] && [ "$actual" = "$(expected "$case_id")" ]; then
    VALIDATION_STATUS=PASS; PARSE_PASS=YES; RUN_PASS=YES; MATCH=YES
  elif [ "$compile_exit" -eq 0 ]; then
    VALIDATION_STATUS=FAIL; PARSE_PASS=YES; RUN_PASS=NO; MATCH=NO
  else
    VALIDATION_STATUS=FAIL; PARSE_PASS=NO; RUN_PASS=NO; MATCH=NO
  fi
  rm -f "$lower" "$wrapper"
}

repair_prompt() {
  local lang=$1 case_id=$2 initial_prompt=$3 source=$4 log=$5 out=$6
  cat "$initial_prompt" > "$out"
  printf '\nThe first attempt failed validation. Repair only this trial. Return only the complete corrected source code. Do not add a main function.\nCURRENT_SOURCE:\n' >> "$out"
  cat "$source" >> "$out"
  printf '\nVALIDATION_LOG:\n' >> "$out"
  cat "$log" >> "$out"
}

run_one() {
  local lang=$1 case_id=$2 trial=$3
  TRIAL=$trial
  local base="case-$case_id-trial-$trial"
  if [ -e "$RUN_ROOT/rows/${lang,,}-$base.tsv" ]; then return 0; fi
  local prompt="$RUN_ROOT/prompts/${lang,,}/$base.txt"
  local raw="$RUN_ROOT/raw/${lang,,}/$base.out"
  local events="$RUN_ROOT/events/${lang,,}/$base.jsonl"
  local log="$RUN_ROOT/validation/${lang,,}/$base.log"
  local snapdir="$RUN_ROOT/snapshots/${lang,,}/$base"
  mkdir -p "$(dirname "$prompt")" "$(dirname "$raw")" "$(dirname "$events")" "$(dirname "$log")" "$snapdir"
  make_prompt "$lang" "$case_id" "$prompt"
  local start_utc end_utc work_ms=0 validation_ms=0 repair_count=0 rollback_attempts=0 rollback_success=NA
  start_utc=$(now_utc)
  local workdir="/tmp/fx3-stage1-${lang,,}-${case_id}-${trial}"
  run_ai "$lang" "$case_id" "$trial" "$prompt" "$raw" "$events" "$workdir"; work_ms=$AI_MS
  local ai_exit=$AI_EXIT
  if [ "$lang" = RUST ]; then validate_rust "$case_id" "$raw" "$log" initial
  else validate_fx3 "$case_id" "$raw" "$log" initial; fi
  local first_parse=$PARSE_PASS first_run=$RUN_PASS first_match=$MATCH final_match=$MATCH
  validation_ms=$VALIDATION_MS; local final_status=$VALIDATION_STATUS final_exit=$VALIDATION_EXIT error_type=NONE final_source="$raw"
  if [ "$final_status" != PASS ]; then
    error_type=$(classify "$log")
    cp "$raw" "$snapdir/repair-0.out"
    local repair_prompt_file="$snapdir/repair-1.txt" repair_out="$snapdir/repair-1.out" repair_events="$RUN_ROOT/events/${lang,,}/$base-repair-1.jsonl" repair_log="$RUN_ROOT/validation/${lang,,}/$base-repair-1.log"
    repair_prompt "$lang" "$case_id" "$prompt" "$raw" "$log" "$repair_prompt_file"
    run_ai "$lang" "$case_id" "$trial" "$repair_prompt_file" "$repair_out" "$repair_events" "$workdir-repair-1"; work_ms=$((work_ms+AI_MS)); repair_count=1
    if [ "$lang" = RUST ]; then validate_rust "$case_id" "$repair_out" "$repair_log" repair-1
    else validate_fx3 "$case_id" "$repair_out" "$repair_log" repair-1; fi
    validation_ms=$((validation_ms+VALIDATION_MS)); final_status=$VALIDATION_STATUS; final_exit=$VALIDATION_EXIT; final_match=$MATCH
    if [ "$final_status" = PASS ]; then final_source="$repair_out"; else
      rollback_attempts=1
      cp "$snapdir/repair-0.out" "$snapdir/restored.out"
      if cmp -s "$snapdir/repair-0.out" "$snapdir/restored.out"; then rollback_success=YES; else rollback_success=NO; fi
      final_source="$raw"
    fi
  fi
  end_utc=$(now_utc)
  local prompt_hash code_hash
  prompt_hash=$(sha256sum "$prompt" | awk '{print $1}')
  code_hash=$(sha256sum "$final_source" | awk '{print $1}')
  local complete=YES
  [ "$ai_exit" -eq 124 ] && complete=NO
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$lang" "$case_id" "$trial" "$MODEL" "$prompt_hash" "$start_utc" "$end_utc" "$work_ms" "$validation_ms" \
    "$first_parse" "$first_run" "$first_match" "$final_match" "$repair_count" "$rollback_attempts" "$rollback_success" "$error_type" "$code_hash" "$final_exit" "$complete" \
    > "$RUN_ROOT/rows/${lang,,}-$base.tsv"
  rm -rf "$workdir" "$workdir-repair-1"
}

if [ "${2:-}" = "one" ]; then
  run_one "$3" "$4" "$5"
else
  pids=()
  for lang in RUST FX3; do
    for case_id in 01 02 03 04 05 06 07 08 09 10 11 12; do
      for trial in 1 2 3; do
        run_one "$lang" "$case_id" "$trial" &
        pids+=("$!")
        if [ "${#pids[@]}" -ge 4 ]; then
          wait "${pids[0]}" || true
          pids=("${pids[@]:1}")
        fi
      done
    done
  done
  for pid in "${pids[@]}"; do wait "$pid" || true; done
fi
