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


def row_passed(row: dict[str, str]) -> bool:
    if 'passed' in row:
        return row.get('passed', '').lower() == 'true'
    if 'status' in row:
        return row.get('status', '').upper() == 'PASS'
    if 'ok' in row:
        return row.get('ok', '').lower() == 'true'
    return True


def gate_file_status(cover_rows: list[dict[str, str]]) -> tuple[bool, str]:
    checked = 0
    failed: list[str] = []
    for rel in sorted({row.get('path', '') for row in cover_rows if row.get('path', '')}):
        path = ROOT / rel
        if not path.exists():
            failed.append(f'{rel}:missing')
            continue
        rows = read(path)
        passable = [row for row in rows if any(key in row for key in ('passed', 'status', 'ok'))]
        if not passable:
            continue
        checked += 1
        if not all(row_passed(row) for row in passable):
            failed.append(rel)
    return checked > 0 and not failed, f'checked={checked};failed={";".join(failed[:8])}'


claims = read(E / "claim_evidence_graph_claims.csv")
summary = {r['metric']: int(r['value']) for r in read(E / "claim_evidence_graph_summary.csv")}
cover = read(E / "claim_evidence_gate_cover.csv")
gate_cover_ok, gate_cover_details = gate_file_status(cover)
checks = [
    {"check": "claim_graph_has_claims", "passed": str(summary.get('claims', 0) >= 10).lower(), "details": f"claims={summary.get('claims', 0)}"},
    {"check": "claim_graph_has_edges", "passed": str(summary.get('edges', 0) >= 30).lower(), "details": f"edges={summary.get('edges', 0)}"},
    {"check": "all_claims_have_existing_support", "passed": str(bool(claims) and all(r.get('passed') == 'true' for r in claims)).lower(), "details": f"{sum(r.get('passed') == 'true' for r in claims)}/{len(claims)}"},
    {"check": "gate_cover_nonempty", "passed": str(bool(cover)).lower(), "details": f"cover_size={len(cover)}"},
    {"check": "gate_cover_files_pass", "passed": str(gate_cover_ok).lower(), "details": gate_cover_details},
]
with (E / "claim_evidence_graph_check.csv").open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=["check", "passed", "details"]); writer.writeheader(); writer.writerows(checks)
print(f"Claim graph check: {sum(r['passed']=='true' for r in checks)}/{len(checks)} passed")
if not all(r['passed'] == 'true' for r in checks):
    sys.exit(1)
