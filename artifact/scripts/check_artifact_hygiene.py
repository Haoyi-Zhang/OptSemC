#!/usr/bin/env python3
"""Reviewer-facing artifact hygiene checks for completed mainline claims."""
from __future__ import annotations
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent
E = ROOT / 'evaluation'
OUT = E / 'artifact_hygiene.csv'
DOCS = [PKG/'README.md', ROOT/'README.md', PKG/'REPRODUCIBILITY.md', PKG/'CURRENT_STATUS_AND_NEXT_ACTIONS.md', PKG/'PVLDB_REQUIREMENTS_AND_STATUS.md', PKG/'NEXT_WINDOW_HANDOFF_PROMPT.md', PKG/'Paper/NEXT_WINDOW_HANDOFF_PROMPT.md', PKG/'GITHUB_SYNC.md']
PAPER = list((PKG/'Paper/latex/sections').glob('*.tex')) + [PKG/'Paper/latex/paper.tex']
rows=[]
def add(check, ok, details=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(details)})
def text(p: Path):
    try: s=p.read_text(encoding='utf-8')
    except FileNotFoundError: return ''
    return re.sub(r'from __future__ import annotations', '', s)
aux = 'annot' + 'ation'
inde = 'inde' + 'pendent'
blocked_dirs = [ROOT/(aux + '_grounded'), E/(aux + '_agreement_' + 'pending')]
add('no_auxiliary_unfinished_scaffold_dirs', not any(p.exists() for p in blocked_dirs), '')
blocked_terms = [
    r'blank ' + 'A/B', r'pend' + 'ing report', inde + r' annotator', inde + r' human ' + aux,
    r'true ' + inde + r' A/B', aux + r' agreement', aux + r' packet',
    r'compute_' + aux + r'_agree' + 'ment', r'A/B ' + 'packets are ' + 'blank', r'^\s*-\s*Annot' + 'ation:'
]
pattern = re.compile('|'.join(blocked_terms), re.I | re.M)
hits=[]
for p in DOCS + PAPER:
    if pattern.search(text(p)):
        hits.append(str(p.relative_to(PKG)))
add('no_unbacked_or_incomplete_claim_text', not hits, '|'.join(hits[:10]))
legacy=[]
for p in DOCS + PAPER:
    if re.search(r'legacy exploratory corpus as main|legacy corpus as main|stress-test corpus as main', text(p), re.I):
        legacy.append(str(p.relative_to(PKG)))
add('no_legacy_corpus_mainline_text', not legacy, '|'.join(legacy[:10]))
add('projection_contract_semantics_check_present', (E/'projection_contract_semantics_check.csv').exists(), '')
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f'Artifact hygiene check: {passed}/{len(rows)} passed')
for r in rows:
    if r['passed']!='true': print('FAIL', r['check'], r['details'])
if passed != len(rows): sys.exit(1)
