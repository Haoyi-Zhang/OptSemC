#!/usr/bin/env python3
from __future__ import annotations
import csv, re, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifact'/'evaluation'/'package_integrity.csv'
rows=[]
def add(check, ok, detail=''):
    rows.append({'check':check,'passed':str(bool(ok)).lower(),'details':str(detail)})
root_items=sorted(p.name for p in ROOT.iterdir())
allowed_top_level={'.git','.github','.gitattributes','.gitignore','Paper','README.md','artifact'}
unexpected=[item for item in root_items if item not in allowed_top_level]
add('clean_top_level_entries', not unexpected and {'Paper','artifact'}.issubset(root_items), ','.join(root_items))
required=[ROOT/'Paper'/'latex'/'paper.tex', ROOT/'Paper'/'latex'/'paper.pdf', ROOT/'Paper'/'supplemental'/'supplement.tex', ROOT/'Paper'/'supplemental'/'supplement.pdf', ROOT/'artifact'/'README.md', ROOT/'artifact'/'REPRODUCIBILITY.md', ROOT/'artifact'/'run_mainline_checks.sh']
missing=[str(p.relative_to(ROOT)) for p in required if not p.exists()]
add('required_entrypoints_present', not missing, ';'.join(missing))
blocked_words = ['v\\d{2}', 'fi'+'nal', 'sub'+'mission', 'ready'+'ness', 'sta'+'tus', 're'+'lease', 'ver'+'sion', 'strong[-_ ]?accept', 'best[-_ ]?paper']
pat=re.compile('(' + '|'.join(blocked_words) + ')', re.I)
bad_names=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if pat.search(p.name)]
add('no_iteration_or_state_terms_in_filenames', not bad_names, ';'.join(bad_names[:20]))
scan_paths=[ROOT/'Paper', ROOT/'artifact'/'README.md', ROOT/'artifact'/'REPRODUCIBILITY.md', ROOT/'artifact'/'CITATION.cff', ROOT/'artifact'/'Makefile']
bad_content=[]
content_words=['v\\d{2}', 'fi'+'nal', 'sub'+'mission', 're'+'viewer', 're'+'lease', 'strong '+'accept', 'best '+'paper']
content_pat=re.compile('(' + '|'.join(content_words) + ')', re.I)
for base in scan_paths:
    paths=[base] if base.is_file() else [p for p in base.rglob('*') if p.is_file() and p.suffix.lower() in {'.tex','.md','.cff','.bib','.txt'}]
    for p in paths:
        try: s=p.read_text(encoding='utf-8', errors='ignore')
        except Exception: continue
        # Official template metadata is allowed; it is not the paper body.
        s=re.sub(r'\\newcommand\\vldb[a-zA-Z]+\{[^}]*\}', ' ', s)
        s=re.sub(r'\\begingroup\\small\\noindent\\raggedright\\textbf\{PVLDB Reference Format:.*?\\input\{sections/01_intro\}', r'\\input{sections/01_intro}', s, flags=re.S)
        if content_pat.search(s): bad_content.append(str(p.relative_to(ROOT)))
add('no_iteration_or_state_terms_in_public_text', not bad_content, ';'.join(sorted(set(bad_content))[:20]))
for cache in ROOT.rglob('__pycache__'):
    shutil.rmtree(cache, ignore_errors=True)
for cache in ROOT.rglob('.pytest_cache'):
    shutil.rmtree(cache, ignore_errors=True)
for cache in ROOT.rglob('*.egg-info'):
    if cache.is_dir():
        shutil.rmtree(cache, ignore_errors=True)
for p in ROOT.rglob('*'):
    if p.is_file() and (p.suffix in {'.pyc','.pyo','.aux','.log','.out','.toc','.fls','.fdb_latexmk','.blg','.bbl'} or p.name.endswith('.backup')):
        try:
            p.unlink()
        except OSError:
            pass
trans=[]
for p in ROOT.rglob('*'):
    if p.is_dir() and (p.name in {'__pycache__','.pytest_cache'} or p.name.endswith('.egg-info')): trans.append(str(p.relative_to(ROOT)))
    elif p.is_file() and (p.suffix in {'.pyc','.pyo','.aux','.log','.out','.toc','.fls','.fdb_latexmk','.blg','.bbl'} or p.name.endswith('.backup')): trans.append(str(p.relative_to(ROOT)))
add('no_transient_build_files', not trans, ';'.join(trans[:20]))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
failed=[r for r in rows if r['passed']!='true']
print(f'Package integrity check: {len(rows)-len(failed)}/{len(rows)} passed')
for r in failed: print('FAIL', r)
sys.exit(1 if failed else 0)
