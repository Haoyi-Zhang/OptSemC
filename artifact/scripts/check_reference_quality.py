#!/usr/bin/env python3
"""Check bibliography count, anchors, and citation consistency."""
from __future__ import annotations
import csv
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
LATEX = ROOT / 'Paper' / 'latex'
BIB = LATEX / 'refs.bib'
MAIN = LATEX / 'paper.tex'
OUT = ROOT / 'artifact' / 'evaluation' / 'reference_quality.csv'
ADJUDICATION = ROOT / 'artifact' / 'evaluation' / 'reference_primary_adjudication.csv'
GUARD = ROOT / 'artifact' / 'evaluation' / 'reference_guard_audit_latest.json'

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

def load_adjudication() -> dict[str, dict[str, str]]:
    if not ADJUDICATION.exists():
        return {}
    with ADJUDICATION.open(newline='', encoding='utf-8') as f:
        return {
            row.get('key', '').strip(): row
            for row in csv.DictReader(f)
            if row.get('key', '').strip()
        }

def guard_key(entry: dict) -> str:
    ref = entry.get('reference') or {}
    return str(ref.get('key') or '').strip()

adjudication = load_adjudication()
adjudication_keys = set(adjudication)
bib_key_set = set(bib_keys)
extra_adjudication = sorted(adjudication_keys - bib_key_set)
missing_adjudication = sorted(bib_key_set - adjudication_keys)
add('__adjudication_keys_match_bibtex__', 'global', len(adjudication_keys),
    True, True, True, not extra_adjudication and not missing_adjudication,
    f"extra={extra_adjudication[:10]};missing={missing_adjudication[:10]}")

if GUARD.exists():
    guard_entries = json.loads(GUARD.read_text(encoding='utf-8'))
    guard_keys = [guard_key(entry) for entry in guard_entries]
    guard_key_set = {key for key in guard_keys if key}
    extra_guard = sorted(guard_key_set - bib_key_set)
    missing_guard = sorted(bib_key_set - guard_key_set)
    add('__guard_keys_match_bibtex__', 'global', len(guard_key_set),
        True, True, True, not extra_guard and not missing_guard,
        f"extra={extra_guard[:10]};missing={missing_guard[:10]}")
    guard_counts: dict[str, int] = {}
    open_guard = []
    for entry in guard_entries:
        key = guard_key(entry)
        status = str(entry.get('status') or '').upper()
        guard_counts[status] = guard_counts.get(status, 0) + 1
        adj = adjudication.get(key, {})
        adj_status = str(adj.get('status') or '').upper()
        primary_source = bool(adj.get('source') and adj.get('identifier'))
        reason = adj.get('note', '')
        source_text = adj.get('source', '')
        source_and_reason = f'{source_text} {reason}'.lower()
        source_reason = (
            'exact_doi_record' in reason
            or 'http=' in reason
            or 'arxiv_url' in reason
            or 'official page' in source_and_reason
            or 'official pdf' in source_and_reason
            or 'project page' in source_and_reason
        )
        closed = (
            status == 'PASS'
            or (
                adj_status in {'PASS', 'ADJUDICATED_PASS'}
                and primary_source
                and source_reason
            )
        )
        if not closed:
            open_guard.append(key)
        add(f'guard_adjudicated:{key}', adj.get('source', 'guard'), status,
            primary_source, key in cited, key in bib_key_set, closed,
            f"guard={status};adjudication={adj_status};identifier={adj.get('identifier','')};note={reason[:160]}")
    add('__guard_review_fail_closed_by_primary_sources__', 'global',
        ';'.join(f'{k}={v}' for k, v in sorted(guard_counts.items())),
        True, True, True, not open_guard, '|'.join(open_guard[:20]))
else:
    add('__reference_guard_json_present__', 'global', 'missing',
        True, True, True, False, str(GUARD.relative_to(ROOT)))

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['key','venue_or_type','year','has_stable_anchor','cited','bibtex_metadata','passed','details'])
    w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Reference quality: {len(rows)-len(failed)}/{len(rows)} checks passed')
if failed:
    for r in failed[:20]: print('FAIL', r)
    sys.exit(1)
