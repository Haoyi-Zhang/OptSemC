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
import hashlib
import time
from pathlib import Path

root = Path(".")
evidence_files = [
    root / "benchmark" / "generated_probes.jsonl",
    root / "evaluation" / "sql_probe_execution.csv",
    root / "evaluation" / "sql_probe_execution_summary.csv",
    root / "evaluation" / "sql_probe_execution_check.csv",
    root / "evaluation" / "sql_probe_multicatalog_summary.csv",
    root / "evaluation" / "sql_probe_multicatalog_totals.csv",
    root / "evaluation" / "sql_probe_multicatalog_check.csv",
    root / "evaluation" / "real_engine_probe_validation_full.csv",
    root / "evaluation" / "real_engine_probe_validation_full_summary.csv",
    root / "evaluation" / "real_engine_probe_validation_motif.csv",
    root / "evaluation" / "real_engine_probe_validation_motif_summary.csv",
]

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

bundle = hashlib.sha256()
for path in sorted(evidence_files, key=lambda p: p.as_posix()):
    bundle.update(path.as_posix().encode("utf-8"))
    bundle.update(b"\0")
    bundle.update(sha256_file(path).encode("ascii"))
    bundle.update(b"\n")

out = Path("evaluation/real_engine_fresh_run.csv")
rows = [
    {"key": "validation_mode", "value": "fresh-engine-rerun"},
    {"key": "engines", "value": "duckdb,postgres"},
    {"key": "subsets", "value": "motif,full"},
    {"key": "evidence_bundle_sha256", "value": bundle.hexdigest()},
    {"key": "unix_time", "value": f"{time.time():.6f}"},
]
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["key", "value"])
    writer.writeheader()
    writer.writerows(rows)
PY
OPTSEMC_REQUIRE_FRESH_REAL_ENGINE=1 "$PYTHON_BIN" scripts/check_real_engine_validation.py
"$PYTHON_BIN" scripts/check_environment_report.py
