#!/usr/bin/env python3
from optsemc.domain import LineRange, ActionRecord, Probe
from optsemc.coverage import combinations_from_vector, interaction_key, motif_covered

def test_domain_coverage_case_1_1():
    lr = LineRange.parse("L1-L3")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_2():
    lr = LineRange.parse("L2-L4")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_3():
    lr = LineRange.parse("L3-L5")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_4():
    lr = LineRange.parse("L4-L6")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_5():
    lr = LineRange.parse("L5-L7")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_6():
    lr = LineRange.parse("L6-L8")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_7():
    lr = LineRange.parse("L7-L9")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_8():
    lr = LineRange.parse("L8-L10")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_9():
    lr = LineRange.parse("L9-L11")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_10():
    lr = LineRange.parse("L10-L12")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_11():
    lr = LineRange.parse("L11-L13")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_12():
    lr = LineRange.parse("L12-L14")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_13():
    lr = LineRange.parse("L13-L15")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_14():
    lr = LineRange.parse("L14-L16")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_15():
    lr = LineRange.parse("L15-L17")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_16():
    lr = LineRange.parse("L16-L18")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_17():
    lr = LineRange.parse("L17-L19")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_18():
    lr = LineRange.parse("L18-L20")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_19():
    lr = LineRange.parse("L19-L21")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_20():
    lr = LineRange.parse("L20-L22")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_21():
    lr = LineRange.parse("L21-L23")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_22():
    lr = LineRange.parse("L22-L24")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_23():
    lr = LineRange.parse("L23-L25")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_24():
    lr = LineRange.parse("L24-L26")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_25():
    lr = LineRange.parse("L25-L27")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_26():
    lr = LineRange.parse("L26-L28")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_27():
    lr = LineRange.parse("L27-L29")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_28():
    lr = LineRange.parse("L28-L30")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_29():
    lr = LineRange.parse("L29-L31")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_30():
    lr = LineRange.parse("L30-L32")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_31():
    lr = LineRange.parse("L31-L33")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_32():
    lr = LineRange.parse("L32-L34")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_33():
    lr = LineRange.parse("L33-L35")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_34():
    lr = LineRange.parse("L34-L36")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_35():
    lr = LineRange.parse("L35-L37")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_36():
    lr = LineRange.parse("L36-L38")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_37():
    lr = LineRange.parse("L37-L39")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_38():
    lr = LineRange.parse("L38-L40")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_39():
    lr = LineRange.parse("L39-L41")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_40():
    lr = LineRange.parse("L40-L42")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_41():
    lr = LineRange.parse("L41-L43")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_42():
    lr = LineRange.parse("L42-L44")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_43():
    lr = LineRange.parse("L43-L45")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

def test_domain_coverage_case_1_44():
    lr = LineRange.parse("L44-L46")
    assert lr.width == 3
    action = ActionRecord("Join", "reorder", "inner", "logical", "engine", "compile", "explain")
    assert action.key().count("|") == 6
    probe = Probe("P", {"join_type":"inner", "join_shape":"binary"}, "SELECT * FROM a JOIN b ON a.k=b.k")
    assert probe.feature_key() == (("join_shape", "binary"), ("join_type", "inner"))
    assert combinations_from_vector(probe.feature_vector, 1)
    assert motif_covered([probe], {"join_type":"inner"}) == (True, 1)

