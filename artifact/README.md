# OptSemC Artifact

OptSemC evaluates public query-optimizer behavior contracts, not hidden implementation behavior or runtime latency. This directory is the public replay package: it contains the grounded corpus, benchmark probe generator, generated probes, reusable Python package, checks, tests, and reproducibility outputs needed to inspect the claims.

The manuscript source is intentionally outside the anonymous replay archive. The replay package is sufficient to rebuild the corpus, derived tables, SQL bundles, and integrity reports; manuscript compilation is a separate paper-build gate in the development repository.

## Main research objects

- Grounded public-contract corpus: 287 verified rules, 287 source-linked evidence spans, 26 public source records.
- OptSemBench-C: 4,216 generated SQL probes covering 7,112 renderable valid feature interactions.
- SQL validation: 12,648 probe-catalog executions across three deterministic validation catalogs, with zero failures.
- Real-engine validation: 8,432 DuckDB/PostgreSQL full-corpus executions and 142 motif-representative executions, with zero failures.
- Published-motif denominator: 90/90 motifs across 12 optimizer/workload families are covered; each motif has a generated SQL representative validated on the deterministic catalog.
- Projection-kernel evaluation: exact, lossy, ablation, mutation, strengthened, and exhaustive field-resolution projections.
- Repair certificates: finite separator and field-lattice certificates for semantic repair.
- Claim-evidence graph: paper claims linked to generated outputs and integrity gates.
- Side-balanced evidence audit: every headline false witness has public-source support on both compared sides.

## Fast check

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 ./run_mainline_checks.sh
```

Expected result:

```text
Package integrity check: passed
Fast mainline checks: passed
```

## Execution environment

The artifact is designed for standard Linux systems with Python 3 and the dependencies in `requirements.txt`. Development edits were made on Windows, while the full replay and integrity gates were validated on Linux. The public replay does not require project-specific credentials or private infrastructure.

## Full no-cache replay

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 ./run_from_scratch_no_cache.sh
```

The replay removes derived generated outputs, regenerates probes and contract maps from grounded evidence, rebuilds the SQL bundle, validates generated SQL probes and published-motif representatives on deterministic catalogs, runs optional DuckDB/PostgreSQL validation when `RUN_REAL_ENGINE_VALIDATION=1`, and runs integrity suites. Paper-build checks are kept out of the anonymous replay archive.
