#!/usr/bin/env python3
from pathlib import Path
from optsemc.workloads import WorkloadMotif, WorkloadSuite
from optsemc.domain import Probe
from optsemc.replay import default_replay_steps, replay_plan_rows
from optsemc.manifest import classify_path

def test_workload_replay_manifest_case_1_1():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_2():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_3():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_4():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_5():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_6():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_7():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_8():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_9():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_10():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_11():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_12():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_13():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_14():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_15():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_16():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_17():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_18():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_19():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_20():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_21():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_22():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_23():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_24():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_25():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_26():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_27():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_28():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_29():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_30():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_31():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_32():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_33():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_34():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_35():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_36():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_37():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_38():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_1_39():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

