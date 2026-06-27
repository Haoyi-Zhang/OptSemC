#!/usr/bin/env python3
"""Attach stable public-source locators to verified evidence segments.

Earlier internal audit metadata kept web-tool refs in segment records.  Those
refs are useful during construction but are not public artifact locators.  This
script makes the public locator explicit by copying source URL/title/retrieval
metadata from the verified source manifest into every segment.
"""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / 'grounded'
SRC = G / 'verified_sources.csv'
SEG = G / 'verified_segments.jsonl'

sources = {}
with SRC.open(newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        sources[r['source_id']] = r

updated = []
for line in SEG.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    s = json.loads(line)
    src = sources.get(s.get('source_id'), {})
    if not src:
        raise SystemExit(f"segment {s.get('segment_id')} references unknown source {s.get('source_id')}")
    s['source_url'] = src.get('url', '')
    s['source_title'] = src.get('title', '')
    s['source_retrieved_at'] = src.get('retrieved_at', '')
    s['source_class'] = src.get('source_class', '')
    s['public_locator'] = f"{s['source_url']}::{s.get('line_range','')}"
    updated.append(s)

with SEG.open('w', encoding='utf-8') as f:
    for s in updated:
        f.write(json.dumps(s, sort_keys=True) + '\n')
print(f'Annotated {len(updated)} verified segments with public source URLs')
