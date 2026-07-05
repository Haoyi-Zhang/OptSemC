#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/scripts${PYTHONPATH:+:$PYTHONPATH}"
RUN_REAL_ENGINE_VALIDATION="${RUN_REAL_ENGINE_VALIDATION:-1}"
OPTSEMC_REQUIRE_FRESH_REAL_ENGINE="${OPTSEMC_REQUIRE_FRESH_REAL_ENGINE:-1}"
export OPTSEMC_REQUIRE_FRESH_REAL_ENGINE
# Remove derived outputs that can be regenerated from grounded rules, feature
# domains, and external motif specifications.  Raw public evidence files are
# never deleted.
rm -f benchmark/generated_probes.jsonl \
      benchmark/sql_bundle/full_probe_bundle.sql \
      benchmark/sql_bundle/full_probe_manifest.csv \
      evaluation/grounded_applicable_rules.jsonl \
      evaluation/grounded_contract_maps.jsonl \
      evaluation/grounded_contract_support.jsonl \
      evaluation/grounded_conflicts.jsonl
rm -rf benchmark/sql_bundle/representative
find evaluation benchmark/sql_bundle -type f -name '*.gz' -delete
./recompute_grounded_mainline.sh
if [[ "$RUN_REAL_ENGINE_VALIDATION" == "1" ]]; then
  PYTHON="${PYTHON:-python}" ./run_cloud_real_engine_validation.sh
else
  echo "Skipping DuckDB/PostgreSQL validation by explicit request; paper-claim gates require OPTSEMC_REQUIRE_FRESH_REAL_ENGINE=1."
fi
if [[ ! -d ../Paper || "${ANONYMOUS_ARTIFACT_ONLY:-0}" == "1" ]]; then
  echo "Paper tree not present; running full artifact-only replay checks."
  ANONYMOUS_ARTIFACT_ONLY=1 RUN_EXPENSIVE_RECOMPUTE=1 ./run_deep_checks.sh
else
  RUN_EXPENSIVE_RECOMPUTE=1 RUN_LATEX_COMPILE=1 ./run_deep_checks.sh
fi
./run_mainline_checks.sh
