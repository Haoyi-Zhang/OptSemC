#!/usr/bin/env python3
"""Check projection information-loss diagnostics against headline invariants."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evaluation" / "projection_information_profile_check.csv"
INFO = ROOT / "evaluation" / "projection_information_profile.csv"
rows=[]
def add(check, ok, details=""):
    rows.append({"check":check,"passed":str(bool(ok)).lower(),"details":str(details)})
with INFO.open(newline='', encoding='utf-8') as f:
    data = {r['projection']: r for r in csv.DictReader(f)}
add('required_projection_profiles_present', {'strict','keyword','operator_only','state_only','operator_kind_surface'}.issubset(data), f"projections={len(data)}")
add('strict_is_information_negative_control', int(data['strict']['false_equivalences']) == 0 and float(data['strict']['entropy_retained']) >= 0.999, data['strict'])
add('keyword_projection_has_nontrivial_kernel', int(data['keyword']['false_equivalences']) == 254 and int(data['keyword']['projected_collision_classes']) > 0, data['keyword'])
add('operator_projection_has_nontrivial_kernel', int(data['operator_only']['false_equivalences']) == 238 and int(data['operator_only']['projected_collision_classes']) > 0, data['operator_only'])
add('state_only_is_strictly_worse_than_keyword', float(data['state_only']['conditional_false_rate']) > float(data['keyword']['conditional_false_rate']), data['state_only']['conditional_false_rate'])
add('surface_projection_recovers_exact_kernel', int(data['operator_kind_surface']['false_equivalences']) == 0 and int(data['operator_kind_surface']['projected_equivalences']) == int(data['strict']['projected_equivalences']), '')
with OUT.open('w', newline='', encoding='utf-8') as f:
    w=csv.DictWriter(f, fieldnames=['check','passed','details']); w.writeheader(); w.writerows(rows)
passed=sum(r['passed']=='true' for r in rows)
print(f"Projection information profile check: {passed}/{len(rows)} passed")
if passed != len(rows):
    for r in rows:
        if r['passed'] != 'true': print('FAIL', r)
    sys.exit(1)
