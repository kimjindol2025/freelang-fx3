#!/usr/bin/env bash
# Thin wrapper → shared tools/check_poc.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
exec python3 "$ROOT/tools/check_poc.py" "$ROOT/poc/config-lint"
