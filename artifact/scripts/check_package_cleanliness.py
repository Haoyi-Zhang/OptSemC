#!/usr/bin/env python3
"""Check package-facing tree for stale labels, transients, and manuscript leakage.

The checker streams large text outputs instead of reading JSONL/CSV artifacts into
memory.  This keeps the public hygiene gate stable even when generated relation
files are tens of megabytes.
"""
from __future__ import annotations
import csv
import re
import shutil
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from optsemc.streaming import contains_pattern, iter_text_files, transient_paths
OUT = ROOT / 'evaluation' / 'package_cleanliness.csv'
# The checker imports the package it audits; remove any bytecode caches that
# the interpreter may have produced before scanning for package transients.
for cache in PKG.rglob('__pycache__'):
    shutil.rmtree(cache, ignore_errors=True)
for cache in PKG.rglob('*.egg-info'):
    if cache.is_dir():
        shutil.rmtree(cache, ignore_errors=True)
for pyc in PKG.rglob('*.py[co]'):
    try:
        pyc.unlink()
    except OSError:
        pass
ROWS: list[dict[str,str]] = []

def add(check: str, passed: bool, details: str = '') -> None:
    ROWS.append({'check': check, 'passed': str(bool(passed)).lower(), 'details': details})

transient = transient_paths(PKG, suffixes=(
    '.pyc', '.pyo', '.aux', '.log', '.out', '.toc', '.fls', '.fdb_latexmk', '.synctex.gz', '.backup', '.egg-info',
), names={'__pycache__', '.DS_Store', '.pytest_cache'})
add('no_transient_or_build_byproducts', not transient, '|'.join(transient[:20]))

version_hits = []
current_version_text = (ROOT / 'VERSION').read_text(encoding='utf-8').strip() if (ROOT / 'VERSION').exists() else 'OptSemC'
try:
    current_version_number = int(current_version_text.lstrip('v'))
except ValueError:
    current_version_number = 50
stale_labels = [f'v{i}' for i in range(40, current_version_number)]
version_re = re.compile('(' + '|'.join(re.escape(label) for label in stale_labels) + ')') if stale_labels else re.compile(r'$.')
for p in iter_text_files(ROOT):
    rel = p.relative_to(PKG).as_posix()
    if version_re.search(rel) or contains_pattern(p, version_re):
        version_hits.append(rel)
add('no_stale_package_version_labels', not version_hits, '|'.join(version_hits[:30]))

allowed_root_files = {'.gitattributes', '.gitignore', 'README.md'}
root_files = sorted(p.name for p in PKG.iterdir() if p.is_file())
unexpected_root_files = [name for name in root_files if name not in allowed_root_files]
add('clean_project_top_level_files', not unexpected_root_files, ','.join(unexpected_root_files))

paper_files = [
    PKG/'Paper'/'latex'/'paper.tex',
    *sorted((PKG/'Paper'/'latex'/'sections').glob('*.tex')),
    *sorted((PKG/'Paper'/'latex'/'tables').glob('*.tex')),
]
paper_text = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in paper_files if p.exists())
# Ignore required PVLDB metadata blocks when checking whether the research body reads like a paper.
paper_text = re.sub(r'\\newcommand\\vldb[a-zA-Z]+\{[^}]*\}', ' ', paper_text)
paper_text = re.sub(r'\\begingroup\\small\\noindent\\raggedright\\textbf\{PVLDB Reference Format:.*?\\input\{sections/01_intro\}', r'\\input{sections/01_intro}', paper_text, flags=re.S)
leak_terms = [
    r'\bartifact\b', r'\breader\b', r'\brepository\b', r'\bscript\b', r'\bfunction name\b',
    r'\bfolder\b', r'\.csv', r'\.json', r'\.py', r'run_mainline', r'\bSQL bundle\b', r'\bbundle\b',
]
leaks = [pat for pat in leak_terms if re.search(pat, paper_text, re.I)]
add('paper_body_avoids_engineering_package_terms', not leaks, ';'.join(leaks))
visible_report_text = re.sub(r'\\(input|label|ref|cite|Description)\{[^}]*\}', ' ', paper_text)
report_like = re.findall(r'\b(passed|gate|snapshot|hardening report|completion report)\b', visible_report_text, flags=re.I)
add('paper_body_not_written_as_artifact_report', not report_like, '|'.join(report_like[:20]))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=['check','passed','details'])
    writer.writeheader(); writer.writerows(ROWS)
passed = sum(r['passed']=='true' for r in ROWS)
print(f'Package cleanliness: {passed}/{len(ROWS)} passed')
for r in ROWS:
    if r['passed'] != 'true':
        print('FAIL', r['check'], r['details'])
if passed != len(ROWS):
    raise SystemExit(1)
