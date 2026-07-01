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
except Exception as e:
    add('pdf_readable_by_pypdf', False, type(e).__name__, 'readable')
    pages = 0

try:
    proc = subprocess.run(['pdftotext', str(PDF), '-'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    text = proc.stdout if proc.returncode == 0 else ''
    add('pdf_text_extractable', proc.returncode == 0 and len(text) > 1000, len(text), '>1000 chars')
    add('title_present', 'Public Optimizer Contracts' in text, 'yes' if 'Public Optimizer Contracts' in text else 'no', 'yes')
    normalized = ' '.join(text.split()).lower()
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
