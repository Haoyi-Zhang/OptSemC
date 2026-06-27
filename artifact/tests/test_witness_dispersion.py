from optsemc.witnesses import WitnessRecord, dispersion_by_projection, feature_coverage_rows, greedy_probe_cover


def test_witness_dispersion_counts_features_and_pairs():
    records = (
        WitnessRecord("keyword", "P1", "A", "B"),
        WitnessRecord("keyword", "P2", "A", "C"),
        WitnessRecord("operator_only", "P2", "A", "C"),
    )
    features = {
        "P1": {"join_type": "inner", "source_boundary": "local"},
        "P2": {"join_type": "outer", "source_boundary": "remote"},
    }
    rows = {row.projection: row for row in dispersion_by_projection(records, features)}
    assert rows["keyword"].false_witnesses == 2
    assert rows["keyword"].distinct_probes == 2
    assert rows["keyword"].distinct_engine_pairs == 2
    assert rows["keyword"].feature_dimensions_touched == 2
    assert rows["operator_only"].distinct_probes == 1


def test_witness_feature_coverage_and_greedy_cover():
    records = (
        WitnessRecord("keyword", "P1", "A", "B"),
        WitnessRecord("keyword", "P2", "A", "B"),
    )
    features = {
        "P1": {"join_type": "inner", "source_boundary": "local"},
        "P2": {"join_type": "outer", "source_boundary": "remote"},
        "P3": {"join_type": "semi", "source_boundary": "local"},
    }
    coverage = {row["feature"]: row for row in feature_coverage_rows(records, features, features)}
    assert coverage["join_type"]["touched_values"] == "2"
    assert coverage["join_type"]["total_values"] == "3"
    cover = greedy_probe_cover(records)
    assert cover[-1]["cumulative_witnesses"] == "2"
    assert cover[-1]["total_witnesses"] == "2"
