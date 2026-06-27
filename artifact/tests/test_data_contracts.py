from pathlib import Path
import tempfile
import json

from optsemc.data_contracts import (
    CSVContract, JSONLContract, ColumnSpec, JSONFieldSpec,
    nonnegative_integer, rate, boolish, validate_contracts, cross_file_invariants,
)

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent


def test_nonnegative_integer_accepts_zero():
    assert nonnegative_integer('0')


def test_nonnegative_integer_rejects_negative():
    assert not nonnegative_integer('-1')


def test_rate_accepts_one():
    assert rate('1.0')


def test_rate_rejects_over_one():
    assert not rate('1.1')


def test_boolish_accepts_true():
    assert boolish('true')


def test_boolish_rejects_maybe():
    assert not boolish('maybe')


def test_csv_contract_passes_minimal_file():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / 'x.csv').write_text('id,count\na,1\n', encoding='utf-8')
        contract = CSVContract('x', 'x.csv', (ColumnSpec('id'), ColumnSpec('count', validator=nonnegative_integer)), unique_key=('id',))
        assert contract.validate(root).passed


def test_csv_contract_detects_duplicate_key():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / 'x.csv').write_text('id,count\na,1\na,2\n', encoding='utf-8')
        contract = CSVContract('x', 'x.csv', (ColumnSpec('id'), ColumnSpec('count', validator=nonnegative_integer)), unique_key=('id',))
        result = contract.validate(root)
        assert not result.passed
        assert any('duplicate' in issue.message for issue in result.issues)


def test_jsonl_contract_passes_nested_field():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / 'x.jsonl').write_text(json.dumps({'id': 'a', 'nested': {'state': 'MAY'}}) + '\n', encoding='utf-8')
        contract = JSONLContract('x', 'x.jsonl', (JSONFieldSpec(('id',)), JSONFieldSpec(('nested', 'state'))), unique_path=('id',))
        assert contract.validate(root).passed


def test_jsonl_contract_detects_missing_nested_field():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / 'x.jsonl').write_text(json.dumps({'id': 'a', 'nested': {}}) + '\n', encoding='utf-8')
        contract = JSONLContract('x', 'x.jsonl', (JSONFieldSpec(('nested', 'state')),))
        assert not contract.validate(root).passed


def test_repository_contracts_all_pass():
    results = validate_contracts(PKG)
    assert results
    assert all(result.passed for result in results)


def test_cross_file_invariants_all_pass():
    rows = cross_file_invariants(PKG)
    assert rows
    assert all(row['passed'] == 'true' for row in rows)


def test_grounded_rules_contract_count_is_fixed():
    rows = {result.contract: result for result in validate_contracts(PKG)}
    assert rows['grounded_rules'].rows == 287


def test_generated_probe_contract_count_is_fixed():
    rows = {result.contract: result for result in validate_contracts(PKG)}
    assert rows['generated_probes'].rows == 4216


def test_projection_mutation_suite_contract_count_is_large():
    rows = {result.contract: result for result in validate_contracts(PKG)}
    assert rows['projection_mutation_suite'].rows >= 41
