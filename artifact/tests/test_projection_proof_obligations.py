#!/usr/bin/env python3
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    with (ROOT / path).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def test_projection_proof_obligations_pass():
    rr = rows('evaluation/projection_proof_obligations.csv')
    assert rr
    assert all(r['passed'] == 'true' for r in rr)
    assert len(rr) == 20

def test_stale_diagnostic_outputs_absent():
    rr = rows('evaluation/stale_diagnostic_outputs.csv')
    assert rr
    assert all(r['passed'] == 'true' for r in rr)

