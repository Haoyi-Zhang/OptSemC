"""Baseline and ablation definitions for public optimizer-contract comparison."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BaselineSpec:
    baseline_id: str
    projection: str
    comparison_object: str
    erased_semantics: str
    expected_failure_mode: str


BASELINES: tuple[BaselineSpec, ...] = (
    BaselineSpec(
        "B0-exact-contract",
        "strict",
        "Full evidence atom: operator, kind, variant, layer, placement, decision time, observability, modality",
        "None",
        "Negative control; no false equivalence when exact signatures match the semantics",
    ),
    BaselineSpec(
        "B1-keyword-matrix",
        "keyword",
        "Feature-name checklist such as pushdown=yes or adaptivity=yes",
        "Operator, variant, layer, placement, decision time, observability, and modality",
        "Fabricates equivalence between local rewrite, source delegation, pruning, and runtime behavior",
    ),
    BaselineSpec(
        "B2-yes-no-operator-kind",
        "yesno",
        "Operator/action-kind yes/no matrix",
        "Variant, layer, placement, decision time, observability, and modality",
        "Conflates supported behavior with different public execution placement or planning layer",
    ),
    BaselineSpec(
        "B3-operator-only",
        "operator_only",
        "Native plan-operator-name comparison",
        "Kind, variant, layer, placement, decision time, observability, and modality",
        "Treats logical, physical, delegated, and runtime evidence as the same operator object",
    ),
    BaselineSpec(
        "B4-placement-ablated",
        "no_placement",
        "Full contract without execution placement",
        "Placement",
        "Ablation control for source delegation versus local or distributed execution",
    ),
    BaselineSpec(
        "B5-decision-time-ablated",
        "no_decision_time",
        "Full contract without decision time",
        "Decision time",
        "Ablation control for compile-time, stage-boundary, runtime, and profile-time evidence",
    ),
    BaselineSpec(
        "B6-observability-ablated",
        "no_observability",
        "Full contract without plan-observability surface",
        "Observability",
        "Ablation control for logical, physical, runtime-profile, and stage-graph evidence",
    ),
    BaselineSpec(
        "B7-modality-ablated",
        "no_modality",
        "Full contract with supported states collapsed to evidenced=yes",
        "MUST/MAY/MUST_NOT distinction",
        "Ablation control for modal public commitments",
    ),
    BaselineSpec(
        "B8-kind-only",
        "kind_only",
        "Action-kind token comparison such as pushdown, observe, reorder, adapt",
        "Operator, variant, layer, placement, decision time, observability, and modality",
        "Tests whether keyword results are robust to using action-kind rather than synonym-normalized feature labels",
    ),
    BaselineSpec(
        "B9-layer-only",
        "layer_only",
        "Optimizer-layer checklist",
        "Operator, kind, variant, placement, decision time, observability, and modality",
        "Conflates distinct actions that happen at the same logical/physical/runtime layer",
    ),
    BaselineSpec(
        "B10-placement-only",
        "placement_only",
        "Execution-placement checklist",
        "Operator, kind, variant, layer, decision time, observability, and modality",
        "Conflates different optimizer actions merely because they execute locally, in a source, or in a distributed service",
    ),
    BaselineSpec(
        "B11-observability-only",
        "observability_only",
        "Plan-surface checklist",
        "Operator, kind, variant, layer, placement, decision time, and modality",
        "Conflates behavior when only the public evidence surface is compared",
    ),
    BaselineSpec(
        "B12-decision-time-only",
        "decision_time_only",
        "Decision-time checklist",
        "Operator, kind, variant, layer, placement, observability, and modality",
        "Conflates different optimizer actions that are compile-time, runtime, or profile-time exposed",
    ),
    BaselineSpec(
        "B13-state-only",
        "state_only",
        "Modal-state checklist",
        "Operator, kind, variant, layer, placement, decision time, and observability",
        "Conflates unrelated optimizer actions because they are all documented as MAY or MUST_NOT",
    ),
    BaselineSpec(
        "B14-operator-kind-layer",
        "operator_kind_layer",
        "Operator/action/layer matrix",
        "Variant, placement, decision time, observability, and modality",
        "Strengthened matrix baseline that still omits source delegation and plan-surface differences",
    ),
    BaselineSpec(
        "B15-operator-kind-placement",
        "operator_kind_placement",
        "Operator/action/placement matrix",
        "Variant, layer, decision time, observability, and modality",
        "Strengthened matrix baseline that still omits optimizer-layer and plan-surface differences",
    ),
    BaselineSpec(
        "B16-operator-kind-surface",
        "operator_kind_surface",
        "Operator/action/layer/placement/observability matrix",
        "Variant, decision time, and modality",
        "High-information public matrix baseline close to the full contract but without fine-grained variant or modality",
    ),
)
