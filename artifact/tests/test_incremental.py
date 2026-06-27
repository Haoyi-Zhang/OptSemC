from pathlib import Path

from optsemc.incremental import source_influence, TOTAL_MAP_ROWS

ROOT = Path(__file__).resolve().parents[1]


def test_source_influence_counts():
    rows, summary = source_influence(ROOT)
    assert len(rows) == 26
    assert summary.sources == 26
    assert summary.rules == 287
    assert summary.total_map_rows == TOTAL_MAP_ROWS


def test_source_update_footprints_are_engine_local():
    rows, _summary = source_influence(ROOT)
    assert max(row.affected_maps for row in rows) <= 4216
    assert max(row.affected_map_share for row in rows) <= 1.0 / 7.0 + 1e-6
