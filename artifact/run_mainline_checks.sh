#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/scripts${PYTHONPATH:+:$PYTHONPATH}"
find .. -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name "*.egg-info" \) -prune -exec rm -rf {} +
find .. -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
rm -f ../Paper/latex/optsem_c_main_build* ../Paper/latex/*.aux ../Paper/latex/*.log ../Paper/latex/*.out ../Paper/latex/*.toc ../Paper/latex/*.fls ../Paper/latex/*.fdb_latexmk ../Paper/latex/*.bbl ../Paper/latex/*.blg ../Paper/latex/*.backup
python scripts/check_package_cleanliness.py
python scripts/check_package_manifest.py
python scripts/check_fast_mainline_results.py
find .. -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name "*.egg-info" \) -prune -exec rm -rf {} +
find .. -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
