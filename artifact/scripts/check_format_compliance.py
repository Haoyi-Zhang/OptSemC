#!/usr/bin/env python3
from __future__ import annotations
import csv, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
TEX = ROOT/'Paper'/'latex'/'paper.tex'
PDF = ROOT/'Paper'/'latex'/'paper.pdf'
OUT = ROOT/'artifact'/'evaluation'/'format_compliance.csv'
text = TEX.read_text(encoding='utf-8', errors='ignore') if TEX.exists() else ''
rows=[]
def add(check, ok, detail=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(detail)})
add(
    'uses_acmart_sigconf_nonacm',
    bool(re.search(r'\\documentclass\[\s*sigconf\s*,\s*nonacm\s*\]\{acmart\}', text)),
    'documentclass',
)
author_blocks = re.findall(r'\\author\{[^}]+\}(.*?)(?=\\author\{|\\begin\{document\})', text, re.S)
add('single_blind_author_block_present', len(author_blocks) >= 2 and all(x in text for x in ['\\affiliation','\\email']), 'authors')
add('pvl_db_reference_block_present', all(x in text for x in ['PVLDB Reference Format', 'PVLDB, \\vldbvolume', 'Proceedings of the VLDB Endowment', '\\vldbdoi', '\\vldbpages']), 'pvl_db_block')
author_two_text = author_blocks[1] if len(author_blocks) >= 2 else ''
add('author_two_affiliation_correct', all(x in author_two_text for x in ['Nanyang Technological University', '\\city{Singapore}', '\\country{Singapore}']) and 'Suzhou' not in author_two_text, 'ntu_singapore')
add('no_track_suffix_in_title', '[Vision]' not in text and '[Experiment' not in text and '[Scalable' not in text, 'regular research')
add('abstract_nonplaceholder', len(re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', text, re.S).group(1).strip()) > 1000 if re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', text, re.S) else False, 'abstract')
bibtex_configured = (
    '\\bibliographystyle{ACM-Reference-Format}' in text
    and '\\bibliography{refs}' in text
    and (ROOT/'Paper'/'latex'/'refs.bib').exists()
)
add('references_acm_bibtex_configured', bibtex_configured or '\\begin{thebibliography}' in text, 'bibliography')
try:
    from pypdf import PdfReader
    reader = PdfReader(str(PDF))
    pages = len(reader.pages)
    page_texts=[p.extract_text() or '' for p in reader.pages]
    refs=[
        i+1
        for i,t in enumerate(page_texts)
        if any(line.strip().upper() == 'REFERENCES' for line in t.splitlines())
    ]
    add('pdf_pages_with_references', pages >= 13 and refs and refs[0] == 13, f'pages={pages};refs={refs[:3]}')
except Exception as e:
    add('pdf_pages_with_references', False, type(e).__name__)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Format compliance: {len(rows)-len(failed)}/{len(rows)} passed')
for r in failed: print('FAIL', r)
sys.exit(1 if failed else 0)
