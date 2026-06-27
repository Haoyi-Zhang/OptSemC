from pathlib import Path
from optsemc.claim_graph import build_claim_graph, graph_metrics, graph_summary, gate_cover_rows

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT.parent


def test_claim_graph_has_claim_nodes():
    graph = build_claim_graph(PKG)
    assert len(graph.claims()) >= 20


def test_claim_graph_has_file_nodes():
    graph = build_claim_graph(PKG)
    assert len(graph.files()) >= 90


def test_claim_graph_edges_are_nonempty():
    graph = build_claim_graph(PKG)
    assert len(graph.edges) >= 70


def test_claim_graph_metrics_all_pass():
    graph = build_claim_graph(PKG)
    rows = graph_metrics(graph, PKG)
    assert all(row['passed'] == 'true' for row in rows)


def test_claim_graph_summary_existing_files_match():
    summary = {row['metric']: int(row['value']) for row in graph_summary(build_claim_graph(PKG), PKG)}
    assert summary['files'] == summary['existing_files']


def test_claim_gate_cover_nonempty():
    rows = gate_cover_rows(build_claim_graph(PKG))
    assert rows


def test_claim_gate_cover_covers_claims():
    rows = gate_cover_rows(build_claim_graph(PKG))
    assert sum(int(row['claims_covered']) for row in rows) >= len(build_claim_graph(PKG).claims())


def test_claim_graph_reachable_files_for_first_claim():
    graph = build_claim_graph(PKG)
    claim = graph.claims()[0]
    assert graph.reachable(claim.node_id, kinds={'file'})


def test_claim_graph_reachable_gates_for_first_claim():
    graph = build_claim_graph(PKG)
    claim = graph.claims()[0]
    assert graph.reachable(claim.node_id, kinds={'gate'})


def test_claim_graph_node_ids_unique():
    graph = build_claim_graph(PKG)
    assert len(graph.nodes) == len({node.node_id for node in graph.nodes})
