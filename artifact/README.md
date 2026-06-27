# OptSemC Artifact

OptSemC is the companion artifact for *OptSem-C: Public Optimizer Contracts for Query Engine Portability*. It evaluates public query-optimizer behavior contracts, not hidden implementation behavior or runtime latency.

## Package layout

The package has two top-level folders:

- `Paper/`: PVLDB-style LaTeX source, generated figures/tables, bibliography, compiled paper, and supplemental material.
- `artifact/`: grounded corpus, generated benchmark probes, executable SQL bundle, reusable Python package, checks, tests, and reproducibility outputs.

The active paper source is `Paper/latex/paper.tex`.

## Main research objects

- Grounded public-contract corpus: 287 verified rules, 287 source-linked evidence spans, 26 public source records.
- OptSemBench-C: 4,216 generated SQL probes covering 7,112 renderable valid feature interactions.
- SQL validation: 12,648 probe-catalog executions across three deterministic validation catalogs, with zero failures.
- External motif denominator: 90/90 motifs across 12 optimizer/workload families are covered; each motif has a generated SQL representative validated on the deterministic catalog.
- Projection-kernel evaluation: exact, lossy, ablation, mutation, strengthened, and exhaustive field-resolution projections.
- Repair certificates: finite separator and field-lattice certificates for semantic repair.
- Claim-evidence graph: paper claims linked to generated outputs and integrity gates.
- Side-balanced evidence audit: every headline false witness has public-source support on both compared sides.

## Fast check

Run from the `artifact/` directory:

```bash
PYTHONDONTWRITEBYTECODE=1 ./run_mainline_checks.sh
```

Expected result:

```text
Package integrity check: passed
Fast mainline checks: passed
```

## Full no-cache replay

Run from `artifact/`:

```bash
PYTHONDONTWRITEBYTECODE=1 ./run_from_scratch_no_cache.sh
```

The replay removes derived generated outputs, regenerates probes and contract maps from grounded evidence, rebuilds the SQL bundle, validates generated SQL probes and external motif representatives on deterministic catalogs, recompiles the paper when enabled, and runs integrity suites.
