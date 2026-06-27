from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / "evaluation"


def read_csv(name):
    with (EVAL / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_projection_frontier_antichain_summary_counts():
    rows = {row["universe"]: row for row in read_csv("projection_frontier_antichain_summary.csv")}
    assert set(rows) == {"all_fields", "semantic_no_variant"}
    assert rows["all_fields"]["subsets"] == "256"
    assert rows["semantic_no_variant"]["subsets"] == "128"
    assert rows["semantic_no_variant"]["safe_subsets"] == "84"
    assert rows["semantic_no_variant"]["unsafe_subsets"] == "44"


def test_projection_frontier_has_expected_minimum_semantic_basis():
    rows = {row["universe"]: row for row in read_csv("projection_frontier_antichain_summary.csv")}
    assert rows["semantic_no_variant"]["minimum_safe_size"] == "2"
    assert set(rows["semantic_no_variant"]["minimum_safe_fields"].split(";")) == {"kind+placement", "operator+layer"}


def test_projection_frontier_antichains_are_covering_certificates():
    rows = read_csv("projection_frontier_antichain_summary.csv")
    for row in rows:
        assert row["monotone_safe"] == "true"
        assert row["monotone_unsafe"] == "true"
        assert row["every_safe_covered"] == "true"
        assert row["every_unsafe_covered"] == "true"


def test_semantic_frontier_row_counts_and_false_counts():
    rows = [row for row in read_csv("projection_frontier_antichains.csv") if row["universe"] == "semantic_no_variant"]
    min_safe = [row for row in rows if row["frontier"] == "minimal_safe"]
    max_unsafe = [row for row in rows if row["frontier"] == "maximal_unsafe"]
    assert len(min_safe) == 14
    assert len(max_unsafe) == 8
    assert all(int(row["false_equivalences"]) == 0 for row in min_safe)
    assert all(int(row["false_equivalences"]) > 0 for row in max_unsafe)
