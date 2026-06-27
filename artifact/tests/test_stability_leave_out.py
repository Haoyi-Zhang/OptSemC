from pathlib import Path

from optsemc.corpus import load_contract_maps
from optsemc.stability import compact_paper_rows, leave_out_stability_profile, summarize_stability


def test_leave_out_stability_profiles_resolve_by_repair():
    cm = load_contract_maps(Path(__file__).resolve().parents[1])
    rows = leave_out_stability_profile(cm.maps, cm.engines, cm.probes, ("strict", "keyword", "operator_only", "operator_kind_surface"))
    assert rows
    assert all(row.unresolved_after_layer_placement == 0 for row in rows)
    by_projection = {row.projection for row in rows}
    assert by_projection == {"strict", "keyword", "operator_only", "operator_kind_surface"}


def test_leave_out_stability_preserves_headline_counts():
    cm = load_contract_maps(Path(__file__).resolve().parents[1])
    rows = leave_out_stability_profile(cm.maps, cm.engines, cm.probes, ("strict", "keyword", "operator_only", "operator_kind_surface"))
    all_rows = {row.projection: row for row in rows if row.scope_kind == "all"}
    assert all_rows["strict"].false_equivalences == 0
    assert all_rows["keyword"].false_equivalences == 254
    assert all_rows["operator_only"].false_equivalences == 238
    assert all_rows["operator_kind_surface"].false_equivalences == 0


def test_leave_out_stability_summaries_are_paper_ready():
    cm = load_contract_maps(Path(__file__).resolve().parents[1])
    projections = ("strict", "keyword", "yesno", "operator_only", "operator_kind_surface")
    rows = leave_out_stability_profile(cm.maps, cm.engines, cm.probes, projections)
    summary = summarize_stability(rows)
    paper = compact_paper_rows(rows, projections)
    assert len(summary) >= 12
    assert len(paper) == 5
    assert all(row["max_unresolved_after_repair"] == "0" for row in paper)
