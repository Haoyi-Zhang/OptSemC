# OptSemC Artifact

OptSemC evaluates public query-optimizer behavior contracts, not hidden implementation behavior or runtime latency. This directory is the public replay package: it contains the grounded corpus, benchmark probe generator, generated probes, reusable Python package, checks, tests, and reproducibility outputs needed to inspect the claims.

The manuscript source is intentionally outside the anonymous replay archive. The replay package is sufficient to rebuild the corpus, derived tables, SQL bundles, and integrity reports; manuscript compilation is a separate paper-build gate in the development repository.

## Archive verification

The public anonymous replay package is archived at https://doi.org/10.5281/zenodo.21198009. The repository README and the PVLDB availability block record the exact SHA-256 for the uploaded `optsemc-artifact.zip`. Verify a downloaded archive with:

```bash
sha256sum optsemc-artifact.zip
```

The archive records its source Git commit and clean-tree status in `artifact/evaluation/git_tree_state.csv`. The recorded SHA-256 applies only to the uploaded zip. If replay code, grounded corpus inputs, generated-probe logic, validation scripts, or paper-facing evidence changes, the release gate requires a new clean-tree archive build and a new digest in the repository README and PVLDB availability block.

## Main research objects

- Grounded public-contract corpus: 287 admitted source-linked rules, 287 evidence spans, 26 public source records.
- OptSemBench-C: 4,216 generated SQL probes covering 7,112 renderable valid feature interactions. The generator is rule-aware: 99 probes are forced by admitted public rule guards, and the remaining probes come from the feature-interaction universe.
- SQL validation: 12,648 probe-catalog executions across three deterministic validation catalogs, with zero failures.
- Real-engine SQL validation: 8,432 DuckDB/PostgreSQL full-corpus executions and 142 motif-representative executions, with zero failures.
- Published-motif denominator: 90/90 motifs across 12 optimizer/workload families are covered; each motif has a generated SQL representative validated on the deterministic catalog.
- Projection-kernel evaluation: exact, lossy, ablation, mutation, strengthened, and exhaustive field-resolution projections.
- Repair certificates: finite separator and field-lattice certificates for semantic repair.
- Claim-evidence graph: paper claims linked to generated outputs and integrity gates.
- Side-balanced evidence audit: every headline false witness has public-source support on both compared sides.
- Anti-overfit boundary ledger: source removal, probe subsampling, feature-family stress, engine-family stress, failed point-learned transfer, and resource-profile checks are reported separately so stress evidence is not overstated as a learned generalization claim.

## Fast check

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 ./run_mainline_checks.sh
```

Expected result:

```text
Unit tests passed: ...
Package cleanliness check: passed
Package manifest check: passed
Fast mainline checks: passed
```

## Execution environment

The artifact is designed for standard Linux systems with Python 3 and the dependencies in `requirements.txt`. Development edits were made on Windows, while the full replay and integrity gates were validated on Linux. Cloud execution was used as the validation host, not as a private service dependency. The tested environment is recorded in `evaluation/environment.csv` after a replay. The public replay does not require project-specific credentials or private infrastructure.

## Full no-cache replay

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 ./run_from_scratch_no_cache.sh
```

The replay removes derived generated outputs, regenerates probes and contract maps from grounded evidence, rebuilds the SQL bundle, validates generated SQL probes and published-motif representatives on deterministic catalogs, records replay resource profiles in `evaluation/resource_profile.csv`, checks the evidence-freeze manifest, rebuilds the claim ledger, runs optional DuckDB/PostgreSQL validation when `RUN_REAL_ENGINE_VALIDATION=1`, and runs integrity suites. Paper-build checks are kept out of the anonymous replay archive.

The saved real-engine CSV files are replay certificates. A fresh DuckDB/PostgreSQL rerun must use `run_cloud_real_engine_validation.sh`, which writes `evaluation/real_engine_fresh_run.csv` and changes the validation mode from saved-certificate replay to fresh-engine rerun.

## Scope notes

The corpus is a public-contract denominator, not a private optimizer oracle. Source-linked rules are admitted from public evidence spans with digests, line ranges, guards, and observability fields. DuckDB and PostgreSQL real-engine runs validate that the generated SQL denominator is executable on two open systems; they do not admit rules for other engines or turn documentation into private implementation truth. The repair-stability outputs test whether the finite kernel is a one-source, one-probe, or one-engine-family artifact; they do not claim that a repair learned on one engine pair transfers to arbitrary future systems. Testing tools such as SQLsmith and SQLancer are complementary implementation bug finders, while this artifact audits whether an optimizer comparison vocabulary collapses distinct public contracts.
