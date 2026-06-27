from pathlib import Path

from optsemc.architecture import import_edges, internal_adjacency, module_name, strongly_connected_components
from optsemc.scalability import natural_probe_key, pair_family

ROOT = Path(__file__).resolve().parents[1]


def test_natural_probe_key_orders_numeric_suffixes():
    assert sorted(["P10", "P2", "P1"], key=natural_probe_key) == ["P1", "P2", "P10"]


def test_engine_pair_family_is_symmetric():
    assert pair_family("BigQuery", "DuckDB") == pair_family("DuckDB", "BigQuery")


def test_package_import_graph_has_no_cycles():
    pkg = ROOT / "optsemc"
    modules = sorted(module_name(p, pkg.parent) for p in pkg.glob("*.py"))
    adj = internal_adjacency(import_edges(pkg), modules)
    assert strongly_connected_components(adj) == []
