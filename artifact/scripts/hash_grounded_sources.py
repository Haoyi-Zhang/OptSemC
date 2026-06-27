#!/usr/bin/env python3
import csv,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
G=ROOT/'grounded'; EVAL=ROOT/'evaluation'; EVAL.mkdir(exist_ok=True)
segments_by_source={}
for line in open(G/'verified_segments.jsonl'):
    if not line.strip(): continue
    s=json.loads(line)
    payload=json.dumps({k:s.get(k,'') for k in ['segment_id','line_range','claim_paraphrase','public_locator','source_url','grounding_status']},sort_keys=True)
    segments_by_source.setdefault(s['source_id'],[]).append(payload)
with open(G/'grounded_source_hashes.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['source_id','segment_count','hash_type','sha256','bytes'])
    for sid,items in sorted(segments_by_source.items()):
        data='\n'.join(sorted(items)).encode('utf-8')
        w.writerow([sid,len(items),'verified_segments_sha256',hashlib.sha256(data).hexdigest(),len(data)])
print(f'Wrote grounded hashes for {len(segments_by_source)} sources')
