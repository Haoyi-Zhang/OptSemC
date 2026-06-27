#!/usr/bin/env python3
"""Build the public evidence DAG and deep provenance audit."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'artifact'
sys.path.insert(0, str(ART))
from optsemc.corpus import load_rule_objects, load_segment_objects, load_source_objects
from optsemc.provenance import audit_provenance, provenance_edges, source_coverage, evidence_depth_by_engine
from optsemc.io import write_csv
rules=load_rule_objects(ART); segments=load_segment_objects(ART); sources=load_source_objects(ART)
issues=audit_provenance(rules, segments, sources)
write_csv(ART/'evaluation'/'provenance_deep_audit.csv', [i.as_row() for i in issues] or [{'kind':'none','object_id':'none','details':'no issues'}], ['kind','object_id','details'])
write_csv(ART/'evaluation'/'provenance_graph_edges.csv', provenance_edges(rules, segments), ['from_type','from_id','to_type','to_id','edge'])
write_csv(ART/'evaluation'/'provenance_source_coverage.csv', source_coverage(rules), ['source_id','source_class','rules','engines','engine_list'])
write_csv(ART/'evaluation'/'evidence_depth_by_engine.csv', evidence_depth_by_engine(rules), ['engine','rules','sources','segments','operators','layers'])
print(f"Provenance deep audit: issues={len(issues)}; edges={len(rules)*2}")

