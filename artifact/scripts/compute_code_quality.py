#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.quality import analyze_tree, quality_summary, import_graph_rows
from optsemc.io import write_csv
rows=analyze_tree(ROOT)
write_csv(ART/'evaluation'/'python_code_quality.csv', [r.as_row() for r in rows], ['path','functions','classes','imports','max_function_lines','syntax_ok'])
write_csv(ART/'evaluation'/'python_code_quality_summary.csv', quality_summary(rows), ['metric','value'])
write_csv(ART/'evaluation'/'python_import_graph.csv', import_graph_rows(ROOT), ['source','target','kind'])
print(f'Code quality: files={len(rows)}')
