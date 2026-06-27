#!/usr/bin/env python3
"""Check claim-to-evidence graph completeness."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
E = ROOT / "artifact" / "evaluation"

def read(path: Path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))
claims = read(E / "claim_evidence_graph_claims.csv")
summary = {r['metric']: int(r['value']) for r in read(E / "claim_evidence_graph_summary.csv")}
cover = read(E / "claim_evidence_gate_cover.csv")
checks = [
    {"check": "claim_graph_has_claims", "passed": str(summary.get('claims', 0) >= 10).lower(), "details": f"claims={summary.get('claims', 0)}"},
    {"check": "claim_graph_has_edges", "passed": str(summary.get('edges', 0) >= 30).lower(), "details": f"edges={summary.get('edges', 0)}"},
    {"check": "all_claims_have_existing_support", "passed": str(bool(claims) and all(r.get('passed') == 'true' for r in claims)).lower(), "details": f"{sum(r.get('passed') == 'true' for r in claims)}/{len(claims)}"},
    {"check": "gate_cover_nonempty", "passed": str(bool(cover)).lower(), "details": f"cover_size={len(cover)}"},
]
with (E / "claim_evidence_graph_check.csv").open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"]); writer.writeheader(); writer.writerows(checks)
print(f"Claim graph check: {sum(r['passed']=='true' for r in checks)}/{len(checks)} passed")
if not all(r['passed'] == 'true' for r in checks):
    sys.exit(1)
