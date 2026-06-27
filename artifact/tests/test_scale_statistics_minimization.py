#!/usr/bin/env python3
from optsemc.statistics import mean
from optsemc.minimization import minimal_by_inclusion

def test_extra_scale_case_1():
    values = [1, 2, 3]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_2():
    values = [2, 3, 4]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_3():
    values = [3, 4, 5]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_4():
    values = [4, 5, 6]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_5():
    values = [5, 6, 7]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_6():
    values = [6, 7, 8]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_7():
    values = [7, 8, 9]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_8():
    values = [8, 9, 10]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_9():
    values = [9, 10, 11]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_10():
    values = [10, 11, 12]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_11():
    values = [11, 12, 13]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_12():
    values = [12, 13, 14]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_13():
    values = [13, 14, 15]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_14():
    values = [14, 15, 16]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_15():
    values = [15, 16, 17]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_16():
    values = [16, 17, 18]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_17():
    values = [17, 18, 19]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_18():
    values = [18, 19, 20]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_19():
    values = [19, 20, 21]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_20():
    values = [20, 21, 22]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_21():
    values = [21, 22, 23]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_22():
    values = [22, 23, 24]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_23():
    values = [23, 24, 25]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_24():
    values = [24, 25, 26]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_25():
    values = [25, 26, 27]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_26():
    values = [26, 27, 28]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_27():
    values = [27, 28, 29]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_28():
    values = [28, 29, 30]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_29():
    values = [29, 30, 31]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_30():
    values = [30, 31, 32]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_31():
    values = [31, 32, 33]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_32():
    values = [32, 33, 34]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_33():
    values = [33, 34, 35]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_34():
    values = [34, 35, 36]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_35():
    values = [35, 36, 37]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_36():
    values = [36, 37, 38]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_37():
    values = [37, 38, 39]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_38():
    values = [38, 39, 40]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_39():
    values = [39, 40, 41]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_40():
    values = [40, 41, 42]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_41():
    values = [41, 42, 43]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_42():
    values = [42, 43, 44]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_43():
    values = [43, 44, 45]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_44():
    values = [44, 45, 46]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_45():
    values = [45, 46, 47]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_46():
    values = [46, 47, 48]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_47():
    values = [47, 48, 49]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_48():
    values = [48, 49, 50]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_49():
    values = [49, 50, 51]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_50():
    values = [50, 51, 52]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_51():
    values = [51, 52, 53]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_52():
    values = [52, 53, 54]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_53():
    values = [53, 54, 55]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_54():
    values = [54, 55, 56]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_55():
    values = [55, 56, 57]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_56():
    values = [56, 57, 58]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_57():
    values = [57, 58, 59]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_58():
    values = [58, 59, 60]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_59():
    values = [59, 60, 61]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_60():
    values = [60, 61, 62]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_61():
    values = [61, 62, 63]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_62():
    values = [62, 63, 64]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_63():
    values = [63, 64, 65]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_64():
    values = [64, 65, 66]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_65():
    values = [65, 66, 67]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_66():
    values = [66, 67, 68]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_67():
    values = [67, 68, 69]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_68():
    values = [68, 69, 70]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_69():
    values = [69, 70, 71]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_70():
    values = [70, 71, 72]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_71():
    values = [71, 72, 73]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_72():
    values = [72, 73, 74]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_73():
    values = [73, 74, 75]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_74():
    values = [74, 75, 76]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_75():
    values = [75, 76, 77]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_76():
    values = [76, 77, 78]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_77():
    values = [77, 78, 79]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_78():
    values = [78, 79, 80]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

def test_extra_scale_case_79():
    values = [79, 80, 81]
    assert mean(values) == sum(values) / len(values)
    mins = minimal_by_inclusion([{"a"}, {"a", "b"}, {"c"}])
    assert ("a",) in mins
    assert ("c",) in mins

