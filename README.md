# OptSem-C

OptSem-C studies public optimizer behavior contracts for analytical SQL engines. It separates the public contract an engine exposes from hidden implementation behavior and latency measurements.

The project has two primary directories:

- `Paper/`: PVLDB-style LaTeX source, generated figures, generated tables, bibliography, compiled paper, and supplement material.
- `artifact/`: grounded corpus, benchmark probe generator, generated probes, evaluation outputs, reusable Python package, scripts, tests, and reproducibility checks.

The active manuscript source is `Paper/latex/paper.tex`. The artifact entry point is `artifact/README.md`.

## Artifact archive

The public anonymous replay package is archived at https://doi.org/10.5281/zenodo.21211610. The expected SHA-256 for the archived `optsemc-artifact.zip` is:

```text
b78a87658980f3123bbf82481118fb7d1a3efcbc928b6253beda3335863facb3
```

The archived replay package records its source Git state in `artifact/evaluation/git_tree_state.csv`. The digest above applies only to that uploaded archive. Any commit that changes replay code, grounded corpus inputs, generated-probe logic, validation scripts, or paper-facing evidence must rebuild the anonymous archive from a clean source tree and update both the repository README and the PVLDB availability block.

## Evidence scope

OptSem-C is a finite public-contract audit, not a learned model and not a hidden-optimizer oracle. OptSemBench-C is rule-aware by design: 99 probes are forced by admitted public rule guards so that the declared contract denominator is reachable, while the remaining probes cover optimizer-feature interactions. The paper therefore treats robustness checks as source/probe/feature/engine stress evidence, not as proof that a point-learned repair generalizes to arbitrary future engines. Resource-profile rows report the cost of rerunning this finite comparison audit; the deterministic 8x lift checks only the comparison inner loop, not a new corpus, source set, or engine-count claim.

## Execution environment

The artifact is designed for standard Linux systems with Python 3 and the dependencies listed in `artifact/requirements.txt`. Cloud execution was used as the validation host for full replay and paper compilation; it is not a private service dependency for inspecting or replaying the public artifact. Local work in this repository should be limited to source inspection, editing, static checks, and packaging preparation unless a reviewer intentionally runs the artifact replay.
