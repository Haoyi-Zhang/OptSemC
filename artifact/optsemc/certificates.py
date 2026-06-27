"""Proof-carrying finite certificates for OptSem-C artifact claims."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from .domain import canonical_json, sha256_text
from .lattice import evaluate_lattice, minimum_hitting_sets, subset_key
from .projections import project_signature
from .repair import separator_fields
from .semantics import ContractSignature

Witness = tuple[str, str, tuple[str, str], tuple[str, str]]


def stable_key(key: tuple[str, str]) -> str:
    return f"{key[0]}::{key[1]}"


def witness_to_dict(witness: Witness) -> dict[str, Any]:
    method, probe, left, right = witness
    return {"projection": method, "probe_id": probe, "left": stable_key(left), "right": stable_key(right)}


@dataclass(frozen=True)
class CertificateHeader:
    """Common metadata for proof-carrying repository certificates."""

    certificate_id: str
    version: str
    inputs: Mapping[str, str]
    produced_by: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "version": self.version,
            "inputs": dict(sorted(self.inputs.items())),
            "produced_by": self.produced_by,
        }


@dataclass(frozen=True)
class ProjectionLossCertificate:
    """Certificate that every listed witness is exact-unequal and projection-equal."""

    header: CertificateHeader
    projection: str
    witnesses: tuple[dict[str, Any], ...]
    witness_hash: str

    @classmethod
    def build(
        cls,
        header: CertificateHeader,
        projection: str,
        witnesses: Sequence[Witness],
        maps: Mapping[tuple[str, str], ContractSignature],
        *,
        sample_limit: int = 100,
    ) -> "ProjectionLossCertificate":
        rows: list[dict[str, Any]] = []
        for witness in witnesses[:sample_limit]:
            method, probe, left, right = witness
            left_sig = maps[left]
            right_sig = maps[right]
            projected_equal = project_signature(left_sig, method) == project_signature(right_sig, method)
            exact_unequal = left_sig != right_sig
            rows.append({
                **witness_to_dict(witness),
                "exact_unequal": exact_unequal,
                "projected_equal": projected_equal,
                "left_signature_size": len(left_sig),
                "right_signature_size": len(right_sig),
            })
        return cls(header, projection, tuple(rows), sha256_text(canonical_json([witness_to_dict(w) for w in witnesses])))

    def verify(self) -> tuple[bool, tuple[str, ...]]:
        issues = []
        for row in self.witnesses:
            if not row.get("exact_unequal"):
                issues.append(f"not exact-unequal: {row}")
            if not row.get("projected_equal"):
                issues.append(f"not projection-equal: {row}")
        return not issues, tuple(issues)

    def as_dict(self) -> dict[str, Any]:
        return {
            "header": self.header.as_dict(),
            "projection": self.projection,
            "witness_count_sampled": len(self.witnesses),
            "witness_hash": self.witness_hash,
            "witnesses": list(self.witnesses),
        }


@dataclass(frozen=True)
class FrontierCertificate:
    """Certificate for a finite field-lattice repair frontier."""

    header: CertificateHeader
    scope: str
    universe: tuple[str, ...]
    witness_count: int
    safe_sets: tuple[str, ...]
    unsafe_sets: tuple[str, ...]
    minimum_safe_sets: tuple[str, ...]
    maximal_unsafe_sets: tuple[str, ...]
    monotone: bool

    @classmethod
    def build(
        cls,
        header: CertificateHeader,
        scope: str,
        witnesses: Sequence[Witness],
        maps: Mapping[tuple[str, str], ContractSignature],
        universe: Sequence[str],
    ) -> "FrontierCertificate":
        summary = evaluate_lattice(witnesses, maps, universe)
        return cls(
            header=header,
            scope=scope,
            universe=tuple(universe),
            witness_count=len(witnesses),
            safe_sets=tuple(point.label for point in summary.safe_points),
            unsafe_sets=tuple(point.label for point in summary.unsafe_points),
            minimum_safe_sets=tuple(point.label for point in summary.minimum_safe_points),
            maximal_unsafe_sets=tuple(point.label for point in summary.maximal_unsafe_points),
            monotone=not summary.monotonicity_violations(),
        )

    def verify(self) -> tuple[bool, tuple[str, ...]]:
        issues = []
        if not self.monotone:
            issues.append("frontier is not monotone")
        if self.witness_count and not self.minimum_safe_sets:
            issues.append("nonempty witness set has no safe repair")
        if set(self.safe_sets) & set(self.unsafe_sets):
            issues.append("field set listed as both safe and unsafe")
        return not issues, tuple(issues)

    def as_dict(self) -> dict[str, Any]:
        return {
            "header": self.header.as_dict(),
            "scope": self.scope,
            "universe": list(self.universe),
            "witness_count": self.witness_count,
            "safe_sets": list(self.safe_sets),
            "unsafe_sets": list(self.unsafe_sets),
            "minimum_safe_sets": list(self.minimum_safe_sets),
            "maximal_unsafe_sets": list(self.maximal_unsafe_sets),
            "monotone": self.monotone,
        }


@dataclass(frozen=True)
class HittingSetCertificate:
    """Dual certificate for minimum universal repair via separators."""

    header: CertificateHeader
    scope: str
    universe: tuple[str, ...]
    witness_count: int
    minimum_hitting_sets: tuple[str, ...]
    empty_separator_count: int
    separator_hash: str

    @classmethod
    def build(
        cls,
        header: CertificateHeader,
        scope: str,
        witnesses: Sequence[Witness],
        maps: Mapping[tuple[str, str], ContractSignature],
        universe: Sequence[str],
    ) -> "HittingSetCertificate":
        separators = []
        empty = 0
        for method, _probe, left, right in witnesses:
            sep = separator_fields(method, maps[left], maps[right], universe)
            if not sep:
                empty += 1
            separators.append(tuple(sorted(sep)))
        hits = tuple(subset_key(item) for item in minimum_hitting_sets(separators, universe))
        return cls(
            header=header,
            scope=scope,
            universe=tuple(universe),
            witness_count=len(witnesses),
            minimum_hitting_sets=hits,
            empty_separator_count=empty,
            separator_hash=sha256_text(canonical_json(separators)),
        )

    def verify(self) -> tuple[bool, tuple[str, ...]]:
        issues: list[str] = []
        if self.empty_separator_count:
            issues.append(f"{self.empty_separator_count} witnesses have no singleton separator")
        if self.witness_count and not self.minimum_hitting_sets:
            issues.append("no minimum hitting set reported")
        return not issues, tuple(issues)

    def as_dict(self) -> dict[str, Any]:
        return {
            "header": self.header.as_dict(),
            "scope": self.scope,
            "universe": list(self.universe),
            "witness_count": self.witness_count,
            "minimum_hitting_sets": list(self.minimum_hitting_sets),
            "empty_separator_count": self.empty_separator_count,
            "separator_hash": self.separator_hash,
        }


@dataclass(frozen=True)
class CertificateBundle:
    """A deterministic set of proof-carrying certificates."""

    certificates: tuple[Mapping[str, Any], ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "certificate_count": len(self.certificates),
            "bundle_hash": sha256_text(canonical_json(list(self.certificates))),
            "certificates": list(self.certificates),
        }

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_bundle(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_bundle(path: Path) -> tuple[bool, tuple[str, ...]]:
    data = read_bundle(path)
    issues: list[str] = []
    certificates = data.get("certificates") or []
    if data.get("certificate_count") != len(certificates):
        issues.append("certificate_count mismatch")
    expected = sha256_text(canonical_json(certificates))
    if data.get("bundle_hash") != expected:
        issues.append("bundle_hash mismatch")
    for cert in certificates:
        if not cert.get("header", {}).get("certificate_id"):
            issues.append("certificate without id")
        if cert.get("monotone") is False:
            issues.append(f"non-monotone certificate {cert.get('scope')}")
        if cert.get("empty_separator_count", 0):
            issues.append(f"empty separators in {cert.get('scope')}")
    return not issues, tuple(issues)

