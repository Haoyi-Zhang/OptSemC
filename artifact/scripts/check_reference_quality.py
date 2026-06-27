#!/usr/bin/env python3
"""Check bibliography count, anchors, and citation consistency."""
from __future__ import annotations
import csv
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
LATEX = ROOT / 'Paper' / 'latex'
BIB = LATEX / 'refs.bib'
MAIN = LATEX / 'paper.tex'
OUT = ROOT / 'artifact' / 'evaluation' / 'reference_quality.csv'
tex = MAIN.read_text(encoding='utf-8') + '\n'.join(p.read_text(encoding='utf-8') for p in sorted((LATEX/'sections').glob('*.tex')))
# BibTeX entries retained as stable metadata.
bib_text = BIB.read_text(encoding='utf-8')
bib_entries = re.findall(r'@\w+\s*\{([^,]+),(.*?)(?=\n@\w+\s*\{|\Z)', bib_text, flags=re.S)
bib_keys = [k.strip() for k,_ in bib_entries]
manual = re.findall(r'\\bibitem\{([^}]+)\}\s*(.*?)(?=\n\\bibitem\{|\n\\end\{thebibliography\})', MAIN.read_text(encoding='utf-8'), flags=re.S)
manual_keys = [k.strip() for k,_ in manual]
cited = []
for m in re.findall(r'\\cite\{([^}]+)\}', tex):
    cited += [x.strip() for x in m.split(',') if x.strip()]
rows=[]
def add(key, venue, year, has_anchor, cited_ok, matched_bib, passed, details=''):
    rows.append({'key':key,'venue_or_type':venue,'year':year,'has_stable_anchor':str(has_anchor).lower(),'cited':str(cited_ok).lower(),'bibtex_metadata':str(matched_bib).lower(),'passed':str(passed).lower(),'details':details})
for key, body in manual:
    year = re.search(r'\b(19|20)\d{2}\b', body)
    venue = ''
    em = re.search(r'\\emph\{([^}]+)\}', body)
    if em: venue = em.group(1)
    has_anchor = bool(re.search(r'DOI:|URL:', body))
    cited_ok = key in cited
    matched = key in bib_keys
    reliable = bool(year and venue and has_anchor and cited_ok and matched)
    add(key, venue, year.group(0) if year else '', has_anchor, cited_ok, matched, reliable)
# Global consistency rows as pseudo-entries.
missing_cites = sorted(set(cited) - set(manual_keys))
uncited = sorted(set(manual_keys) - set(cited))
duplicate_keys = sorted(k for k in set(manual_keys) if manual_keys.count(k) > 1)
global_checks = [
    ('__count_70_to_80__', str(len(manual)), 70 <= len(manual) <= 80, ''),
    ('__all_cites_resolve__', str(len(missing_cites)), not missing_cites, '|'.join(missing_cites[:20])),
    ('__no_duplicate_bibitems__', str(len(duplicate_keys)), not duplicate_keys, '|'.join(duplicate_keys)),
    ('__bibtex_matches_manual__', f'{len(set(bib_keys) & set(manual_keys))}/{len(manual_keys)}', set(bib_keys) == set(manual_keys), ''),
]
for key,value,ok,details in global_checks:
    add(key, 'global', value, True, True, True, ok, details)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['key','venue_or_type','year','has_stable_anchor','cited','bibtex_metadata','passed','details'])
    w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Reference quality: {len(rows)-len(failed)}/{len(rows)} checks passed')
if failed:
    for r in failed[:20]: print('FAIL', r)
    sys.exit(1)
