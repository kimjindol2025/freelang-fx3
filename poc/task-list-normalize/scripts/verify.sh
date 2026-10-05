#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
exec python3 "$ROOT/tools/check_poc.py" "$ROOT/poc/task-list-normalize"
