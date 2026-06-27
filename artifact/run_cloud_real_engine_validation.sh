#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/scripts${PYTHONPATH:+:$PYTHONPATH}"

PYTHON_BIN="${PYTHON:-python}"
ENGINES="${OPTSEMC_REAL_ENGINES:-duckdb,postgres}"
POSTGRES_DSN="${OPTSEMC_POSTGRES_DSN:-dbname=optsemc user=root}"

"$PYTHON_BIN" scripts/run_real_engine_validation.py \
  --engines "$ENGINES" \
  --subset motif \
  --postgres-dsn "$POSTGRES_DSN" \
  --out evaluation/real_engine_probe_validation_motif.csv \
  --summary-out evaluation/real_engine_probe_validation_motif_summary.csv

"$PYTHON_BIN" scripts/run_real_engine_validation.py \
  --engines "$ENGINES" \
  --subset full \
  --postgres-dsn "$POSTGRES_DSN" \
  --out evaluation/real_engine_probe_validation_full.csv \
  --summary-out evaluation/real_engine_probe_validation_full_summary.csv

"$PYTHON_BIN" scripts/check_real_engine_validation.py
