#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/scripts${PYTHONPATH:+:$PYTHONPATH}"

PYTHON_BIN="${PYTHON:-python}"
ENGINES="${OPTSEMC_REAL_ENGINES:-duckdb,postgres}"
POSTGRES_DSN="${OPTSEMC_POSTGRES_DSN:-}"
if [[ "$ENGINES" == *postgres* && -z "$POSTGRES_DSN" ]]; then
  echo "OPTSEMC_POSTGRES_DSN must be set for PostgreSQL validation." >&2
  exit 2
fi
POSTGRES_ARGS=()
if [[ -n "$POSTGRES_DSN" ]]; then
  POSTGRES_ARGS=(--postgres-dsn "$POSTGRES_DSN")
fi

"$PYTHON_BIN" scripts/run_real_engine_validation.py \
  --engines "$ENGINES" \
  --subset motif \
  "${POSTGRES_ARGS[@]}" \
  --out evaluation/real_engine_probe_validation_motif.csv \
  --summary-out evaluation/real_engine_probe_validation_motif_summary.csv

"$PYTHON_BIN" scripts/run_real_engine_validation.py \
  --engines "$ENGINES" \
  --subset full \
  "${POSTGRES_ARGS[@]}" \
  --out evaluation/real_engine_probe_validation_full.csv \
  --summary-out evaluation/real_engine_probe_validation_full_summary.csv

"$PYTHON_BIN" scripts/build_environment_report.py
"$PYTHON_BIN" - <<'PY'
import csv
import time
from pathlib import Path

out = Path("evaluation/real_engine_fresh_run.csv")
rows = [
    {"key": "validation_mode", "value": "fresh-engine-rerun"},
    {"key": "engines", "value": "duckdb,postgres"},
    {"key": "subsets", "value": "motif,full"},
    {"key": "unix_time", "value": f"{time.time():.6f}"},
]
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["key", "value"])
    writer.writeheader()
    writer.writerows(rows)
PY
OPTSEMC_REQUIRE_FRESH_REAL_ENGINE=1 "$PYTHON_BIN" scripts/check_real_engine_validation.py
"$PYTHON_BIN" scripts/check_environment_report.py
