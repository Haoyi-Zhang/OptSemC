# OptSem-C

OptSem-C studies public optimizer behavior contracts for analytical SQL engines. It separates the public contract an engine exposes from hidden implementation behavior and latency measurements.

The project has two primary directories:

- `Paper/`: PVLDB-style LaTeX source, generated figures, generated tables, bibliography, compiled paper, and supplement material.
- `artifact/`: grounded corpus, benchmark probe generator, generated probes, evaluation outputs, reusable Python package, scripts, tests, and reproducibility checks.

The active manuscript source is `Paper/latex/paper.tex`. The artifact entry point is `artifact/README.md`.

## Artifact archive

The public anonymous replay package is archived at https://doi.org/10.5281/zenodo.21194523. The expected SHA-256 for `optsemc-artifact.zip` is:

```text
0c33154200aca8bc8c26fae9ac1b17e9de7afe421f283813c66dd777a5f7d8a1
```

The archived replay package was built from Git commit `f48421f081db`. Later public repository commits may update the paper availability block, compiled PDF, archive digest, or repository metadata; they do not change the replay code, grounded corpus, generated probes, or validation scripts used by the archived package.

## Execution environment

The artifact is designed for standard Linux systems with Python 3 and the dependencies listed in `artifact/requirements.txt`. Cloud execution was used as the validation host for full replay and paper compilation; it is not a private service dependency for inspecting or replaying the public artifact. Local work in this repository should be limited to source inspection, editing, static checks, and packaging preparation unless a reviewer intentionally runs the artifact replay.
