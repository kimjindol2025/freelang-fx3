#!/usr/bin/env bash
set -u

# Locked benchmark boundary. This script only orchestrates external AI,
# compiler, lowerer, and runtime tools; it does not change task or golden files.
# The prompt and C10 inspection modes do not start model measurements.

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
RUN_ROOT=${1:?usage: run_stage1_locked.sh RUN_ROOT [prompt LANGUAGE CASE|c10|one LANGUAGE CASE TRIAL]}
CLI=/root/.nvm/versions/node/v24.15.0/bin/codex
MODEL=gpt-5.6-luna
AI_LIMIT=120
VALIDATION_LIMIT=30
LINKER=/data/data/com.termux/files/usr/bin/clang
MAINTENANCE_LOG="$RUN_ROOT/tool-maintenance.tsv"
FREEZE_MANIFEST="$ROOT/bench/rust-stage1/freeze-manifest.tsv"

mkdir -p "$RUN_ROOT" "$RUN_ROOT/rows" "$RUN_ROOT/prompts" "$RUN_ROOT/raw" \
  "$RUN_ROOT/events" "$RUN_ROOT/validation" "$RUN_ROOT/snapshots"
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

verify_freeze() {
  [ -s "$FREEZE_MANIFEST" ] || { printf 'FREEZE_FAIL missing %s\n' "$FREEZE_MANIFEST" >&2; return 1; }
  local role path expected actual failures=0
  while IFS=$'\t' read -r role path expected; do
    case "$role" in
      ''|'#'*) continue ;;
      ROLE) continue ;;
    esac
    [ -n "$path" ] && [ -n "$expected" ] || { failures=$((failures+1)); continue; }
    if [ ! -f "$ROOT/$path" ]; then
      printf 'FREEZE_FAIL missing %s\n' "$path" >&2
      failures=$((failures+1))
      continue
    fi
    actual=$(sha256sum "$ROOT/$path" | awk '{print $1}')
    if [ "$actual" != "$expected" ]; then
      printf 'FREEZE_FAIL hash %s expected=%s actual=%s\n' "$path" "$expected" "$actual" >&2
      failures=$((failures+1))
    fi
  done < "$FREEZE_MANIFEST"
  [ "$failures" -eq 0 ]
}

calculate_c10() {
  local out=${1:-"$RUN_ROOT/c10.tsv"}
  local rust_ms=0 fx3_ms=0 rust_rows=0 fx3_rows=0 invalid=0
  local lang ms status evidence
  if [ -s "$MAINTENANCE_LOG" ]; then
    while IFS=$'\t' read -r lang ms status evidence; do
      [ "$lang" = LANGUAGE ] && continue
      case "$lang" in RUST|FX3) ;; *) invalid=1; continue ;; esac
      case "$ms" in ''|*[!0-9]*) invalid=1; continue ;; esac
      if [ "$ms" -gt 0 ] && [ -z "$evidence" ]; then invalid=1; fi
      if [ "$lang" = RUST ]; then rust_ms=$((rust_ms+ms)); rust_rows=$((rust_rows+1)); fi
      if [ "$lang" = FX3 ]; then fx3_ms=$((fx3_ms+ms)); fx3_rows=$((fx3_rows+1)); fi
    done < "$MAINTENANCE_LOG"
  else
    invalid=1
  fi
  {
    printf 'CRITERION\tRUST_MAINTENANCE_MS\tFX3_MAINTENANCE_MS\tDELTA_MS\tTHRESHOLD_MS\tRESULT\tREASON\n'
    if [ "$invalid" -ne 0 ] || [ "$rust_rows" -eq 0 ] || [ "$fx3_rows" -eq 0 ]; then
      printf 'C10\t%s\t%s\t0\t0\t측정 불가\tinvalid-or-missing-maintenance-evidence\n' "$rust_ms" "$fx3_ms"
    elif [ "$rust_ms" -eq 0 ] && [ "$fx3_ms" -eq 0 ]; then
      printf 'C10\t0\t0\t0\t0\t측정 불가\tboth-zero-no-maintenance-denominator\n'
    else
      awk -v rust="$rust_ms" -v fx3="$fx3_ms" 'BEGIN {
        threshold = rust * 0.99
        delta = fx3 - rust
        result = (fx3 <= threshold) ? "PASS" : "FAIL"
        printf "C10\t%d\t%d\t%d\t%.3f\t%s\tpost-freeze-maintenance-comparison\n", rust, fx3, delta, threshold, result
      }'
    fi
  } > "$out"
}

if [ ! -e "$MAINTENANCE_LOG" ]; then
  {
    printf 'LANGUAGE\tMAINTENANCE_MS\tSTATUS\tEVIDENCE\n'
    printf 'RUST\t0\tNO_CHANGE\tNo post-freeze tool change\n'
    printf 'FX3\t0\tNO_CHANGE\tNo post-freeze tool change\n'
  } > "$MAINTENANCE_LOG"
fi

make_prompt() {
  local lang=$1 case_id=$2 out=$3 task
  task="$ROOT/bench/rust-stage1/tasks/case-$case_id.md"
  local task_text input rust_sig fx3_sig
  task_text=$(field TASK_TEXT "$task"); input=$(field INPUT "$task"); rust_sig=$(field RUST_SIGNATURE "$task"); fx3_sig=$(fx3_signature "$case_id")
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
  local prompt=$1 out=$2 events=$3 workdir=$4 start end
  mkdir -p "$workdir"; start=$(now_ms)
  timeout --foreground "${AI_LIMIT}s" "$CLI" exec --ephemeral --ignore-user-config \
    --model "$MODEL" -c model_reasoning_effort=low --skip-git-repo-check \
    --cd "$workdir" --json --output-last-message "$out" - < "$prompt" > "$events" 2>&1
  AI_EXIT=$?; end=$(now_ms); [ -e "$out" ] || : > "$out"; AI_MS=$((end-start))
}

rust_prefix() {
  local case_id=$1 out=$2
  case "$case_id" in
    01) printf '%s\n' 'struct Profile { name: String }' > "$out";; 02|03|04) : > "$out";;
    05) printf '%s\n' 'struct Order { subtotal: i64, tax: i64 }' > "$out";;
    06) printf '%s\n' 'struct Payload { ok: i64, code: String }' > "$out";;
    07) printf '%s\n' 'struct EmailProfile { email: Option<String> }' > "$out";;
    08) printf '%s\n' 'struct Row { code: String }' > "$out";;
    09) printf '%s\n' 'struct ScoredProfile { name: String, score: i64 }' > "$out";;
    10) printf '%s\n' 'struct Side { value: i64 }' > "$out"; printf '%s\n' 'struct Sides { left: Side, right: Side }' >> "$out";;
    11) printf '%s\n' 'struct Metrics { a: i64, b: i64, c: i64 }' > "$out";; 12) : > "$out";;
  esac
}

rust_suffix() {
  local c=$1 o=$2
  case "$c" in
    01) printf '%s\n' 'fn main() { assert_eq!(pick_name(&Profile { name: "Ada".into() }), "Ada"); println!("BENCH_PASS"); }' > "$o";;
    02) printf '%s\n' 'fn main() { assert_eq!(add_points(7, 5), 12); println!("BENCH_PASS"); }' > "$o";;
    03) printf '%s\n' 'fn main() { assert_eq!(status_label(72), "pass"); println!("BENCH_PASS"); }' > "$o";;
    04) printf '%s\n' 'fn main() { assert_eq!(upper_city("seoul"), "SEOUL"); println!("BENCH_PASS"); }' > "$o";;
    05) printf '%s\n' 'fn main() { assert_eq!(order_total(&Order { subtotal: 100, tax: 18 }), 118); println!("BENCH_PASS"); }' > "$o";;
    06) printf '%s\n' 'fn main() { assert_eq!(choose_code(&Payload { ok: 1, code: "A7".into() }), "A7"); println!("BENCH_PASS"); }' > "$o";;
    07) printf '%s\n' 'fn main() { assert_eq!(fallback_email(&EmailProfile { email: None }), "none"); println!("BENCH_PASS"); }' > "$o";;
    08) printf '%s\n' 'fn main() { assert_eq!(indexed_code(&[Row { code: "A1".into() }, Row { code: "B2".into() }]), "B2"); println!("BENCH_PASS"); }' > "$o";;
    09) printf '%s\n' 'fn main() { assert_eq!(profile_band(&ScoredProfile { name: "Mina".into(), score: 81 }), "Mina"); println!("BENCH_PASS"); }' > "$o";;
    10) printf '%s\n' 'fn main() { assert_eq!(side_product(&Sides { left: Side { value: 6 }, right: Side { value: 7 } }), 42); println!("BENCH_PASS"); }' > "$o";;
    11) printf '%s\n' 'fn main() { assert_eq!(score_band(&Metrics { a: 40, b: 35, c: 30 }), "high"); println!("BENCH_PASS"); }' > "$o";;
    12) printf '%s\n' 'fn main() { assert_eq!(matrix_cell(&vec![vec![10, 11], vec![20, 21]], 1), 20); println!("BENCH_PASS"); }' > "$o";;
  esac
}

rust_hidden_suffix() {
  local c=$1 o=$2
  case "$c" in
    01) printf '%s\n' 'fn main() { assert_eq!(pick_name(&Profile { name: "Grace".into() }), "Grace"); println!("HIDDEN_PASS"); }' > "$o";;
    02) printf '%s\n' 'fn main() { assert_eq!(add_points(-4, 9), 5); println!("HIDDEN_PASS"); }' > "$o";;
    03) printf '%s\n' 'fn main() { assert_eq!(status_label(59), "retry"); println!("HIDDEN_PASS"); }' > "$o";;
    04) printf '%s\n' 'fn main() { assert_eq!(upper_city("Busan"), "BUSAN"); println!("HIDDEN_PASS"); }' > "$o";;
    05) printf '%s\n' 'fn main() { assert_eq!(order_total(&Order { subtotal: -3, tax: 8 }), 5); println!("HIDDEN_PASS"); }' > "$o";;
    06) printf '%s\n' 'fn main() { assert_eq!(choose_code(&Payload { ok: 0, code: "Z9".into() }), "rejected"); println!("HIDDEN_PASS"); }' > "$o";;
    07) printf '%s\n' 'fn main() { assert_eq!(fallback_email(&EmailProfile { email: Some("x@y".into()) }), "x@y"); println!("HIDDEN_PASS"); }' > "$o";;
    08) printf '%s\n' 'fn main() { assert_eq!(indexed_code(&[Row { code: "X1".into() }, Row { code: "Y2".into() }]), "Y2"); println!("HIDDEN_PASS"); }' > "$o";;
    09) printf '%s\n' 'fn main() { assert_eq!(profile_band(&ScoredProfile { name: "Mina".into(), score: 69 }), "unrated"); println!("HIDDEN_PASS"); }' > "$o";;
    10) printf '%s\n' 'fn main() { assert_eq!(side_product(&Sides { left: Side { value: -2 }, right: Side { value: 4 } }), -8); println!("HIDDEN_PASS"); }' > "$o";;
    11) printf '%s\n' 'fn main() { assert_eq!(score_band(&Metrics { a: 40, b: 30, c: 29 }), "low"); println!("HIDDEN_PASS"); }' > "$o";;
    12) printf '%s\n' 'fn main() { assert_eq!(matrix_cell(&vec![vec![10, 11], vec![20, 21]], 0), 10); println!("HIDDEN_PASS"); }' > "$o";;
  esac
}

fx3_call() {
  case "$1" in
    01) echo '(println (pick-name {"name" "Ada"}))';; 02) echo '(println (add-points 7 5))';; 03) echo '(println (status-label 72))';; 04) echo '(println (upper-city "seoul"))';;
    05) echo '(println (order-total {"subtotal" 100 "tax" 18}))';; 06) echo '(println (choose-code {"ok" 1 "code" "A7"}))';; 07) echo '(println (fallback-email {}))';; 08) echo '(println (indexed-code [{"code" "A1"} {"code" "B2"}]))';;
    09) echo '(println (profile-band {"name" "Mina" "score" 81}))';; 10) echo '(println (side-product {"left" {"value" 6} "right" {"value" 7}}))';; 11) echo '(println (score-band {"a" 40 "b" 35 "c" 30}))';; 12) echo '(println (matrix-cell [[10 11] [20 21]] 1))';;
  esac
}

fx3_hidden_call() {
  case "$1" in
    01) echo '(println (pick-name {"name" "Grace"}))';; 02) echo '(println (add-points -4 9))';; 03) echo '(println (status-label 59))';; 04) echo '(println (upper-city "Busan"))';;
    05) echo '(println (order-total {"subtotal" -3 "tax" 8}))';; 06) echo '(println (choose-code {"ok" 0 "code" "Z9"}))';; 07) echo '(println (fallback-email {"email" "x@y"}))';; 08) echo '(println (indexed-code [{"code" "X1"} {"code" "Y2"}]))';;
    09) echo '(println (profile-band {"name" "Mina" "score" 69}))';; 10) echo '(println (side-product {"left" {"value" -2} "right" {"value" 4}}))';; 11) echo '(println (score-band {"a" 40 "b" 30 "c" 29}))';; 12) echo '(println (matrix-cell [[10 11] [20 21]] 0))';;
  esac
}

expected() { case "$1" in 01) echo Ada;; 02) echo 12;; 03) echo pass;; 04) echo SEOUL;; 05) echo 118;; 06) echo A7;; 07) echo none;; 08) echo B2;; 09) echo Mina;; 10) echo 42;; 11) echo high;; 12) echo 20;; esac; }
hidden_expected() { case "$1" in 01) echo Grace;; 02) echo 5;; 03) echo retry;; 04) echo BUSAN;; 05) echo 5;; 06) echo rejected;; 07) echo x@y;; 08) echo Y2;; 09) echo unrated;; 10) echo -8;; 11) echo low;; 12) echo 10;; esac; }
classify() { local log=$1; if grep -qi 'timed out\|TIMEOUT' "$log"; then echo TIMEOUT; elif grep -qi 'lower.py\|LowerError\|기대' "$log"; then echo LOWERING; elif grep -qi 'error\|Error\|error:' "$log"; then echo COMPILE; else echo OTHER; fi; }
write_result() { printf 'VISIBLE_PASS=%s\nHIDDEN_PASS=%s\nVISIBLE_EXIT=%s\nHIDDEN_EXIT=%s\nOVERALL_PASS=%s\n' "$VISIBLE_PASS" "$HIDDEN_PASS" "$VISIBLE_EXIT" "$HIDDEN_EXIT" "$OVERALL_PASS" > "$1"; }

validate_rust() {
  local c=$1 source=$2 log=$3 hlog=$4 tag=$5 result=$6
  local w="$RUN_ROOT/validation/rust/case-$c-trial-$TRIAL-$tag.rs"
  # Hidden source must not be "$w.hidden.rs": rustc crate names reject the extra '.' in "*.rs.hidden".
  local hidden_src="$RUN_ROOT/validation/rust/case-$c-trial-$TRIAL-$tag-hidden.rs"
  local b="/tmp/fx3-rust-stage1-$c-$TRIAL-$tag" bh="/tmp/fx3-rust-stage1-$c-$TRIAL-$tag-hidden" start end ce re hce hre
  local p="$RUN_ROOT/validation/rust/case-$c-trial-$TRIAL-$tag.prefix" s="$RUN_ROOT/validation/rust/case-$c-trial-$TRIAL-$tag.suffix" hs="$RUN_ROOT/validation/rust/case-$c-trial-$TRIAL-$tag.hidden-suffix"
  mkdir -p "$(dirname "$w")"; rust_prefix "$c" "$p"; rust_suffix "$c" "$s"; rust_hidden_suffix "$c" "$hs"; cat "$p" "$source" "$s" > "$w"
  start=$(now_ms); rustc -C linker="$LINKER" "$w" -o "$b" > "$log" 2>&1; ce=$?
  if [ "$ce" -eq 0 ]; then timeout --foreground "${VALIDATION_LIMIT}s" "$b" >> "$log" 2>&1; re=$?; else re=$ce; fi
  if [ "$ce" -eq 0 ] && [ "$re" -eq 0 ] && grep -q BENCH_PASS "$log"; then VISIBLE_PASS=YES; else VISIBLE_PASS=NO; fi; VISIBLE_EXIT=$re
  cat "$p" "$source" "$hs" > "$hidden_src"; rustc -C linker="$LINKER" "$hidden_src" -o "$bh" > "$hlog" 2>&1; hce=$?
  if [ "$hce" -eq 0 ]; then timeout --foreground "${VALIDATION_LIMIT}s" "$bh" >> "$hlog" 2>&1; hre=$?; else hre=$hce; fi
  if [ "$hce" -eq 0 ] && [ "$hre" -eq 0 ] && grep -q HIDDEN_PASS "$hlog"; then HIDDEN_PASS=YES; else HIDDEN_PASS=NO; fi; HIDDEN_EXIT=$hre
  end=$(now_ms); VALIDATION_MS=$((end-start)); [ "$ce" -eq 0 ] && PARSE_PASS=YES || PARSE_PASS=NO; [ "$VISIBLE_PASS" = YES ] && MATCH=YES || MATCH=NO; [ "$PARSE_PASS" = YES ] && [ "$VISIBLE_PASS" = YES ] && [ "$HIDDEN_PASS" = YES ] && OVERALL_PASS=YES || OVERALL_PASS=NO; write_result "$result"; VALIDATION_EXIT=$re
  rm -f "$b" "$bh" "$w" "$hidden_src" "$p" "$s" "$hs"
}

validate_fx3() {
  local c=$1 source=$2 log=$3 hlog=$4 tag=$5 result=$6
  local l="$RUN_ROOT/validation/fx3/case-$c-trial-$TRIAL-$tag.fl" w="$RUN_ROOT/validation/fx3/case-$c-trial-$TRIAL-$tag-run.fl" hl="$RUN_ROOT/validation/fx3/case-$c-trial-$TRIAL-$tag-hidden.fl" hw="$RUN_ROOT/validation/fx3/case-$c-trial-$TRIAL-$tag-hidden-run.fl" start end le re hre actual hactual
  mkdir -p "$(dirname "$l")"; : > "$hlog"; start=$(now_ms); python3 "$ROOT/tools/lower.py" "$source" > "$l" 2> "$log"; le=$?
  if [ "$le" -eq 0 ]; then cat "$l" > "$w"; fx3_call "$c" >> "$w"; timeout --foreground "${VALIDATION_LIMIT}s" /root/lang/freelang-v11/bin/fl run "$w" >> "$log" 2>&1; re=$?; actual=$(tail -1 "$log"); [ "$re" -eq 0 ] && [ "$actual" = "$(expected "$c")" ] && VISIBLE_PASS=YES || VISIBLE_PASS=NO; else re=$le; VISIBLE_PASS=NO; fi; VISIBLE_EXIT=$re
  if [ "$le" -eq 0 ]; then
    python3 "$ROOT/tools/lower.py" "$source" > "$hl" 2> "$hlog"; local hle=$?
    if [ "$hle" -eq 0 ]; then
      cat "$hl" > "$hw"; fx3_hidden_call "$c" >> "$hw"
      timeout --foreground "${VALIDATION_LIMIT}s" /root/lang/freelang-v11/bin/fl run "$hw" >> "$hlog" 2>&1; hre=$?
      hactual=$(tail -1 "$hlog"); [ "$hre" -eq 0 ] && [ "$hactual" = "$(hidden_expected "$c")" ] && HIDDEN_PASS=YES || HIDDEN_PASS=NO
    else
      hre=$hle; HIDDEN_PASS=NO
    fi
  else
    # Always leave a hidden log so row_complete can see evidence when visible lowering fails.
    printf 'HIDDEN_SKIPPED visible lowering failed with exit %s\n' "$le" > "$hlog"
    hre=$le; HIDDEN_PASS=NO
  fi
  HIDDEN_EXIT=$hre
  end=$(now_ms); VALIDATION_MS=$((end-start)); [ "$le" -eq 0 ] && PARSE_PASS=YES || PARSE_PASS=NO; [ "$VISIBLE_PASS" = YES ] && MATCH=YES || MATCH=NO; [ "$PARSE_PASS" = YES ] && [ "$VISIBLE_PASS" = YES ] && [ "$HIDDEN_PASS" = YES ] && OVERALL_PASS=YES || OVERALL_PASS=NO; write_result "$result"; VALIDATION_EXIT=$re; rm -f "$l" "$w" "$hl" "$hw"
}

repair_prompt() { local initial=$1 source=$2 log=$3 hlog=$4 out=$5; cat "$initial" > "$out"; printf '\nThe current attempt failed validation. Repair only this trial. Return only the complete corrected source code. Do not add a main function.\nCURRENT_SOURCE:\n' >> "$out"; cat "$source" >> "$out"; printf '\nVISIBLE_VALIDATION_LOG:\n' >> "$out"; cat "$log" >> "$out"; }

row_complete() {
  local lang=$1 base=$2 repairs=$3 n
  [ -e "$RUN_ROOT/prompts/${lang,,}/$base.txt" ] && [ -e "$RUN_ROOT/raw/${lang,,}/$base.out" ] && [ -s "$RUN_ROOT/events/${lang,,}/$base.jsonl" ] || return 1
  [ -e "$RUN_ROOT/validation/${lang,,}/$base.log" ] && [ -e "$RUN_ROOT/validation/${lang,,}/$base-hidden.log" ] || return 1
  for n in $(seq 1 "$repairs"); do [ -e "$RUN_ROOT/snapshots/${lang,,}/$base/repair-$n.txt" ] && [ -e "$RUN_ROOT/snapshots/${lang,,}/$base/repair-$n.out" ] && [ -s "$RUN_ROOT/events/${lang,,}/$base-repair-$n.jsonl" ] && [ -e "$RUN_ROOT/validation/${lang,,}/$base-repair-$n.log" ] && [ -e "$RUN_ROOT/validation/${lang,,}/$base-repair-$n-hidden.log" ] || return 1; done
  return 0
}

run_one() {
  local lang=$1 c=$2 trial=$3; TRIAL=$trial; local base="case-$c-trial-$trial"
  [ -e "$RUN_ROOT/rows/${lang,,}-$base.tsv" ] && return 0
  local prompt="$RUN_ROOT/prompts/${lang,,}/$base.txt" raw="$RUN_ROOT/raw/${lang,,}/$base.out" events="$RUN_ROOT/events/${lang,,}/$base.jsonl" log="$RUN_ROOT/validation/${lang,,}/$base.log" hlog="$RUN_ROOT/validation/${lang,,}/$base-hidden.log" snap="$RUN_ROOT/snapshots/${lang,,}/$base" workdir="/tmp/fx3-stage1-${lang,,}-${c}-${trial}"
  mkdir -p "$(dirname "$prompt")" "$(dirname "$raw")" "$(dirname "$events")" "$(dirname "$log")" "$snap"; make_prompt "$lang" "$c" "$prompt"; local start_utc=$(now_utc) work_ms=0 validation_ms=0 repairs=0 rolls=0 ry=0 iy=0 rec=0 recc=0 current_source="$raw" current_log="$log" current_hlog="$hlog" current_result="$snap/initial.result" final_source="$raw" error_type=NONE
  run_ai "$prompt" "$raw" "$events" "$workdir"; work_ms=$AI_MS; local ai_exit=$AI_EXIT
  if [ "$lang" = RUST ]; then validate_rust "$c" "$raw" "$log" "$hlog" initial "$current_result"; else validate_fx3 "$c" "$raw" "$log" "$hlog" initial "$current_result"; fi
  validation_ms=$VALIDATION_MS
  local first_parse=$PARSE_PASS first_run=$VISIBLE_PASS first_match=$MATCH first_hidden=$HIDDEN_PASS final_match=$MATCH final_hidden=$HIDDEN_PASS final_exit=$VALIDATION_EXIT previous_error=NONE
  [ "$OVERALL_PASS" = YES ] || error_type=$(classify "$log"); previous_error=$error_type
  while [ "$OVERALL_PASS" != YES ] && [ "$repairs" -lt 2 ]; do
    local n=$((repairs+1))
    local before="$snap/repair-$n-before.out" before_result="$snap/repair-$n-before.result" rp="$snap/repair-$n.txt" ro="$snap/repair-$n.out" ev="$RUN_ROOT/events/${lang,,}/$base-repair-$n.jsonl" rl="$RUN_ROOT/validation/${lang,,}/$base-repair-$n.log" rh="$RUN_ROOT/validation/${lang,,}/$base-repair-$n-hidden.log" rr="$snap/repair-$n.result"
    cp "$current_source" "$before"; cp "$current_result" "$before_result"; printf 'ROUND\tBEFORE_SOURCE_SHA256\tBEFORE_RESULT_SHA256\n' > "$snap/repair-$n-rollback.tsv"; local bs=$(sha256sum "$before" | awk '{print $1}') brs=$(sha256sum "$before_result" | awk '{print $1}'); printf '%s\t%s\t%s\n' "$n" "$bs" "$brs" >> "$snap/repair-$n-rollback.tsv"; repair_prompt "$prompt" "$current_source" "$current_log" "$current_hlog" "$rp"; run_ai "$rp" "$ro" "$ev" "$workdir-repair-$n"; work_ms=$((work_ms+AI_MS)); repairs=$n; if [ "$lang" = RUST ]; then validate_rust "$c" "$ro" "$rl" "$rh" "repair-$n" "$rr"; else validate_fx3 "$c" "$ro" "$rl" "$rh" "repair-$n" "$rr"; fi; validation_ms=$((validation_ms+VALIDATION_MS)); final_match=$MATCH; final_hidden=$HIDDEN_PASS; final_exit=$VALIDATION_EXIT; local repair_error=NONE; [ "$OVERALL_PASS" = YES ] || repair_error=$(classify "$rl"); recc=$((recc+1)); [ "$repair_error" = "$previous_error" ] && [ "$repair_error" != NONE ] && rec=$((rec+1)); previous_error=$repair_error
    if [ "$OVERALL_PASS" = YES ]; then final_source="$ro"; current_source="$ro"; current_log="$rl"; current_hlog="$rh"; current_result="$rr"; error_type=NONE; break; fi
    local restored="$snap/repair-$n-restored.out" restored_result="$snap/repair-$n-restored.result" rlog="$RUN_ROOT/validation/${lang,,}/$base-repair-$n-rollback.log" rhlog="$RUN_ROOT/validation/${lang,,}/$base-repair-$n-rollback-hidden.log"; cp "$before" "$restored"; cp "$before_result" "$restored_result"; if [ "$lang" = RUST ]; then validate_rust "$c" "$restored" "$rlog" "$rhlog" "repair-$n-rollback" "$restored_result"; else validate_fx3 "$c" "$restored" "$rlog" "$rhlog" "repair-$n-rollback" "$restored_result"; fi; validation_ms=$((validation_ms+VALIDATION_MS)); local as=$(sha256sum "$restored" | awk '{print $1}') ars=$(sha256sum "$restored_result" | awk '{print $1}') bytes=NO result=NO; cmp -s "$before" "$restored" && bytes=YES; cmp -s "$before_result" "$restored_result" && result=YES; printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$bs" "$as" "$brs" "$ars" "$bytes" "$result" >> "$snap/repair-$n-rollback.tsv"; rolls=$n; [ "$bytes" = YES ] && [ "$result" = YES ] && [ "$OVERALL_PASS" = NO ] && ry=$((ry+1)) && iy=$((iy+1)); current_source="$before"; current_log="$log"; current_hlog="$hlog"; current_result="$before_result"; final_source="$before"; final_match=$(sed -n 's/^VISIBLE_PASS=//p' "$before_result"); final_hidden=$(sed -n 's/^HIDDEN_PASS=//p' "$before_result"); error_type=$previous_error
  done
  local rollback_status=NA integrity_status=NA recurrence_status=NA; [ "$rolls" -gt 0 ] && rollback_status=NO && integrity_status=NO && [ "$ry" -eq "$rolls" ] && rollback_status=YES && [ "$iy" -eq "$rolls" ] && integrity_status=YES; [ "$repairs" -gt 0 ] && recurrence_status=NO && [ "$rec" -gt 0 ] && recurrence_status=YES
  local end_utc=$(now_utc) ph=$(sha256sum "$prompt" | awk '{print $1}') ch=$(sha256sum "$final_source" | awk '{print $1}') maintenance=$(awk -F '\t' -v l="$lang" '$1==l {print $2}' "$MAINTENANCE_LOG") complete=NO; row_complete "$lang" "$base" "$repairs" && complete=YES
  # 25 fields: keep format count aligned with args (complete is last).
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$lang" "$c" "$trial" "$MODEL" "$ph" "$start_utc" "$end_utc" "$work_ms" "$validation_ms" "$first_parse" "$first_run" "$first_match" "$final_match" "$first_hidden" "$final_hidden" "$repairs" "$rolls" "$rollback_status" "$integrity_status" "$recurrence_status" "$maintenance" "$error_type" "$ch" "$final_exit" "$complete" > "$RUN_ROOT/rows/${lang,,}-$base.tsv"
  rm -rf "$workdir" "$workdir-repair-1" "$workdir-repair-2"
}

if ! verify_freeze; then
  exit 2
fi

if [ "${2:-}" = prompt ]; then
  [ "$#" -eq 4 ] || { printf 'usage: run_stage1_locked.sh RUN_ROOT prompt LANGUAGE CASE\n' >&2; exit 2; }
  make_prompt "$3" "$4" /dev/stdout
elif [ "${2:-}" = prompts ]; then
  for lang in RUST FX3; do
    for c in 01 02 03 04 05 06 07 08 09 10 11 12; do
      out="$RUN_ROOT/prompts/${lang,,}/case-$c.txt"
      mkdir -p "$(dirname "$out")"
      make_prompt "$lang" "$c" "$out"
    done
  done
elif [ "${2:-}" = c10 ]; then
  calculate_c10
  cat "$RUN_ROOT/c10.tsv"
elif [ "${2:-}" = one ]; then
  run_one "$3" "$4" "$5"
else
  pids=(); for lang in RUST FX3; do for c in 01 02 03 04 05 06 07 08 09 10 11 12; do for trial in 1 2 3; do run_one "$lang" "$c" "$trial" & pids+=("$!"); if [ "${#pids[@]}" -ge 4 ]; then wait "${pids[0]}" || true; pids=("${pids[@]:1}"); fi; done; done; done; for pid in "${pids[@]}"; do wait "$pid" || true; done
fi
