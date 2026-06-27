from collections import Counter
from pathlib import Path
import csv

from optsemc.corpus import load_probes
from optsemc.information import entropy
from optsemc.sql_bundle import bundle_manifest_rows, probe_comment, sql_filename, sql_payload

ROOT = Path(__file__).resolve().parents[1]


def test_entropy_zero_and_binary_distribution():
    assert entropy(Counter()) == 0.0
    assert round(entropy(Counter({('a',): 1, ('b',): 1})), 6) == 1.0


def _information_rows():
    with (ROOT / 'evaluation/projection_information_profile.csv').open(newline='', encoding='utf-8') as f:
        return {row['projection']: row for row in csv.DictReader(f)}


def test_projection_information_negative_and_positive_controls():
    by_projection = _information_rows()
    assert int(by_projection['strict']['false_equivalences']) == 0
    assert int(by_projection['operator_kind_surface']['false_equivalences']) == 0
    assert int(by_projection['keyword']['false_equivalences']) == 254
    assert int(by_projection['operator_only']['false_equivalences']) == 238
    assert float(by_projection['keyword']['kernel_inflation']) > 1.0


def test_information_profile_entropy_monotonicity_for_lossy_projection():
    by_projection = _information_rows()
    strict = by_projection['strict']
    keyword = by_projection['keyword']
    assert float(strict['entropy_retained']) == 1.0
    assert 0.0 < float(keyword['entropy_retained']) < float(strict['entropy_retained'])
    assert int(keyword['projected_collision_classes']) > 0


def test_sql_bundle_manifest_covers_all_probes_and_shapes():
    probes = load_probes(ROOT)
    rows = bundle_manifest_rows(probes)
    assert len(rows) == 4216
    assert all(row['sql_file'] == sql_filename(row['probe_id']) for row in rows)
    assert all(row['shape_valid'] == 'true' for row in rows)
    assert len({row['sql_sha256'] for row in rows}) >= 200


def test_sql_payload_is_self_describing_and_terminated():
    probe = load_probes(ROOT)[0]
    comment = probe_comment(probe)
    payload = sql_payload(probe)
    assert comment.startswith('-- OptSemBench-C probe ')
    assert '-- features:' in comment
    assert payload.endswith(';\n')
    assert str(probe['probe_id']) in payload
