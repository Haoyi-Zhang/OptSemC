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
from .projections import false_equivalence_witnesses
from .semantics import ActionAtom, ContractSignature, FIELDS, UNSPEC
from .severity import field_value_delta, symmetric_atom_delta
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


def _atom_text(signature: ContractSignature) -> str:
    return ";".join("|".join(atom.as_tuple()) for atom in sorted(signature))


def _witness_rows(
    maps: dict[tuple[str, str], ContractSignature],
    engines: tuple[str, ...],
    probes: tuple[str, ...],
    projections: list[str],
    limit: int,
) -> list[dict[str, str]]:
    empty: ContractSignature = frozenset()
    rows: list[dict[str, str]] = []
    for projection in projections:
        for method, probe_id, left_key, right_key in false_equivalence_witnesses(maps, engines, probes, projection)[:limit]:
            left = maps.get(left_key, empty)
            right = maps.get(right_key, empty)
            field_delta = field_value_delta(left, right)
            rows.append(
                {
                    "projection": method,
                    "probe_id": probe_id,
                    "engine_left": left_key[0],
                    "engine_right": right_key[0],
                    "atom_delta": str(symmetric_atom_delta(left, right)),
                    "differing_fields": ";".join(field for field, _count in field_delta.most_common()),
                    "left_atoms": _atom_text(left),
                    "right_atoms": _atom_text(right),
                }
            )
    return rows


def _contract_maps_from_csv(path: Path) -> tuple[dict[tuple[str, str], ContractSignature], tuple[str, ...], tuple[str, ...]]:
    required = {"engine", "probe_id", "operator", "kind", "layer", "placement", "decision_time", "observability"}
    maps: dict[tuple[str, str], set[ActionAtom]] = {}
    engines: set[str] = set()
    probes: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise SystemExit(f"input CSV missing required columns: {','.join(sorted(missing))}")
        for line_no, row in enumerate(reader, 2):
            engine = (row.get("engine") or "").strip()
            probe_id = (row.get("probe_id") or "").strip()
            if not engine or not probe_id:
                raise SystemExit(f"{path}:{line_no}: engine and probe_id are required")
            state = (row.get("state") or "MUST").strip() or "MUST"
            if state == UNSPEC:
                continue
            atom = ActionAtom(
                operator=(row.get("operator") or "").strip(),
                kind=(row.get("kind") or "").strip(),
                variant=(row.get("variant") or "").strip(),
                layer=(row.get("layer") or "").strip(),
                placement=(row.get("placement") or "").strip(),
                decision_time=(row.get("decision_time") or "").strip(),
                observability=(row.get("observability") or "").strip(),
                state=state,
            )
            if any(not atom.field(field) for field in FIELDS if field != "variant"):
                raise SystemExit(f"{path}:{line_no}: empty required atom field")
            key = (engine, probe_id)
            maps.setdefault(key, set()).add(atom)
            engines.add(engine)
            probes.add(probe_id)
    frozen = {key: frozenset(value) for key, value in maps.items()}
    return frozen, tuple(sorted(engines)), tuple(sorted(probes))


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


def cmd_witnesses(args: argparse.Namespace) -> int:
    root = Path(args.root)
    cm = load_contract_maps(root / "artifact")
    rows = _witness_rows(cm.maps, cm.engines, cm.probes, args.projection, args.limit)
    _write_rows(rows, Path(args.output) if args.output else None)
    return 0


def cmd_audit_csv(args: argparse.Namespace) -> int:
    maps, engines, probes = _contract_maps_from_csv(Path(args.input))
    if args.mode == "metrics":
        rows = [equivalence_metrics(maps, engines, probes, projection).as_row() for projection in args.projection]
    else:
        rows = _witness_rows(maps, engines, probes, args.projection, args.limit)
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
    p_witnesses = sub.add_parser("witnesses", help="print projection-collision witness rows from the artifact")
    p_witnesses.add_argument("--projection", nargs="+", default=["keyword", "yesno", "operator_only"])
    p_witnesses.add_argument("--limit", type=int, default=20, help="maximum witnesses per projection")
    p_witnesses.add_argument("--output")
    p_witnesses.set_defaults(func=cmd_witnesses)
    p_audit_csv = sub.add_parser("audit-csv", help="audit a user CSV of public contract atoms")
    p_audit_csv.add_argument("--input", required=True, help="CSV with engine, probe_id, operator, kind, layer, placement, decision_time, observability, and optional variant/state")
    p_audit_csv.add_argument("--projection", nargs="+", default=["keyword", "yesno", "operator_only"])
    p_audit_csv.add_argument("--mode", choices=["metrics", "witnesses"], default="witnesses")
    p_audit_csv.add_argument("--limit", type=int, default=20, help="maximum witnesses per projection")
    p_audit_csv.add_argument("--output")
    p_audit_csv.set_defaults(func=cmd_audit_csv)
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
