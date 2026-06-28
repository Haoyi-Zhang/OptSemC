from pathlib import Path
import csv

from optsemc.corpus import load_contract_maps, load_probes
from optsemc.severity import false_equivalence_severity, jaccard_distance, symmetric_atom_delta
from optsemc.sql_multicatalog import execute_probe_suite_multicatalog, multicatalog_totals

ROOT = Path(__file__).resolve().parents[1]


def test_jaccard_distance_and_atom_delta_on_empty_and_disjoint_sets():
    assert jaccard_distance(frozenset(), frozenset()) == 0.0
    # Use two real signatures that are known to differ under the corpus.
    cm = load_contract_maps(ROOT)
    left = cm.maps[("BigQuery", "P0001")]
    right = cm.maps[("PostgreSQL", "P0001")]
    assert 0.0 <= jaccard_distance(left, right) <= 1.0
    assert symmetric_atom_delta(left, right) == len(left ^ right)


def test_false_equivalence_severity_headline_counts_and_distance():
    cm = load_contract_maps(ROOT)
    keyword = false_equivalence_severity(cm.maps, cm.engines, cm.probes, "keyword")
    operator = false_equivalence_severity(cm.maps, cm.engines, cm.probes, "operator_only")
    repaired = false_equivalence_severity(cm.maps, cm.engines, cm.probes, "operator_kind_surface")
    assert keyword.false_equivalences == 254
    assert operator.false_equivalences == 238
    assert repaired.false_equivalences == 0
    assert keyword.mean_exact_distance == 1.0
    assert operator.mean_atom_delta > 5.0


def test_multicatalog_executor_on_small_prefix():
    probes = load_probes(ROOT)[:12]
    details, summaries = execute_probe_suite_multicatalog(probes, catalog_sizes=(1, 3))
    totals = multicatalog_totals(summaries)
    assert len(details) == 24
    assert totals["total_probe_catalog_runs"] == "24"
    assert totals["total_execution_failures"] == "0"
    assert all(row["execution_successes"] == "12" for row in summaries)


def test_multicatalog_package_summary_matches_full_probe_count():
    with (ROOT / "evaluation/sql_probe_multicatalog_totals.csv").open(newline='', encoding='utf-8') as f:
        totals = {row['metric']: row['value'] for row in csv.DictReader(f)}
    assert totals['catalogs'] == '3'
    assert totals['probes_per_catalog'] == '4216'
    assert totals['total_probe_catalog_runs'] == '12648'
    assert totals['total_execution_failures'] == '0'
