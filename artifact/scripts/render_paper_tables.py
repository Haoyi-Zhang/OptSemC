#!/usr/bin/env python3
"""Render LaTeX tables used by the OptSem-C paper draft from evaluation CSVs."""
from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT.parent / "paper" / "latex" / "tables"
PAPER.mkdir(parents=True, exist_ok=True)
ROW_END = r" \\"  # LaTeX row terminator

def rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def esc(s):
    s = str(s)
    return (s.replace('\\','\\textbackslash{}').replace('&','\\&').replace('%','\\%')
             .replace('$','\\$').replace('#','\\#').replace('_','\\_')
             .replace('{','\\{').replace('}','\\}'))

def write(name, lines):
    (PAPER / name).write_text("\n".join(lines)+"\n", encoding='utf-8')

def fmt_int(x):
    return f"{int(x):,}"

cov = rows(ROOT/'evaluation/contract_coverage.csv')
extr = {r['engine']:r for r in rows(ROOT/'evaluation/contract_extraction.csv')}
lines=[r"\begin{table}[t]",r"\centering",r"\caption{Public-contract extraction and trigger coverage by engine.}",r"\label{tab:contract-denominator}",r"\begin{tabular}{lrrrr}",r"\toprule", "Engine & Rules & Triggered & Dims & Coverage" + ROW_END, r"\midrule"]
for r in cov:
    dims=extr.get(r['engine'],{}).get('dimensions','--')
    lines.append(f"{esc(r['engine'])} & {r['rules_total']} & {r['rules_triggered']} & {dims} & {float(r['contract_coverage']):.2f}" + ROW_END)
lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
write('tab_contract_denominator.tex',lines)

coverage = rows(ROOT/'evaluation/coverage_interactions.csv')
pair=[r for r in coverage if r['arity']=='2']
three=[r for r in coverage if r['arity']=='3']
allr=[r for r in coverage if r['coverage_target']=='ALL'][0]
lines=[r"\begin{table}[t]",r"\centering",r"\caption{OptSemBench-C coverage summary.}",r"\label{tab:benchmark-coverage}",r"\begin{tabular}{lrr}",r"\toprule", "Coverage class & Targets & Valid interactions" + ROW_END, r"\midrule",
       f"Global pairwise & {len(pair)} & {sum(int(r['valid_interactions']) for r in pair)}" + ROW_END,
       f"Selected 3-wise & {len(three)} & {sum(int(r['valid_interactions']) for r in three)}" + ROW_END,
       f"All unique interactions & -- & {allr['total_unique_interactions']}" + ROW_END,
       f"Generated probes & -- & {allr['generated_probes']}" + ROW_END,
       r"\bottomrule",r"\end{tabular}",r"\end{table}"]
write('tab_benchmark_coverage.tex',lines)

trap=rows(ROOT/'evaluation/trap_rate.csv')
lines=[r"\begin{table}[t]",r"\centering",r"\caption{False-equivalence rate of lossy optimizer-comparison baselines.}",r"\label{tab:trap-rate}",r"\begin{tabular}{lrrr}",r"\toprule", "Method & Comparisons & False equiv. & Trap rate" + ROW_END, r"\midrule"]
for r in trap:
    lines.append(f"{esc(r['method'])} & {fmt_int(r['comparisons'])} & {fmt_int(r['false_equivalence'])} & {float(r['trap_rate']):.4f}" + ROW_END)
lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
write('tab_trap_rate.tex',lines)

fc=rows(ROOT/'evaluation/field_collision.csv')
lines=[r"\begin{table}[t]",r"\centering",r"\caption{Action-level semantic collisions caused by lossy projections.}",r"\label{tab:field-collision}",r"\begin{tabular}{lrrr}",r"\toprule", "Variant & Action pairs & Collisions & Collision rate" + ROW_END, r"\midrule"]
for r in fc:
    lines.append(f"{esc(r['variant'])} & {fmt_int(r['action_pairs'])} & {fmt_int(r['action_collisions'])} & {float(r['collision_rate']):.6f}" + ROW_END)
lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
write('tab_field_collision.tex',lines)

sens=sorted(rows(ROOT/'evaluation/workload_sensitivity.csv'), key=lambda r: float(r['mean_distance']), reverse=True)[:12]
lines=[r"\begin{table*}[t]",r"\centering",r"\caption{Largest workload-feature-induced contract movements.}",r"\label{tab:workload-sensitivity}",r"\begin{tabular}{llrrr}",r"\toprule", "Engine & Feature & Groups & Mean dist. & Nonzero frac." + ROW_END, r"\midrule"]
for r in sens:
    lines.append(f"{esc(r['engine'])} & {esc(r['feature'])} & {fmt_int(r['groups'])} & {float(r['mean_distance']):.3f} & {float(r['nonzero_fraction']):.3f}" + ROW_END)
lines += [r"\bottomrule",r"\end{tabular}",r"\end{table*}"]
write('tab_workload_sensitivity.tex',lines)


# Compatibility hierarchy table (projection sensitivity).
try:
    comp = [r for r in rows(ROOT/'evaluation/compatibility_hierarchy.csv') if r['engine_i']=='ALL' and r['engine_j']=='ALL']
    lines=[r"\begin{table}[t]",r"\centering",r"\caption{Mean cross-engine compatibility under increasingly lossy projections.}",r"\label{tab:compatibility-hierarchy}",r"\begin{tabular}{lrr}",r"\toprule", "Projection & Mean & Median" + ROW_END, r"\midrule"]
    for r in comp:
        lines.append(f"{esc(r['projection'])} & {float(r['mean']):.3f} & {float(r['median']):.3f}" + ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
    write('tab_compatibility_hierarchy.tex', lines)
except FileNotFoundError:
    pass

# Contract state distribution table.
try:
    sd=rows(ROOT/'evaluation/state_distribution.csv')
    lines=[r"\begin{table}[t]",r"\centering",r"\caption{Contract-state distribution by engine.}",r"\label{tab:state-distribution}",r"\begin{tabular}{lrrrr}",r"\toprule", r"Engine & Rules & MUST & MAY & MUST\_NOT" + ROW_END, r"\midrule"]
    for r in sd:
        lines.append(f"{esc(r['engine'])} & {r['total_rules']} & {r['must']} & {r['may']} & {r['must_not']}" + ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
    write('tab_state_distribution.tex', lines)
except FileNotFoundError:
    pass

# Artifact snapshot is derived from artifact outputs, not hard-coded.
def line_count(path):
    try:
        with open(path, encoding='utf-8') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return 0
source_records = max(0, line_count(ROOT/'corpus/sources.csv')-1)
evidence_segments = line_count(ROOT/'extraction/evidence_segments.jsonl')
accepted_rules = line_count(ROOT/'extraction/accepted_rules.jsonl')
generated_probes = line_count(ROOT/'benchmark/generated_probes.jsonl')
contract_maps = line_count(ROOT/'evaluation/contract_maps.jsonl')
merge_conflicts = line_count(ROOT/'evaluation/conflicts.jsonl')
try:
    audit_summary=rows(ROOT/'evaluation/rule_audit_summary.csv')
    audit_issues = audit_summary[0].get('rules_with_issues','0') if audit_summary else '0'
except Exception:
    audit_issues='--'
summary = [('Public source records',fmt_int(source_records)),('Frozen evidence segments',fmt_int(evidence_segments)),('Accepted contract rules',fmt_int(accepted_rules)),('Generated query probes',fmt_int(generated_probes)),('Contract maps',fmt_int(contract_maps)),('Merge conflicts',fmt_int(merge_conflicts)),('Rule audit issues',audit_issues)]
lines=[r"\begin{table}[t]",r"\centering",r"\caption{OptSem-C artifact snapshot used by this draft.}",r"\label{tab:artifact-snapshot}",r"\begin{tabular}{lr}",r"\toprule", "Quantity & Value"+ROW_END, r"\midrule"]
for k,v in summary:
    lines.append(f"{esc(k)} & {v}" + ROW_END)
lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
write('tab_artifact_snapshot.tex', lines)
print(f"Rendered tables to {PAPER}")

# Provenance audit summary: issues and evidence support composition.
try:
    prov = rows(ROOT/'evaluation/provenance_summary.csv')
    total_rules = next((r['count'] for r in prov if r['category']=='total' and r['name']=='rules'), '0')
    issue_rows = [r for r in prov if r['category']=='issue']
    source_rows = [r for r in prov if r['category']=='by_source_class']
    lines=[r"\begin{table}[t]",r"\centering",r"\caption{Rule-to-evidence provenance audit.}",r"\label{tab:provenance-audit}",r"\begin{tabular}{lr}",r"\toprule", "Check & Count"+ROW_END, r"\midrule", f"Accepted rules with provenance rows & {fmt_int(total_rules)}"+ROW_END]
    if issue_rows:
        for r in issue_rows: lines.append(f"{esc(r['name'])} & {fmt_int(r['count'])}"+ROW_END)
    else:
        lines.append("Provenance link issues & 0"+ROW_END)
    for r in source_rows:
        lines.append(f"Rules from {esc(r['name'])} evidence & {fmt_int(r['count'])}"+ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
    write('tab_provenance_audit.tex', lines)
except FileNotFoundError:
    pass

# Semantic-audit table: finite-state checks and corpus consistency.
try:
    sa = rows(ROOT/'evaluation/semantics_audit.csv')
    sj = rows(ROOT/'evaluation/state_join_properties.csv')
    passed_props = sum(1 for r in sj if r.get('passed')=='true')
    total_props = len(sj)
    lines=[r"\begin{center}",r"\small",r"\textbf{Semantics audit.}\par\vspace{0.3em}",r"\begin{tabular}{lr}",r"\toprule", "Check & Result"+ROW_END, r"\midrule",
           f"State-join properties & {passed_props}/{total_props} passed"+ROW_END]
    for r in sa:
        lines.append(f"{esc(r['check'])} & {esc(r['value'])}"+ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{center}"]
    write('tab_semantics_audit.tex', lines)
except FileNotFoundError:
    pass

# Projection-loss witnesses: compact representative witnesses.
try:
    pw = rows(ROOT/'evaluation/projection_loss_witnesses.csv')[:8]
    lines=[r"\begin{table*}[t]",r"\centering",r"\caption{Corpus-backed projection-loss witnesses. Each row shows two distinct rules that collapse under a lossy projection.}",r"\label{tab:projection-witnesses}",r"\small",r"\begin{tabular}{lllll}",r"\toprule", "Projection & Rule left & Rule right & Engines & Differing fields"+ROW_END, r"\midrule"]
    for r in pw:
        engines = r['engine_left'] if r['engine_left']==r['engine_right'] else r['engine_left']+' / '+r['engine_right']
        lines.append(f"{esc(r['projection'])} & {esc(r['rule_left'])} & {esc(r['rule_right'])} & {esc(engines)} & {esc(r['differing_fields'])}"+ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table*}"]
    write('tab_projection_witnesses.tex', lines)
except FileNotFoundError:
    pass

# Dimension/action-field coverage by engine.
try:
    dc = rows(ROOT/'evaluation/dimension_coverage_by_engine.csv')
    lines=[r"\begin{table*}[t]",r"\centering",r"\caption{Action-field diversity by engine in the accepted contract corpus.}",r"\label{tab:dimension-coverage}",r"\small",r"\begin{tabular}{lrrrrrrrr}",r"\toprule", "Engine & Rules & Sources & Ops & Kinds & Variants & Placements & Times & Obs."+ROW_END, r"\midrule"]
    for r in dc:
        lines.append(f"{esc(r['engine'])} & {r['rules']} & {r['sources']} & {r['operator_values']} & {r['kind_values']} & {r['variant_values']} & {r['placement_values']} & {r['decision_time_values']} & {r['observability_values']}"+ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table*}"]
    write('tab_dimension_coverage.tex', lines)
except FileNotFoundError:
    pass

# Integrity suite table.
try:
    ints = rows(ROOT/'evaluation/integrity_suite.csv')
    lines=[r"\begin{table}[t]",r"\centering",r"\caption{Executable artifact integrity suite.}",r"\label{tab:integrity-suite}",r"\small",r"\begin{tabular}{ll}",r"\toprule", "Check & Result"+ROW_END, r"\midrule"]
    for r in ints:
        result = 'pass' if r.get('passed')=='true' else 'fail'
        lines.append(f"{esc(r['check'])} & {esc(result)}"+ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
    write('tab_integrity_suite.tex', lines)
except FileNotFoundError:
    pass

# Paper-alignment and reproducibility tables.
try:
    sr = rows(ROOT/'evaluation/paper_alignment.csv')
    passed = sum(1 for r in sr if r.get('passed')=='true')
    failed = len(sr) - passed
    bycrit = {r['criterion']:r for r in sr}
    compact = [
        ('Alignment criteria', f'{passed}/{len(sr)} passed'),
        ('Accepted rules', bycrit.get('accepted_contract_rules',{}).get('value','--')),
        ('Generated probes', bycrit.get('generated_query_probes',{}).get('value','--')),
        ('Valid interactions', bycrit.get('valid_feature_interactions',{}).get('value','--')),
        ('Merge conflicts', bycrit.get('contract_merge_conflicts',{}).get('value','--')),
        ('Table-source failures', bycrit.get('paper_table_source_check',{}).get('value','--')),
    ]
    lines=[r"\begin{table}[t]",r"\centering",r"\caption{Paper-alignment summary for the measurement snapshot.}",r"\label{tab:paper-alignment}",r"\begin{tabular}{lr}",r"\toprule", "Gate & Value"+ROW_END, r"\midrule"]
    for k,v in compact:
        lines.append(f"{esc(k)} & {esc(v)}"+ROW_END)
    lines += [r"\bottomrule",r"\end{tabular}",r"\end{table}"]
    write('tab_paper_alignment.tex', lines)
except FileNotFoundError:
    pass

try:
    rm = {r['metric']:r['value'] for r in rows(ROOT/'evaluation/reproducibility_manifest_summary.csv')}
    pts = {r['metric']:r['value'] for r in rows(ROOT/'evaluation/paper_table_source_check_summary.csv')}
    lines=[r"\begin{table}[t]",r"\centering",r"\caption{Reproducibility manifest and paper-table source check.}",r"\label{tab:repro-manifest}",r"\begin{tabular}{lr}",r"\toprule", "Check & Value"+ROW_END, r"\midrule",
           f"Checksummed files & {fmt_int(rm.get('files','0'))}"+ROW_END,
           f"Manifest bytes & {fmt_int(rm.get('total_bytes','0'))}"+ROW_END,
           f"Hash algorithm & {esc(rm.get('sha256_algorithm','SHA-256'))}"+ROW_END,
           f"Paper tables checked & {fmt_int(pts.get('tables','0'))}"+ROW_END,
           f"Paper table source failures & {fmt_int(pts.get('failed','0'))}"+ROW_END,
           r"\bottomrule",r"\end{tabular}",r"\end{table}"]
    write('tab_repro_manifest.tex', lines)
except FileNotFoundError:
    pass
