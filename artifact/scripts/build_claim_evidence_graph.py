#!/usr/bin/env python3
"""Build claim-to-evidence graph and gate cover."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "artifact"))
from optsemc.claim_graph import build_claim_graph, graph_metrics, graph_summary, gate_cover_rows
from optsemc.io import write_csv
E = ROOT / "artifact" / "evaluation"
graph = build_claim_graph(ROOT)
write_csv(E / "claim_evidence_graph_nodes.csv", [n.as_row() for n in graph.nodes], ["node_id", "kind", "label", "path"])
write_csv(E / "claim_evidence_graph.csv", [e.as_row() for e in graph.edges], ["source", "target", "relation"])
write_csv(E / "claim_evidence_graph_claims.csv", graph_metrics(graph, ROOT), ["claim_id", "claim", "supporting_files", "existing_supporting_files", "checking_gates", "passed"])
write_csv(E / "claim_evidence_graph_summary.csv", graph_summary(graph, ROOT), ["metric", "value"])
write_csv(E / "claim_evidence_gate_cover.csv", gate_cover_rows(graph), ["rank", "gate_id", "gate", "path", "claims_covered"])
print(f"Claim evidence graph: nodes={len(graph.nodes)} edges={len(graph.edges)} claims={len(graph.claims())}")
