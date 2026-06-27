"""Command-line interface for the OptSem-C artifact."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable

import yaml

from .corpus import load_contract_maps, load_engines_probes
from .metrics import equivalence_metrics
from .manifest import build_manifest, manifest_fingerprint, manifest_summary
from .repository import repository_audit, score_row
from .data_contracts import validate_contracts, result_rows
from .claim_graph import build_claim_graph, graph_summary
from .benchmark_compiler import load_suite_requirements, load_probe_features, compute_motif_coverage, suite_summary
from .differential import run_differential_reproducibility


def _write_rows(rows: Iterable[dict[str, str]], path: Path | None) -> None:
    rows = list(rows)
    if not rows:
        return
    if path is None:
        writer = csv.DictWriter(__import__("sys").stdout, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)


def cmd_summary(args: argparse.Namespace) -> int:
    root = Path(args.root)
    cm = load_contract_maps(root / "artifact")
    rows = [
        {"metric": "engines", "value": str(len(cm.engines))},
        {"metric": "probes", "value": str(len(cm.probes))},
        {"metric": "contract_maps", "value": str(len(cm.maps))},
    ]
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0


def cmd_metrics(args: argparse.Namespace) -> int:
    root = Path(args.root)
    cm = load_contract_maps(root / "artifact")
    rows = [equivalence_metrics(cm.maps, cm.engines, cm.probes, projection).as_row() for projection in args.projection]
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0


def cmd_manifest(args: argparse.Namespace) -> int:
    root = Path(args.root)
    rows = build_manifest(root)
    if args.summary:
        out = manifest_summary(rows)
        out.append({"category": "fingerprint", "files": str(len(rows)), "bytes": manifest_fingerprint(rows), "lines": ""})
        _write_rows(out, Path(args.output) if args.output else None)
    else:
        _write_rows([row.as_row() for row in rows], Path(args.output) if args.output else None)
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    root = Path(args.root)
    checks = repository_audit(root)
    rows = [check.as_row() for check in checks]
    rows.append(score_row(checks))
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0 if all(check.passed for check in checks) else 1



def cmd_contracts(args: argparse.Namespace) -> int:
    root = Path(args.root)
    rows = result_rows(validate_contracts(root))
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0 if all(row.get("passed") == "true" for row in rows) else 1


def cmd_claim_graph(args: argparse.Namespace) -> int:
    root = Path(args.root)
    graph = build_claim_graph(root)
    rows = graph_summary(graph, root)
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0


def cmd_benchmark_compile(args: argparse.Namespace) -> int:
    root = Path(args.root)
    artifact = root / "artifact"
    motifs = load_suite_requirements(artifact / "external" / "benchmark_suites.yaml")
    probes = load_probe_features(artifact / "benchmark" / "generated_probes.jsonl")
    rows = suite_summary(compute_motif_coverage(motifs, probes))
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0 if all(float(row.get("coverage_rate", 0)) >= 1.0 for row in rows) else 1


def cmd_differential(args: argparse.Namespace) -> int:
    root = Path(args.root)
    rows = [row.as_row() for row in run_differential_reproducibility(root)]
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0 if all(row.get("passed") == "true" for row in rows) else 1

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="optsemc", description="OptSem-C artifact utilities")
    parser.add_argument("--root", default=".", help="repository root")
    sub = parser.add_subparsers(dest="command", required=True)
    p_summary = sub.add_parser("summary", help="print corpus summary")
    p_summary.add_argument("--output")
    p_summary.set_defaults(func=cmd_summary)
    p_metrics = sub.add_parser("metrics", help="compute projection metrics")
    p_metrics.add_argument("--projection", nargs="+", default=["keyword", "yesno", "operator_only"])
    p_metrics.add_argument("--output")
    p_metrics.set_defaults(func=cmd_metrics)
    p_manifest = sub.add_parser("manifest", help="build package manifest")
    p_manifest.add_argument("--summary", action="store_true")
    p_manifest.add_argument("--output")
    p_manifest.set_defaults(func=cmd_manifest)
    p_audit = sub.add_parser("audit", help="run repository audit gate")
    p_audit.add_argument("--output")
    p_audit.set_defaults(func=cmd_audit)
    p_contracts = sub.add_parser("contracts", help="validate data contracts")
    p_contracts.add_argument("--output")
    p_contracts.set_defaults(func=cmd_contracts)
    p_graph = sub.add_parser("claim-graph", help="summarize claim-to-evidence graph")
    p_graph.add_argument("--output")
    p_graph.set_defaults(func=cmd_claim_graph)
    p_bench = sub.add_parser("benchmark-compile", help="compile external benchmark motif coverage")
    p_bench.add_argument("--output")
    p_bench.set_defaults(func=cmd_benchmark_compile)
    p_diff = sub.add_parser("differential", help="run differential reproducibility checks")
    p_diff.add_argument("--output")
    p_diff.set_defaults(func=cmd_differential)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

