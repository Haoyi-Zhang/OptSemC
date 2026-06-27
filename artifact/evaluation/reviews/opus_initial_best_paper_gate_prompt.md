You are an independent external reviewer for a VLDB 2027 Regular Research submission and its companion artifact. Be skeptical and concrete. The goal is not "is this okay"; the goal is whether this repository could plausibly clear a best-paper-level research gate after iteration.

Project: OptSem-C: Public Optimizer Contracts for Query Engine Portability.

Current local project layout:
- Top level has only `Paper/` and `artifact/`.
- This folder is currently not a Git repository.
- `Paper/latex/paper.tex` uses `\documentclass[sigconf,nonacm]{acmart}` and targets PVLDB/VLDB 2027 Regular Research.
- VLDB Regular body budget is 12 body pages excluding references. This manuscript currently has a local compile certificate claiming 13 total pages with references starting on page 13.
- `artifact/` contains the Python package `optsemc`, scripts, tests, grounded data, generated probes, generated evaluation CSV/JSONL files, and reproducibility scripts.

Main research claims in the paper/artifact:
- Public optimizer behavior contracts are formalized as guarded modal rules over query features.
- Contract signatures include operator, action kind, variant, optimizer layer, placement, decision time, observability, state/modality, version/time window, and public evidence.
- Coarse optimizer comparisons are modeled as projections; false portability is the nontrivial projection kernel.
- Grounded corpus: 287 verified public-contract rules, 287 source-linked evidence spans, 26 public source records across PostgreSQL, Trino, BigQuery, Spark SQL, Snowflake, DuckDB, and ClickHouse.
- Benchmark: 4,216 generated SQL probes covering 7,112 valid optimizer-feature interactions.
- Projection results: keyword projection declares 2,284 equivalences, 254 false; operator-only declares 2,268 equivalences, 238 false; yes/no has 6 false.
- Repair claims: placement repairs keyword collisions, layer repairs operator-only collisions, and layer+placement repairs all 498 headline witnesses after excluding fine-grained variants.
- External motif crosswalk: 90/90 motifs across 12 optimizer/workload families are covered; one representative generated probe per motif executes.
- SQL validation: 12,648 probe-catalog executions over three deterministic catalogs report zero failures.

Important implementation facts and suspected risks:
- `artifact/run_mainline_checks.sh` mostly checks hygiene, package manifest, and frozen certificates. It does not recompute most experimental outputs.
- `artifact/run_deep_checks.sh` recomputes many outputs, runs SQL validation, external motif representative execution, claim checks, unit tests, and paper checks.
- `artifact/run_from_scratch_no_cache.sh` deletes selected derived outputs, recomputes grounded mainline, runs deep checks with `RUN_EXPENSIVE_RECOMPUTE=1 RUN_LATEX_COMPILE=1`, then runs the fast package checks.
- `artifact/scripts/execute_sql_probe_suite.py` runs generated SQL on `optsemc.sql_execution.SyntheticOptimizerCatalog`.
- `artifact/scripts/execute_sql_probe_suite_multicatalog.py` repeats generated SQL over synthetic catalog sizes 1, 5, and 17.
- `artifact/scripts/execute_external_motif_suite.py` chooses one matching generated probe for every external motif and executes it on the same synthetic catalog.
- There is no current evidence that TPC-H/TPC-DS/JOB/SSB/ClickBench original workloads are run, or that generated probes are executed on real PostgreSQL/DuckDB/ClickHouse/Trino/Spark engines.
- `artifact/evaluation/claim_metric_summary.csv` still includes an older-looking external benchmark row (`external_benchmark_motifs=5`, `external_benchmark_requirements=41`) while other current files and paper text say 90 motifs across 12 families.
- `artifact/pyproject.toml` has `version = "1.0.0"`, and several data objects use `version` fields, while the user requires a clean project with no public "version/final" framing.
- `Paper/latex/paper.tex` has placeholder DOI/pages (`XX.XX/XXX.XX`, `XXX-XXX`), an artifact URL pointing to `https://github.com/Haoyi-Zhang/OptSemC`, manual `thebibliography`, and very small bibliography font (`5.6pt`) plus negative item spacing.
- The paper and many tables use `\scriptsize`, `\setlength` float compression, and manual `\vspace` around artifact availability.
- `Paper/latex/refs.bib` exists, but `paper.tex` uses manual bibliography entries.
- Repository quality checks currently include scale-style gates such as Python LOC, number of scripts, number of modules/classes/functions, and file counts. These can be gamed and should not be treated as best-paper evidence.
- Tests include exact target assertions such as 287 rules, 4,216 probes, 90 motifs, and 12 suite rows. Exact integrity checks are useful, but they may look self-fulfilling unless paired with independent recomputation and provenance checks.
- Current top-level package gate expects only `Paper/` and `artifact/`; review outputs are being stored under `artifact/evaluation/reviews/` as generated review evidence.

Review tasks:
1. Give P0/P1/P2/P3 findings for code/artifact correctness, experimental design, novelty, construct validity, external baselines, reproducibility, project hygiene, and VLDB Regular paper readiness.
2. Be explicit about what must change before the work could credibly be called best-paper-level.
3. Identify which claims should be strengthened by new cloud experiments, and which claims should be weakened/reframed to avoid overclaiming.
4. Pay special attention to whether the synthetic SQL validation and external motif crosswalk are sufficient evidence for the paper's benchmark claims.
5. Pay special attention to whether the formal semantics and projection-kernel contribution is novel enough for VLDB Regular, or whether additional external comparisons/baselines are required.
6. Pay special attention to PVLDB formatting/compliance risks, including page budget, bibliography handling, placeholder metadata, artifact URL, single-blind author handling, and font/spacing hacks.
7. End with a concrete prioritized action plan and a "signoff conditions" checklist.

Output format:
- Start with an overall readiness verdict: BLOCKED / MAJOR REVISION / MINOR REVISION / SIGNOFF.
- Then list findings ordered by severity, each with: severity, title, affected files/claims, why it matters, exact required fix.
- Then give the prioritized action plan.
- Then give signoff conditions.
