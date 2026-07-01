# Reproducibility Guide

This artifact reproduces the numerical claims in *OptSem-C: Public Optimizer Contracts for Query Engine Portability*.

## Fast verification

```bash
cd artifact
PYTHONDONTWRITEBYTECODE=1 ./run_mainline_checks.sh
```

This command checks package hygiene, manifest coherence, core frozen certificates, paper/table alignment, source-witness support, and key numerical targets.

## Unit tests

```bash
cd artifact
PYTHONDONTWRITEBYTECODE=1 python scripts/run_unit_tests.py
```

The tests cover finite relations, set cover, hitting sets, SQL shape normalization, field lattices, and contract-state algebra.

## Deep replay

```bash
cd artifact
PYTHONDONTWRITEBYTECODE=1 ./run_deep_checks.sh
```

The deep replay rebuilds derived measurements from the grounded corpus and benchmark specifications. It is more expensive than the fast check because it regenerates contract maps, probe coverage, SQL validation, projection diagnostics, repair certificates, and paper-alignment tables.

## Cloud real-engine validation

```bash
cd artifact
PYTHON=/path/to/python OPTSEMC_POSTGRES_DSN="dbname=optsemc user=optsemc" ./run_cloud_real_engine_validation.sh
```

This replay runs the generated probes on DuckDB and PostgreSQL and then checks the saved certificates. It is intended for a cloud machine with PostgreSQL available; the deterministic-catalog checks remain the portable baseline.

## Key targets

- 287 verified public-contract rules.
- 287 public evidence spans.
- 4,216 executable SQL probes.
- 7,112 valid optimizer-feature interactions.
- 90/90 external optimizer motifs covered, with generated SQL representatives validated on deterministic catalogs.
- 254 keyword false equivalences, 238 operator-only false equivalences, and 6 yes/no false equivalences.
- 44 unsafe retained-field vocabularies among all 256 retained-field subsets.
- 498 headline witnesses repaired by the layer+placement semantic basis.
- 12,648 probe-catalog SQL executions with zero failures.
- 8,432 DuckDB/PostgreSQL full-corpus executions and 142 motif-representative executions with zero failures.
