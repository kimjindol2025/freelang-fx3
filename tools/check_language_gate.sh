#!/usr/bin/env bash
# FX3 언어 회귀 게이트 (주기2). Core 삭감·런타임 없음.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

run() {
  echo "[lang-gate] $*"
  "$@"
}

run python3 tools/lower.py --check
run python3 tools/check_delimiter.py
run python3 tools/check_semi_display.py
run python3 tools/check_whitespace_same_fl.py
run python3 tools/check_semantic_min.py
run python3 tools/check_roadmap6_exec.py
run python3 tools/check_corpus.py

echo "LANG_GATE_SCOPE=fixture_01_04+stdlib(+corpus checks)"
echo "LANG_GATE_CORE_CUT=NO"
echo "LANG_GATE_NATIVE=SKIPPED_USE_check_semantic_native"
echo "LANG_GATE=PASS"
exit 0
