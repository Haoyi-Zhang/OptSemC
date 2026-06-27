#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_probe_objects
from optsemc.sql_render import shape_rows, shape_consistent_with_features
from optsemc.io import write_csv
probes=load_probe_objects(ART)
issues=[]
for p in probes:
    ok, detail=shape_consistent_with_features(p.sql_skeleton, p.feature_vector)
    for d in detail:
        issues.append({'probe_id':p.probe_id,'issue':d})
write_csv(ART/'evaluation'/'sql_shape_diagnostics.csv', shape_rows(probes), ['probe_id','has_join','join_count','has_filter','has_group','has_order','has_limit','has_cte','token_count'])
write_csv(ART/'evaluation'/'sql_shape_feature_issues.csv', issues or [{'probe_id':'none','issue':'no issues'}], ['probe_id','issue'])
print(f'SQL shape diagnostics: probes={len(probes)} issues={len(issues)}')
