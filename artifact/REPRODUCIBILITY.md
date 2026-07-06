# Reproducibility Guide

This artifact reproduces the numerical claims in *OptSem-C: Benchmarking Projection Precision in Public Query-Optimizer Contracts*.

## Fast verification

```bash
cd artifact
PYTHONDONTWRITEBYTECODE=1 ./run_mainline_checks.sh
```

This command runs package unit tests, checks package hygiene, verifies manifest coherence, and then checks core frozen certificates, paper/table alignment, source-witness support, and key numerical targets.

On the Linux validation machine used for replay, the fast path completes in minutes and the deep path regenerates derived corpus, projection, SQL, and integrity outputs. Exact package, Python, dependency, and platform details are written to `evaluation/environment.csv`.

## Unit tests

```bash
cd artifact
PYTHONDONTWRITEBYTECODE=1 python scripts/run_unit_tests.py
```

The tests cover finite relations, set cover, hitting sets, SQL shape normalization, field lattices, and contract-state algebra.

## Execution scope

| Scope | Purpose | Expected environment |
|---|---|---|
| Source inspection | Read paper source, evidence ledgers, grounded rules, generated probes, and checked CSV certificates. | Any platform with a text editor. |
| Fast checks | Verify package hygiene, core certificates, and frozen headline targets. | Linux or compatible POSIX shell with Python 3.10 and `artifact/requirements.txt`. |
| Deep replay | Regenerate derived projection, SQL, robustness, resource, figure, table, and package certificates. | Linux validation host with the pinned dependencies. |
| Fresh real-engine validation | Rerun DuckDB and PostgreSQL probe execution certificates. | Cloud or server host with PostgreSQL available and `OPTSEMC_POSTGRES_DSN` set. |
| Paper compile | Rebuild the PVLDB manuscript PDF and visual/layout certificates. | Cloud validation host with the LaTeX toolchain. |

## Deep replay

```bash
cd artifact
PYTHONDONTWRITEBYTECODE=1 ./run_deep_checks.sh
```

The deep replay rebuilds derived measurements from the grounded corpus and benchmark specifications. It is more expensive than the fast check because it regenerates contract maps, probe coverage, SQL validation, projection diagnostics, repair certificates, anti-overfit boundary tables, resource profiles, the evidence-freeze manifest, and paper-alignment tables. In an anonymous artifact-only archive, paper-build checks are skipped automatically and the package snapshot is checked against the replay package scope.

## Cloud real-engine validation

```bash
cd artifact
PYTHON=/path/to/python OPTSEMC_POSTGRES_DSN="postgresql://USER@HOST:PORT/DBNAME" ./run_cloud_real_engine_validation.sh
```

This replay runs the generated probes on DuckDB and PostgreSQL and then checks the newly written certificates in fresh mode. It is intended for a validation host with PostgreSQL available; the deterministic-catalog checks remain the portable baseline. The saved CSVs in the package are certificate evidence until this command is rerun.

## Key targets

- 287 admitted source-linked public-contract rules.
- 287 public evidence spans.
- 4,216 executable SQL probes.
- 7,112 valid optimizer-feature interactions.
- 99 generated probes forced by admitted public rule guards; the rest are feature-interaction coverage probes.
- 90/90 external optimizer motifs covered by 71 distinct generated SQL representatives, with deterministic-catalog validation and an explicit motif-to-probe map.
- 254 keyword false equivalences, 238 operator-only false equivalences, and 6 yes/no false equivalences.
- 44 unsafe retained-field vocabularies among all 256 retained-field subsets.
- 498 headline witnesses repaired by the layer+placement semantic basis.
- 12,648 probe-catalog SQL executions with zero failures.
- 8,432 DuckDB/PostgreSQL full-corpus executions and 142 motif-representative executions with zero failures (71 representatives on each engine).

The repair and robustness targets are finite stability checks over the declared public-contract denominator. They should not be read as a learned generalization guarantee for future engines, private optimizer behavior, or third-party workload performance.
