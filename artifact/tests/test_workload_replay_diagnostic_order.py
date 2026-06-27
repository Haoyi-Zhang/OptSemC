#!/usr/bin/env python3
from pathlib import Path
from optsemc.workloads import WorkloadMotif, WorkloadSuite
from optsemc.domain import Probe
from optsemc.replay import default_replay_steps, replay_plan_rows
from optsemc.manifest import classify_path

def test_workload_replay_manifest_case_2_1():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_2():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_3():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_4():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_5():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_6():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_7():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_8():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_9():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_10():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_11():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_12():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_13():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_14():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_15():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_16():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_17():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_18():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_19():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_20():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_21():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_22():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_23():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_24():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_25():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_26():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_27():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_28():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_29():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_30():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_31():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_32():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_33():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_34():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_35():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_36():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_37():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_38():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

def test_workload_replay_manifest_case_2_39():
    probe = Probe("P1", {"join_type":"inner", "join_shape":"star"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    motif = WorkloadMotif("M", {"join_type":"inner"})
    suite = WorkloadSuite("S", "suite", (motif,))
    assert motif.matches(probe)
    assert suite.coverage([probe])["covered_motifs"] == "1"
    assert replay_plan_rows(default_replay_steps())
    assert classify_path(Path("artifact/optsemc/semantics.py")) == "library-code"

