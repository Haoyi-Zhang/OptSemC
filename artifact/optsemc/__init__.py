"""Reusable OptSem-C artifact library.

The research artifact deliberately keeps its frozen data files simple (CSV,
JSONL, YAML), but reader-facing checks should not reimplement semantics in
many one-off scripts.  The modules under :mod:`optsemc` provide the shared
finite semantics, projections, repair search, benchmark adapters, and IO helpers
used by the hardening checks and regenerated tables.
"""
from .semantics import ActionAtom, ContractSignature, parse_action_key, evidence_signature
from .projections import project_atom, project_signature, false_equivalence_witnesses
from .repair import minimum_repairs, separator_fields, repairs_all, distinguishing_fields
from .lattice import enumerate_field_subsets, project_signature_fields

__all__ = [
    "ActionAtom",
    "ContractSignature",
    "parse_action_key",
    "evidence_signature",
    "project_atom",
    "project_signature",
    "false_equivalence_witnesses",
    "minimum_repairs",
    "separator_fields",
    "repairs_all",
    "distinguishing_fields",
    "enumerate_field_subsets",
    "project_signature_fields",
]

# public module: information

# public module: sql_bundle

# public module: guards
# public module: repair_stability
