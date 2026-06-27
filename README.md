# OptSem-C

OptSem-C studies public optimizer behavior contracts for analytical SQL engines. It separates the public contract an engine exposes from hidden implementation behavior and latency measurements.

The project has two primary directories:

- `Paper/`: PVLDB-style LaTeX source, generated figures, generated tables, bibliography, compiled paper, and supplement material.
- `artifact/`: grounded corpus, benchmark probe generator, generated probes, evaluation outputs, reusable Python package, scripts, tests, and reproducibility checks.

The active manuscript source is `Paper/latex/paper.tex`. The artifact entry point is `artifact/README.md`.

All experiment replay and paper compilation for this project should be run on the configured cloud server. Local work should be limited to source inspection, editing, static checks, and packaging preparation.

