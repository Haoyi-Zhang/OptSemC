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

tex_files = [
    MAIN,
    *sorted((LATEX/'sections').glob('*.tex')),
    *sorted((LATEX/'tables').glob('*.tex')),
    *sorted((LATEX/'figures').glob('*.tex')),
]
tex = '\n'.join(p.read_text(encoding='utf-8') for p in tex_files if p.exists())
bib_text = BIB.read_text(encoding='utf-8')
bib_entries = re.findall(r'@(\w+)\s*\{([^,]+),(.*?)(?=\n@\w+\s*\{|\Z)', bib_text, flags=re.S)
bib_keys = [key.strip() for _, key, _ in bib_entries]

def parse_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for name, value in re.findall(r'^\s*(\w+)\s*=\s*[\{"](.+?)[\}"],?\s*$', body, flags=re.M):
        fields[name.lower()] = re.sub(r'\s+', ' ', value).strip()
    return fields

cited = []
for m in re.findall(r'\\cite[a-zA-Z*]*(?:\[[^\]]*\]){0,2}\{([^}]+)\}', tex):
    cited += [x.strip() for x in m.split(',') if x.strip()]
rows=[]
def add(key, venue, year, has_anchor, cited_ok, matched_bib, passed, details=''):
    rows.append({'key':key,'venue_or_type':venue,'year':year,'has_stable_anchor':str(has_anchor).lower(),'cited':str(cited_ok).lower(),'bibtex_metadata':str(matched_bib).lower(),'passed':str(passed).lower(),'details':details})
for entry_type, key, body in bib_entries:
    fields = parse_fields(body)
    year = fields.get('year', '')
    venue = fields.get('journal') or fields.get('booktitle') or entry_type
    has_anchor = bool(fields.get('doi') or fields.get('url'))
    cited_ok = key in cited
    metadata = bool(fields.get('title') and year and (fields.get('author') or fields.get('organization')))
    reliable = bool(re.fullmatch(r'(19|20)\d{2}', year) and venue and has_anchor and cited_ok and metadata)
    add(key, venue, year, has_anchor, cited_ok, metadata, reliable)
# Global consistency rows as pseudo-entries.
missing_cites = sorted(set(cited) - set(bib_keys))
uncited = sorted(set(bib_keys) - set(cited))
duplicate_keys = sorted(k for k in set(bib_keys) if bib_keys.count(k) > 1)
global_checks = [
    ('__count_70_to_80__', str(len(bib_entries)), 70 <= len(bib_entries) <= 80, ''),
    ('__all_cites_resolve__', str(len(missing_cites)), not missing_cites, '|'.join(missing_cites[:20])),
    ('__no_uncited_bibtex_entries__', str(len(uncited)), not uncited, '|'.join(uncited[:20])),
    ('__no_duplicate_bibtex_keys__', str(len(duplicate_keys)), not duplicate_keys, '|'.join(duplicate_keys)),
    ('__bibtex_entries_parse__', str(len(bib_entries)), bool(bib_entries) and len(bib_entries) == len(bib_keys), ''),
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
