#!/usr/bin/env python3
"""Check that every grounded segment has a public, source-level locator.

The public artifact must not rely on internal browser/tool references alone.
Every verified segment must carry an HTTPS URL, source title, retrieval date,
line range, public locator, and SHA-256 segment hash.
"""
from __future__ import annotations
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'grounded'
E = ROOT / 'evaluation'
E.mkdir(exist_ok=True)

url_re = re.compile(r'^https?://')
line_re = re.compile(r'^L\d+(?:-L\d+)?$')
hash_re = re.compile(r'^[0-9a-f]{64}$')

issues = []
count = 0
public_locator_count = 0
turn_only = 0
for line in (G/'verified_segments.jsonl').read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    count += 1
    s = json.loads(line)
    sid = s.get('segment_id','')
    if not url_re.match(s.get('source_url','')):
        issues.append((sid,'missing_public_source_url',s.get('source_url','')))
    if not s.get('source_title'):
        issues.append((sid,'missing_source_title',''))
    if not s.get('source_retrieved_at'):
        issues.append((sid,'missing_source_retrieved_at',''))
    if not line_re.match(s.get('line_range','')):
        issues.append((sid,'invalid_line_range',s.get('line_range','')))
    h = s.get('segment_hash') or s.get('segment_sha256') or ''
    if not hash_re.match(h):
        issues.append((sid,'invalid_segment_hash',h))
    locator = s.get('public_locator','')
    if url_re.match(locator.split('::',1)[0]) and '::L' in locator:
        public_locator_count += 1
    else:
        issues.append((sid,'invalid_public_locator',locator))
    if 'web_ref' in s or re.search(r'\bturn\d+', json.dumps(s)):
        issues.append((sid,'internal_construction_reference_present','web_ref_or_turn_ref'))


# The package artifact should not expose construction-time web-tool references
# (for example, turn-id browser refs) in public grounded records.
internal_ref_issues = []
for rel in [
    'grounded/verified_rules.jsonl',
    'grounded/verified_segments.jsonl',
]:
    path = ROOT / rel
    if not path.exists():
        continue
    for i, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        if re.search(r'\bturn\d+', raw) or '"web_ref"' in raw:
            internal_ref_issues.append((rel, str(i), 'internal_construction_reference_present'))
if internal_ref_issues:
    for rel, line_no, typ in internal_ref_issues[:20]:
        issues.append((f'{rel}:{line_no}', typ, 'remove web-tool construction reference from package artifact'))

with (E/'public_provenance_check.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['segment_id','issue_type','detail'])
    w.writerows(issues)
with (E/'public_provenance_summary.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['metric','value'])
    w.writerow(['verified_segments',count])
    w.writerow(['segments_with_public_locator',public_locator_count])
    w.writerow(['internal_construction_refs', sum(1 for _,t,_ in issues if t == 'internal_construction_reference_present')])
    w.writerow(['public_provenance_issues',len(issues)])
print(f'Public provenance: {public_locator_count}/{count} segments with public locators; issues={len(issues)}')
if issues:
    for row in issues[:20]:
        print(row)
    sys.exit(1)
