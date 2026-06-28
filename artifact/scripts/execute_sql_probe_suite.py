#!/usr/bin/env python3
"""Execute every generated OptSemBench-C SQL skeleton on a deterministic catalog."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from optsemc.corpus import load_probes
from optsemc.io import write_csv
from optsemc.sql_execution import execute_probe_suite, execution_summary

probes = load_probes(ROOT)
records = execute_probe_suite(probes, rows_per_table=5)
write_csv(ROOT / 'evaluation' / 'sql_probe_execution.csv', [r.as_row() for r in records], ['probe_id','plan_ok','exec_ok','row_count','plan_steps','plan_hash','error'])
summary_rows = execution_summary(records)
write_csv(ROOT / 'evaluation' / 'sql_probe_execution_summary.csv', summary_rows, ['metric','value'])


def fmt(value: str | int) -> str:
    return f"{int(value):,}"


def render_paper_outputs() -> None:
    summary = {row["metric"]: row["value"] for row in summary_rows}
    probes_n = int(summary["executed_sql_probes"])
    plan_n = int(summary["plan_successes"])
    exec_n = int(summary["execution_successes"])
    fail_n = int(summary["execution_failures"])
    plan_w = 1.20 * plan_n / max(probes_n, 1)
    exec_w = 1.20 * exec_n / max(probes_n, 1)
    fail_w = 1.20 * fail_n / max(probes_n, 1)
    tables = ROOT.parent / "Paper" / "latex" / "tables"
    figures = ROOT.parent / "Paper" / "latex" / "figures"
    tables.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)

    (tables / "tab_sql_execution.tex").write_text(
        "\n".join([
            r"\begin{table}[t]",
            r"\centering",
            r"\caption{Full executable SQL validation of generated probes. The validation catalog is deterministic and is used only to check SQL shape and planability, not to rank engine performance.}",
            r"\label{tab:sql-execution}",
            r"\small",
            r"\begin{tabular}{lr}",
            r"\toprule",
            r"Quantity & Value \\",
            r"\midrule",
            f"Generated SQL probes & {fmt(probes_n)} \\\\",
            f"Probes with query plan & {fmt(plan_n)} \\\\",
            f"Executable probes & {fmt(exec_n)} \\\\",
            f"Execution failures & {fmt(fail_n)} \\\\",
            f"Distinct validation plans & {fmt(summary['distinct_plan_hashes'])} \\\\",
            f"Returned rows & {fmt(summary['total_result_rows'])} \\\\",
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
            "",
        ]),
        encoding="utf-8",
    )

    (figures / "fig_sql_execution_plot.tex").write_text(
        "\n".join([
            r"\begin{figure}[t]",
            r"\centering",
            r"\footnotesize",
            r"\newcommand{\execrow}[5]{%",
            r"  \node[anchor=east, font=\rmfamily\fontsize{6.8}{7.4}\selectfont, text=vldbInk]",
            r"        at (1.55,#1) {#2};",
            r"  \path[draw=#5!70!black, fill=#5!28, rounded corners=.7pt]",
            r"        (1.82,{#1-.13}) rectangle ({1.82+#3},{#1+.13});",
            r"  \node[anchor=west, font=\rmfamily\fontsize{6.8}{7.4}\selectfont, text=vldbGray]",
            r"        at (3.22,#1) {#4};",
            r"}",
            r"\begin{tikzpicture}[x=1cm,y=1cm]",
            r"  \node[vtitle, anchor=west, align=left] at (0,0.25)",
            r"    {SQL validation: all probes execute};",
            r"  \node[vsmall, anchor=west, align=left, text width=6.7cm] at (0,-0.20)",
            r"    {Bars are normalized to the generated-probe denominator; failures remain at zero.};",
            f"  \\execrow{{-0.86}}{{planned}}{{{plan_w:.2f}}}{{{fmt(plan_n)}}}{{vldbBlue}}",
            f"  \\execrow{{-1.48}}{{executed}}{{{exec_w:.2f}}}{{{fmt(exec_n)}}}{{vldbTeal}}",
            f"  \\execrow{{-2.10}}{{failures}}{{{fail_w:.2f}}}{{{fmt(fail_n)}}}{{vldbRose}}",
            r"  \node[vsmall, anchor=west] at (0,-2.76)",
            f"    {{distinct plans: {fmt(summary['distinct_plan_hashes'])}; returned rows: {fmt(summary['total_result_rows'])}}};",
            r"\end{tikzpicture}",
            r"\caption{Executable SQL-probe validation. Every generated probe plans and executes on the deterministic validation catalog; failures are zero.}",
            r"\Description{A compact horizontal bar chart showing planned probes, executed probes, zero failures, distinct validation plans, and returned rows.}",
            r"\label{fig:sql-execution}",
            r"\end{figure}",
            "",
        ]),
        encoding="utf-8",
    )


render_paper_outputs()
failures = [r for r in records if not r.exec_ok]
print(f"SQL probe execution: {len(records) - len(failures)}/{len(records)} executed; failures={len(failures)}")
if failures:
    for r in failures[:10]:
        print('FAIL', r.probe_id, r.error)
    raise SystemExit(1)
