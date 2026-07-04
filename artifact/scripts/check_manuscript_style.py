#!/usr/bin/env python3
"""Check the manuscript reads as a research paper rather than a repository report."""
from __future__ import annotations
import csv
import re
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / 'Paper' / 'latex'
PDF = PAPER / 'paper.pdf'
OUT = ROOT / 'artifact' / 'evaluation' / 'manuscript_style.csv'
text = (PAPER/'paper.tex').read_text(encoding='utf-8')
for folder in ['sections', 'tables', 'figures']:
    for p in sorted((PAPER/folder).glob('*.tex')):
        text += '\n' + p.read_text(encoding='utf-8')
rows=[]
def add(check, passed, details=''):
    rows.append({'check':check,'passed':str(bool(passed)).lower(),'details':str(details)})
# Remove template metadata and LaTeX command arguments before visible-prose checks.
style_text = re.sub(r'\\newcommand\\vldb[a-zA-Z]+\{[^}]*\}', ' ', text)
style_text = re.sub(r'\\begingroup\\small\\noindent\\raggedright\\textbf\{PVLDB Reference Format:.*?\\input\{sections/01_intro\}', r'\\input{sections/01_intro}', style_text, flags=re.S)
visible = re.sub(r'\\(input|label|ref|cite|Description)\{[^}]*\}', ' ', style_text)
visible = re.sub(r'\\[A-Za-z]+', ' ', visible)
blocked = [
    r'\bartifact\b', r'\breader\b', r'\brepository\b', r'\bGitHub\b', r'\bscript\b',
    r'\bfunction name\b', r'\bfolder\b', r'\.csv', r'\.json', r'\.py',
    r'\bSQL bundle\b', r'\bbundle\b', r'\bgate\b', r'\bsnapshot\b',
]
hits=[pat for pat in blocked if re.search(pat, visible, re.I)]
add('no_visible_repository_or_report_terms', not hits, ';'.join(hits))
# Structure checks.
sections = re.findall(r'\\section\{([^}]*)\}', text)
expected = ['Introduction','Precision Loss in Optimizer Comparisons','Contract Formalization and Notation','Benchmark and Grounded Corpus','Evaluation']
add('has_regular_research_structure', sections[:5] == expected, '|'.join(sections[:7]))
add('has_tikz_mechanism_figure', '\\begin{tikzpicture}' in text and 'Projection kernel' in text, '')
theorem_count = text.count('\\begin{theorem}')
lemma_count = text.count('\\begin{lemma}')
proposition_count = text.count('\\begin{proposition}')
observation_count = text.count('\\begin{observation}')
proof_count = text.count('\\begin{proof}')
formal_count = theorem_count + lemma_count + proposition_count + observation_count
details = f"formal={formal_count};theorems={theorem_count};lemmas={lemma_count};propositions={proposition_count};observations={observation_count};proofs={proof_count}"
add('has_formal_statements_and_proofs', formal_count >= 6 and proof_count >= 5, details)
refs_bib = PAPER / 'refs.bib'
reference_count = len(re.findall(r'^@\w+\s*\{', refs_bib.read_text(encoding='utf-8'), flags=re.M)) if refs_bib.exists() else len(re.findall(r'\\bibitem\{', text))
add('references_70_to_80', 70 <= reference_count <= 80, reference_count)
# Basic PDF text check.
try:
    proc = subprocess.run(['pdftotext', str(PDF), '-'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    pdftext = proc.stdout
    body_pdftext = re.sub(r'PVLDB Reference Format:.*?1 INTRODUCTION', '1 INTRODUCTION', pdftext, flags=re.S|re.I)
    add('pdf_has_no_unresolved_references', '??' not in pdftext, 'contains ??' if '??' in pdftext else '')
    add('pdf_does_not_expose_source_paths', not re.search(r'Paper/|artifact/|\.tex|\.csv|\.py|jsonl', body_pdftext, re.I), '')
except Exception as exc:
    add('pdf_text_style_extractable', False, type(exc).__name__)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Manuscript style: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows):
    raise SystemExit(1)
