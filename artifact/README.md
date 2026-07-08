# OptSemC Artifact

OptSemC evaluates public query-optimizer behavior contracts, not hidden implementation behavior or runtime latency. This directory is the public replay package: it contains the grounded corpus, benchmark probe generator, generated probes, reusable Python package, checks, tests, and reproducibility outputs needed to inspect the claims.

The manuscript source is intentionally outside the anonymous replay archive. The replay package is sufficient to rebuild the corpus, derived tables, SQL bundles, and integrity reports; manuscript compilation is a separate paper-build gate in the development repository.

## Archive verification

The public anonymous replay package is archived under the stable Zenodo concept record https://doi.org/10.5281/zenodo.21251442. The paper, repository README, and Zenodo landing page identify the current version DOI and external SHA-256 digest. The zip does not embed its version DOI or digest, so the package is not self-referential. Verify a downloaded archive by comparing the external digest with:

```bash
sha256sum optsemc-artifact.zip
```

The archive records its source-tree certificate in `artifact/evaluation/git_tree_state.csv`. If replay code, grounded corpus inputs, generated-probe logic, validation scripts, or paper-facing evidence changes, the archive gate requires rebuilding from a source tree with no pending edits and updating the external digest in the repository README and PVLDB availability block.

## Main research objects

- Grounded public-contract corpus: 287 admitted source-linked rules, 287 evidence spans, 26 public source records.
- OptSemBench-C: 4,216 generated SQL probes covering 7,112 renderable valid feature interactions. The generator is rule-aware: 99 probes are forced by admitted public rule guards, and the remaining probes come from the feature-interaction universe.
- SQL validation: 12,648 probe-catalog executions across three deterministic validation catalogs, with zero failures.
- Real-engine SQL validation: 8,432 DuckDB/PostgreSQL full-corpus executions and 142 feature-space representative executions, with zero failures.
- Published feature-space denominator: 90/90 optimizer/workload requirements across 12 families are covered by 71 distinct generated SQL representatives; the deterministic-catalog validation and many-to-one requirement map are recorded.
- Projection-kernel evaluation: exact, lossy, ablation, mutation, strengthened, and exhaustive field-resolution projections.
- Retained-field certificates: finite separator and field-lattice certificates for the declared projection corpus.
- Claim-evidence graph: paper claims linked to generated outputs and integrity gates.
- Recoding worksheet: every admitted rule exported with source locator, line range, digest, paraphrase, current fields, and blank independent-coding columns.
- Side-balanced evidence audit: every headline false witness has public-source support on both compared sides.
- Anti-overfit boundary ledger: source removal, probe subsampling, feature-family stress, engine-family stress, source-density-normalized hotspot diagnostics, failed point-learned transfer, and resource-profile checks are reported separately so stress evidence is not overstated as a learned generalization claim.

## Paper-facing evidence views

The `evaluation/*_paper.csv` files are reproducible presentation views, not manually selected data. `scripts/compute_projection_information_profile.py` writes both the complete `evaluation/projection_information_profile.csv` and the compact `evaluation/projection_information_paper.csv`; `scripts/compute_benchmark_motif_difficulty.py` writes both `evaluation/benchmark_motif_difficulty.csv` and the plotted `evaluation/benchmark_motif_difficulty_paper.csv`. `scripts/render_python_figures.py` renders the quantitative paper figures from these frozen CSV views and records input/output hashes in `evaluation/paper_figure_manifest.csv`. Framework and dataflow figures remain native LaTeX/TikZ in the manuscript tree. The motif crosswalk is feature-space coverage, not a claim that generated probes reproduce third-party benchmark workloads.

## Fast check

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 bash run_mainline_checks.sh
```

Expected result:

```text
Unit tests passed: ...
Package cleanliness check: passed
Package manifest check: passed
Fast mainline checks: passed
```

For a non-mutating certificate check, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/check_readonly_certificate.py
```

This command only reads existing certificates and reports whether they are passing. Use the replay commands below when you want to regenerate outputs in a separate clean workspace.

## Projection audit CLI

The reusable command-line entry point is `python -m optsemc.cli`.  The paper's headline projection counts can be recomputed with:

```bash
python -m optsemc.cli --root .. metrics --projection keyword yesno operator_only
python -m optsemc.cli --root .. witnesses --projection keyword --limit 5
```

`audit-csv` applies the same projection and witness logic to a user-supplied comparison table with one public-contract atom per row.  Required columns are `engine`, `probe_id`, `operator`, `kind`, `layer`, `placement`, `decision_time`, and `observability`; `variant` and `state` are optional.

```bash
python -m optsemc.cli audit-csv --input contracts.csv --projection keyword --mode witnesses
```

## Execution environment

The artifact is designed for standard Linux systems with Python 3.10 and the pinned dependencies in `requirements.txt` and `constraints.txt`. Development edits were made on Windows, while the full replay and integrity gates were validated on Linux. Cloud execution was used as the validation host, not as a private service dependency. The tested environment is recorded in `evaluation/environment.csv` after a replay. The public replay does not require project-specific credentials or private infrastructure.

## Full no-cache replay

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 bash run_from_scratch_no_cache.sh
```

The replay removes derived generated outputs, regenerates probes and contract maps from grounded evidence, rebuilds the SQL bundle, validates generated SQL probes and published feature-space representatives on deterministic catalogs, records replay resource profiles in `evaluation/resource_profile.csv`, checks the evidence-freeze manifest, rebuilds the claim ledger, runs optional DuckDB/PostgreSQL validation when `RUN_REAL_ENGINE_VALIDATION=1`, and runs integrity suites. Paper-build checks are kept out of the anonymous replay archive.

The saved real-engine CSV files are replay certificates. A fresh DuckDB/PostgreSQL rerun must use `RUN_REAL_ENGINE_VALIDATION=1 OPTSEMC_POSTGRES_DSN=... bash run_from_scratch_no_cache.sh` or `bash run_cloud_real_engine_validation.sh`, which writes `evaluation/real_engine_fresh_run.csv`, binds the fresh marker to a SHA-256 bundle of the generated evidence files, and changes the validation mode from saved-certificate replay to fresh-engine rerun.

## Scope notes

The corpus is a public-contract denominator, not a private optimizer oracle. Source-linked rules are admitted from public evidence spans with digests, line ranges, guards, and observability fields. DuckDB and PostgreSQL real-engine runs validate that the generated SQL denominator is executable on two open systems; they do not admit rules for other engines or turn documentation into private implementation truth. The field-stability outputs test whether the finite kernel is a one-source, one-probe, or one-engine-family artifact; they do not claim that a field basis learned on one engine pair transfers to arbitrary future systems. Source-density hotspot outputs normalize pair counts by admitted rule mass and rule product as sensitivity diagnostics; they are not documentation-normalized prevalence estimates. Testing tools such as SQLsmith and SQLancer are complementary implementation bug finders, while this artifact audits whether an optimizer comparison vocabulary collapses distinct public contracts.
