from optsemc.domain import Probe
from optsemc.workloads import (
    WorkloadMotif,
    WorkloadSuite,
    representative_probe_set,
    suite_coverage_matrix,
    suite_depth_summary,
)


def _probes():
    return (
        Probe("P1", {"join_type": "inner", "join_shape": "star"}, "SELECT * FROM a JOIN b ON a.k=b.k"),
        Probe("P2", {"join_type": "left", "join_shape": "chain"}, "SELECT * FROM a LEFT JOIN b ON a.k=b.k"),
    )


def test_workload_motif_matches_exact_requirements_and_rejects_gaps():
    motif = WorkloadMotif("star-inner", {"join_type": "inner", "join_shape": "star"})
    assert motif.matches(_probes()[0])
    assert not motif.matches(_probes()[1])
    assert motif.matching_probe_ids(_probes()) == ("P1",)


def test_suite_coverage_counts_covered_motifs_and_hits():
    suite = WorkloadSuite(
        "S",
        "synthetic",
        (
            WorkloadMotif("m1", {"join_type": "inner"}),
            WorkloadMotif("m2", {"join_shape": "missing"}),
        ),
    )
    coverage = suite.coverage(_probes())
    assert coverage["motifs"] == "2"
    assert coverage["covered_motifs"] == "1"
    assert coverage["coverage_rate"] == "0.500000"
    assert suite.gaps(_probes())[0].motif_id == "m2"


def test_coverage_matrix_records_requirements_and_examples():
    suite = WorkloadSuite("S", "synthetic", (WorkloadMotif("m1", {"join_shape": "star"}),))
    rows = suite_coverage_matrix((suite,), _probes())
    assert rows == [
        {
            "suite_id": "S",
            "suite_name": "synthetic",
            "motif_id": "m1",
            "requirements": "join_shape=star",
            "covered": "true",
            "matching_probes": "1",
            "example_probe": "P1",
        }
    ]


def test_depth_summary_and_representative_probe_set_are_deterministic():
    suite = WorkloadSuite(
        "S",
        "synthetic",
        (
            WorkloadMotif("inner", {"join_type": "inner"}),
            WorkloadMotif("any-star", {"join_shape": "star"}),
        ),
    )
    summary = suite_depth_summary((suite,), _probes())[0]
    representatives = representative_probe_set((suite,), _probes())
    assert summary["min_hits"] == "1"
    assert summary["max_hits"] == "1"
    assert [row["probe_id"] for row in representatives] == ["P1", "P1"]
