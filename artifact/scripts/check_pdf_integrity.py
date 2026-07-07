#!/usr/bin/env python3
"""Validate the compiled paper PDF is readable, has expected pages, and contains key claims."""
from __future__ import annotations
import csv, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / 'Paper' / 'latex' / 'paper.pdf'
OUT = ROOT / 'artifact' / 'evaluation' / 'pdf_integrity.csv'
checks=[]

def add(name, passed, value='', target=''):
    checks.append({'check': name, 'passed': str(bool(passed)).lower(), 'value': str(value), 'target': str(target)})

try:
    from pypdf import PdfReader
    reader = PdfReader(str(PDF))
    pages = len(reader.pages)
    add('pdf_readable_by_pypdf', True, 'readable', 'readable')
    add('total_pages_with_references', pages >= 13, pages, 'body pages plus unlimited references')
    page_texts = [page.extract_text() or '' for page in reader.pages]
    ref_pages = [
        i + 1
        for i, text in enumerate(page_texts)
        if any(line.strip().upper() == 'REFERENCES' for line in text.splitlines())
    ]
    add('body_pages_12_references_start_13', ref_pages and ref_pages[0] == 13, ref_pages, 'references start on page 13')
    if ref_pages:
        first_ref_lines = [line.strip() for line in page_texts[ref_pages[0] - 1].splitlines() if line.strip()]
        add(
            'reference_page_has_no_body_prefix',
            bool(first_ref_lines) and first_ref_lines[0].upper() == 'REFERENCES',
            first_ref_lines[:3],
            'first substantive line is REFERENCES',
        )
    else:
        add('reference_page_has_no_body_prefix', False, 'no reference page', 'first substantive line is REFERENCES')
    if len(page_texts) >= 12:
        add(
            'body_page_12_has_no_references_heading',
            not any(line.strip().upper() == 'REFERENCES' for line in page_texts[11].splitlines()),
            'checked',
            'no REFERENCES heading on body page 12',
        )
    else:
        add('body_page_12_has_no_references_heading', False, f'pages={len(page_texts)}', '12 body pages')
except Exception as e:
    add('pdf_readable_by_pypdf', False, type(e).__name__, 'readable')
    pages = 0

try:
    proc = subprocess.run(['pdftotext', str(PDF), '-'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    text = proc.stdout if proc.returncode == 0 else ''
    add('pdf_text_extractable', proc.returncode == 0 and len(text) > 1000, len(text), '>1000 chars')
    normalized_text = ' '.join(text.split())
    title_seen = 'OptSem-C: Auditing Federated SQL Optimizer Contracts' in normalized_text
    add('title_present', title_seen, 'yes' if title_seen else 'no', 'yes')
    normalized = normalized_text.lower()
    collision_claim = (
        'contract collision' in normalized
        or 'collision witnesses' in normalized
        or 'public contracts disagree' in normalized
    )
    core_claim = 'projection kernel' in normalized and collision_claim
    add('core_claim_present', core_claim, 'yes' if core_claim else 'no', 'yes')
except Exception as e:
    add('pdf_text_extractable', False, type(e).__name__, 'extractable')

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['check','passed','value','target'])
    w.writeheader(); w.writerows(checks)
failed=[c for c in checks if c['passed']!='true']
print(f'PDF integrity checks: {len(checks)-len(failed)}/{len(checks)} passed')
if failed:
    for c in failed: print('FAIL', c)
    sys.exit(1)
