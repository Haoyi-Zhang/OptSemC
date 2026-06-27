#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
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
find . -type f -name '*.gz' -delete
./recompute_grounded_mainline.sh
RUN_EXPENSIVE_RECOMPUTE=1 RUN_LATEX_COMPILE=1 ./run_deep_checks.sh
./run_mainline_checks.sh
