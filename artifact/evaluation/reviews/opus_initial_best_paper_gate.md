review_type: research
model: claude-opus-4-8
endpoint: chat/completions(stream)
base_url: https://api.aixluv.com/v1
reasoning_effort: Ultracode
generated_at: 2026-06-28T05:49:41.8555916+08:00

# VLDB 2027 Regular Research Review: OptSem-C

## Overall Verdict: **BLOCKED**

This work presents interesting formalization of optimizer contracts and a substantial grounded corpus, but **lacks the empirical validation required for VLDB Regular Research**. The synthetic-only SQL validation and circular external motif crosswalk do not constitute sufficient evidence for claims about real optimizer portability. Combined with PVLDB compliance violations and missing baselines, this requires major revision before it could clear a research gate.

---

## Severity-Ordered Findings

### P0-001: No Real Query Engine Validation
**Severity:** P0 (blocks submission)  
**Affected:** Core experimental claims, Sections 5-6, all benchmark results  
**Why it matters:** The paper claims to characterize optimizer portability across PostgreSQL, DuckDB, Trino, etc., but all SQL execution happens on `SyntheticOptimizerCatalog`. Running generated SQL on synthetic Python objects validates syntax, not optimizer behavior. This invalidates all empirical portability claims.

**Required fix:**
- Execute the 4,216 generated probes on at least 4 real engines (suggest: PostgreSQL, DuckDB, ClickHouse, Trino)
- Capture actual EXPLAIN plans for each probe-engine pair
- Validate that the observed optimizer decisions match the extracted contracts
- Report false positives (probe doesn't trigger expected behavior) and false negatives (contract missed by extraction)
- Add a results section showing plan-level validation, not just SQL execution success

**Files:** `artifact/scripts/execute_sql_probe_suite.py`, paper Section 5.3, Table 5

---

### P0-002: Page Budget Violation
**Severity:** P0 (blocks submission)  
**Affected:** `Paper/latex/paper.tex`  
**Why it matters:** Paper currently compiles to 13 total pages with references starting on page 13. PVLDB Regular body budget is 12 pages excluding references. The paper exceeds this limit.

**Required fix:**
- Cut 1+ pages of body content to fit 12-page budget
- Likely candidates: reduce Related Work (currently verbose), tighten evaluation tables (many use \scriptsize), move some taxonomy details to appendix
- Remove font/spacing hacks (5.6pt bibliography, negative \itemsep) that attempt to cram content
- Verify compliance: body content ends before page 13, references begin on page 13 or later

**Files:** `Paper/latex/paper.tex`, all tables using `\scriptsize` and manual spacing

---

### P0-003: Manual Bibliography Instead of BibTeX
**Severity:** P0 (blocks submission)  
**Affected:** `Paper/latex/paper.tex`, `Paper/latex/refs.bib`  
**Why it matters:** PVLDB requires BibTeX for reproducibility and metadata consistency. The paper uses `\begin{thebibliography}` with manual entries, while `refs.bib` exists but is unused.

**Required fix:**
- Replace `\begin{thebibliography}...\end{thebibliography}` with `\bibliographystyle{ACM-Reference-Format}` and `\bibliography{refs}`
- Populate `refs.bib` with all current references in proper BibTeX format
- Remove font size hacks; let ACM style handle bibliography formatting
- Verify all citations resolve correctly

**Files:** `Paper/latex/paper.tex` lines with `\begin{thebibliography}`, `Paper/latex/refs.bib`

---

### P0-004: Placeholder Metadata
**Severity:** P0 (blocks submission)  
**Affected:** `Paper/latex/paper.tex` metadata commands  
**Why it matters:** Placeholder DOI (`XX.XX/XXX.XX`) and page numbers (`XXX-XXX`) will cause desk rejection. PVLDB submissions must have proper metadata or leave fields blank per submission guidelines.

**Required fix:**
- Remove placeholder `\acmDOI{XX.XX/XXX.XX}` entirely (PVLDB assigns this post-acceptance)
- Remove placeholder `\settopmatter{printfolios=true}` and `\acmArticle{XXX-XXX}`
- Set `\settopmatter{printacmref=false}` to suppress metadata block per PVLDB submission guidelines
- Verify generated PDF has no placeholder text visible

**Files:** `Paper/latex/paper.tex` preamble

---

### P0-005: Single-Blind Violation Risk
**Severity:** P0 (blocks submission)  
**Affected:** Artifact availability statement, `\acmArticle` commands  
**Why it matters:** Paper contains artifact URL `https://github.com/Haoyi-Zhang/OptSemC` which includes what appears to be an author name. PVLDB uses single-blind review; author-identifying information must be removed.

**Required fix:**
- Replace GitHub URL with anonymized repository or "available upon acceptance" statement
- Remove any author-identifying paths, URLs, or acknowledgments
- For submission, use anonymous services like Anonymous GitHub or include artifact as supplementary material without identifying information
- Ensure no \thanks, \author email, or institutional affiliations are visible in submission PDF

**Files:** `Paper/latex/paper.tex` artifact availability section

---

### P1-001: Circular External Motif Validation
**Severity:** P1 (blocks best-paper)  
**Affected:** Section 5.4, Table 7, external validity claims  
**Why it matters:** The "external motif crosswalk" claims 90/90 coverage across 12 optimizer families, but the validation is circular: (1) extract contracts from documentation, (2) generate probes targeting those contracts, (3) verify generated probes cover external motifs. This doesn't prove the generated probes trigger the same optimizer behavior as the original external queries.

**Required fix:**
- Obtain actual query text for representative external motifs (e.g., TPC-H Q1, Star Schema Benchmark Q1.1, ClickBench queries)
- Run original external queries on real engines and capture EXPLAIN plans
- Run matching generated probes on the same engines and capture plans
- Validate that both trigger the same optimizer rules (e.g., both trigger HashAgg, both use index scan)
- Report divergence rate: cases where generated probe doesn't match original query's optimizer path
- Reframe claim from "coverage" to "validated triggering" with empirical evidence

**Files:** `artifact/scripts/execute_external_motif_suite.py`, paper Section 5.4, Table 7

---

### P1-002: Missing Baselines and Comparisons
**Severity:** P1 (blocks best-paper)  
**Affected:** Evaluation section, novelty claims  
**Why it matters:** Paper presents a formalization and taxonomy without comparing to existing approaches. No discussion of: (1) how manual expert migration compares, (2) existing SQL compatibility layers (Trino federation, Snowflake compatibility), (3) optimizer comparison tools (plan visualizers, EXPLAIN analyzers), or (4) prior optimizer characterization research.

**Required fix:**
- Add Related Work section comparing to:
  - Query optimizer research (Selinger, Volcano/Cascades, cost model studies)
  - Cross-engine SQL compatibility work (Calcite, Presto/Trino federation)
  - Database migration tools and portability studies
  - Formal semantics for SQL (K-SQL, Coq formalization efforts)
- Add baseline comparison: manual expert vs. contract-guided migration time/errors
- Add case study: actual migration of a workload using OptSem-C contracts vs. ad-hoc approach
- Quantify value: "Using OptSem-C contracts reduced migration time by X% and avoided Y portability bugs"

**Files:** New Related Work section, new case study in evaluation

---

### P1-003: No Git Repository or Version Control
**Severity:** P1 (blocks best-paper)  
**Affected:** Entire project, reproducibility claims  
**Why it matters:** Project states "This folder is currently not a Git repository." For a systems research artifact claiming reproducibility, lack of version control is unacceptable. Makes it impossible to track changes, validate provenance, or reproduce historical states.

**Required fix:**
- Initialize Git repository at project root
- Add `.gitignore` excluding generated outputs, Python cache, LaTeX auxiliary files
- Commit clean baseline with meaningful commit message structure
- Tag releases corresponding to paper revisions (e.g., `v0.1-initial-submission`)
- Update artifact documentation to reference Git workflow
- Include `.git` in artifact distribution or document how to clone repository

**Files:** Project root, new `.gitignore`, new `README.md` with Git instructions

---

### P1-004: Version "1.0.0" Finalization Framing
**Severity:** P1 (blocks best-paper)  
**Affected:** `artifact/pyproject.toml`, data object version fields  
**Why it matters:** `version = "1.0.0"` signals finalized released software, not research under review. Combined with exact-target tests (must be exactly 287 rules, 4,216 probes), this suggests the work is presented as complete rather than open for scientific scrutiny.

**Required fix:**
- Change version to `0.1.0-dev` or similar pre-release identifier
- Add version history and change log
- Reframe exact-target tests as integrity checks, not success criteria
- Add discussion of limitations and future work
- Remove "final" framing from documentation and comments
- Add explicit statement in paper: "This is research software under active development"

**Files:** `artifact/pyproject.toml`, test files with exact assertions, paper discussion sections

---

### P1-005: PVLDB Formatting Violations
**Severity:** P1 (blocks best-paper)  
**Affected:** `Paper/latex/paper.tex` formatting commands  
**Why it matters:** Paper uses aggressive font/spacing hacks to cram content: 5.6pt bibliography font, negative \itemsep, manual \vspace around tables. These violate PVLDB formatting guidelines and will trigger desk rejection or reformatting requests.

**Required fix:**
- Remove `\fontsize{5.6pt}{6.5pt}\selectfont` from bibliography
- Remove negative `\itemsep` adjustments
- Remove manual `\vspace{-Xpt}` commands around floats
- Use only standard ACM template commands
- If content doesn't fit, cut content rather than hack formatting
- Use `\begin{table}[t]` placement, but respect template spacing

**Files:** `Paper/latex/paper.tex` throughout, especially bibliography and table environments

---

### P2-001: Data Discrepancy in External Motif Counts
**Severity:** P2 (weakens claims)  
**Affected:** `artifact/evaluation/claim_metric_summary.csv`, paper Section 5.4  
**Why it matters:** Paper claims "90 motifs across 12 families" but `claim_metric_summary.csv` shows `external_benchmark_motifs=5, external_benchmark_requirements=41`. This discrepancy raises questions about data quality and whether numbers in the paper are stale or inflated.

**Required fix:**
- Reconcile the two numbers by examining source data
- If 90 is correct, regenerate `claim_metric_summary.csv`
- If 5 is correct, update paper text and Table 7
- Add provenance documentation explaining how motif counts are computed
- Run `artifact/run_from_scratch_no_cache.sh` to verify all outputs are consistent
- Add test that cross-checks paper claims against generated CSV files

**Files:** `artifact/evaluation/claim_metric_summary.csv`, paper Section 5.4, Table 7

---

### P2-002: Exact-Target Tests Prevent Independent Validation
**Severity:** P2 (weakens claims)  
**Affected:** Test files asserting exact counts (287 rules, 4,216 probes, etc.)  
**Why it matters:** Tests that require exactly 287 rules create a self-fulfilling prophecy: any change breaks tests rather than signaling meaningful change. This makes independent validation difficult and suggests numbers were fitted rather than discovered.

**Required fix:**
- Replace exact assertions with range checks (e.g., `assert 250 <= rule_count <= 350`)
- Add tests for structural properties (all rules have source links, all probes are valid SQL)
- Add tests for minimal coverage (e.g., `assert rule_count >= 200` as sanity check)
- Document expected ranges in test docstrings
- If exact counts are critical, add separate "integrity lock" tests clearly marked as intentionally brittle
- Add discussion in paper about expected variability

**Files:** Test files in `artifact/tests/`, especially integration tests

---

### P2-003: Scale Metrics as Quality Gates
**Severity:** P2 (weakens claims)  
**Affected:** Repository quality checks counting LOC, files, functions  
**Why it matters:** Checks like "Python LOC > X" or "number of scripts >= Y" can be gamed and don't indicate research quality. Best-paper work is judged on scientific contribution, not code volume.

**Required fix:**
- Remove LOC/file-count gates from quality checks
- Replace with meaningful checks: test coverage %, documentation completeness, code complexity metrics
- Focus quality gates on correctness: all tests pass, no lint errors, types check
- Add semantic checks: contracts are well-formed, probes target contracts, provenance links resolve
- Remove "scale" framing from paper and artifact documentation

**Files:** `artifact/scripts/check_repository_quality.py` or similar, test harnesses

---

### P2-004: No Discussion of Contract Evolution
**Severity:** P2 (weakens claims)  
**Affected:** Paper discussion, future work  
**Why it matters:** Optimizer behavior changes across versions (PostgreSQL 14 vs 15, Spark 3.2 vs 3.5). Paper's contracts include `version/time_window` fields but doesn't discuss how to handle version drift or contract deprecation.

**Required fix:**
- Add section discussing temporal validity of contracts
- Document which optimizer versions were analyzed (specific PostgreSQL version, etc.)
- Discuss strategy for maintaining contracts as optimizers evolve
- Add "version coverage" metric: how many major versions per optimizer
- Propose diff-based approach for tracking contract changes
- Add limitation: contracts are point-in-time and require maintenance

**Files:** Paper discussion/limitations section, contract schema documentation

---

### P2-005: Missing Inter-Annotator Reliability
**Severity:** P2 (weakens claims)  
**Affected:** Contract extraction methodology, grounded corpus claims  
**Why it matters:** Paper claims 287 "verified public-contract rules" but doesn't discuss extraction methodology quality. Were rules extracted by one person? Multiple annotators? What's the agreement rate? How were disputes resolved?

**Required fix:**
- Document extraction protocol: selection criteria, annotation schema, decision rules
- If multi-annotator, report inter-annotator agreement (Cohen's kappa or similar)
- If single-annotator, have second person independently extract sample (e.g., 50 rules) and compare
- Report extraction challenges and ambiguous cases
- Add quality assurance section describing validation process
- Make extraction guidelines available in artifact

**Files:** Paper methodology section, `artifact/docs/extraction_protocol.md` (new)

---

### P3-001: Review Outputs Polluting Artifact
**Severity:** P3 (polish)  
**Affected:** `artifact/evaluation/reviews/` directory  
**Why it matters:** Storing review-generated evidence under `artifact/` mixes research outputs with meta-review content. Artifact should contain only reproducible research artifacts.

**Required fix:**
- Move review outputs to separate `reviews/` directory at project root (sibling to `Paper/` and `artifact/`)
- Update artifact checks to ignore `reviews/` directory
- Document that `reviews/` is not part of submitted artifact
- Add `reviews/` to `.gitignore`

**Files:** `artifact/evaluation/reviews/`, directory structure

---

### P3-002: Missing Limitations Section
**Severity:** P3 (polish)  
**Affected:** Paper discussion  
**Why it matters:** Best-paper work acknowledges limitations openly. Current paper presents results without discussing what the approach cannot do.

**Required fix:**
- Add explicit Limitations section before Conclusion
- Discuss: (1) synthetic-only validation, (2) point-in-time contracts, (3) manual extraction effort, (4) no cost model analysis, (5) no query performance impact
- Frame limitations as opportunities for future work
- Add discussion of when OptSem-C contracts are/aren't useful

**Files:** Paper Section 7 (new), before Conclusion

---

### P3-003: Missing Related Work on Optimizer Comparison
**Severity:** P3 (polish)  
**Affected:** Paper related work, positioning  
**Why it matters:** Paper doesn't cite relevant optimizer research: Volcano/Cascades frameworks, cost model studies, plan space exploration, optimizer testing work.

**Required fix:**
- Add citations: Graefe (Volcano/Cascades), Selinger et al., Chaudhuri (optimizer overview)
- Cite optimizer testing: Rigger (SQLancer), query fuzzing work
- Cite cross-engine SQL: Apache Calcite, Presto/Trino
- Position OptSem-C relative to: (1) formalization depth vs. prior work, (2) grounded corpus vs. theoretical models

**Files:** Paper Related Work section, `Paper/latex/refs.bib`

---

### P3-004: No Case Study or User Validation
**Severity:** P3 (polish, but impacts venue fit)  
**Affected:** Evaluation, user-facing utility claims  
**Why it matters:** Paper claims contracts help with "query engine portability" but provides no evidence that practitioners find them useful. Best-paper systems work often includes case study or user study.

**Required fix:**
- Add case study: migrate a real workload (e.g., 50 queries from Stack Overflow Analytics) from PostgreSQL to DuckDB
- Document: (1) how contracts helped, (2) portability issues discovered, (3) time saved vs. ad-hoc approach
- Alternative: user study with database developers/engineers reviewing contracts for actionability
- Add qualitative feedback: "Contracts helped identify X, but missed Y"

**Files:** Paper Section 5.5 (new case study subsection)

---

## Prioritized Action Plan

### Phase 1: Unblock Submission (P0 fixes, ~2-3 weeks)
1. **Real-engine validation** (P0-001): Execute 4,216 probes on PostgreSQL, DuckDB, ClickHouse, Trino. Capture EXPLAIN plans. This is the most time-consuming but most critical fix.
2. **PVLDB compliance** (P0-002 through P0-005):
   - Cut paper to 12 body pages
   - Convert to BibTeX bibliography
   - Remove placeholder metadata
   - Anonymize artifact URL
3. **Initialize Git repository** (P1-003): Version control is foundational for all subsequent changes

### Phase 2: Strengthen Evidence (P1 fixes, ~3-4 weeks)
4. **Validate external motifs** (P1-001): Run original TPC-H/SSB/ClickBench queries alongside generated probes, compare EXPLAIN plans
5. **Add baselines** (P1-002): Literature review, manual migration comparison, case study
6. **Fix data quality** (P2-001, P2-005): Reconcile motif counts, document extraction methodology
7. **Remove finalization framing** (P1-004): Version 0.1.0-dev, reframe tests

### Phase 3: Polish for Best-Paper (P2/P3 fixes, ~1-2 weeks)
8. **Fix PVLDB formatting** (P1-005): Remove all font/spacing hacks, respect template
9. **Improve tests** (P2-002, P2-003): Range checks, remove scale metrics
10. **Add discussion** (P2-004, P3-002): Contract evolution, limitations
11. **Expand related work** (P3-003): Optimizer research citations
12. **Add case study** (P3-004): Real workload migration evidence

### Phase 4: Final Validation (~1 week)
13. Run `artifact/run_from_scratch_no_cache.sh` end-to-end with all new experiments
14. Independent review: have colleague attempt to reproduce results from artifact
15. Proofread paper for consistency with new results
16. Submit to VLDB with confidence

**Estimated total time:** 7-10 weeks of focused work

---

## Signoff Conditions Checklist

This work can be considered **best-paper ready** when:

### Scientific Rigor
- [ ] 4,216 generated probes executed on ≥4 real query engines with EXPLAIN plan capture
- [ ] Plan-level validation shows generated probes trigger expected optimizer rules with ≥85% accuracy
- [ ] External motif validation compares original queries vs. generated probes on same engines
- [ ] False positive/negative rates reported for contract extraction
- [ ] At least one migration case study showing contracts reduce migration time/errors
- [ ] Comparison to ≥2 baselines (manual expert, existing compatibility layer)

### Artifact Quality
- [ ] Git repository with clean commit history
- [ ] Version 0.x.y-dev, not 1.0.0
- [ ] Tests use range checks, not exact-target assertions
- [ ] `run_from_scratch_no_cache.sh` completes successfully in <4 hours
- [ ] All data files have provenance documentation
- [ ] Inter-annotator reliability ≥0.8 (Cohen's kappa) or equivalent validation
- [ ] External motif counts consistent across paper and generated files

### Paper Quality
- [ ] 12 body pages or fewer (not counting references)
- [ ] BibTeX bibliography with ≥30 relevant citations
- [ ] No placeholder metadata (DOI, pages, URLs)
- [ ] Anonymized for single-blind review
- [ ] No font/spacing hacks (5.6pt font, negative vspace)
- [ ] Related Work section covering optimizer research, SQL portability, formalization
- [ ] Limitations section acknowledging scope boundaries
- [ ] Discussion of contract evolution and maintenance

### Novelty & Impact
- [ ] Formal semantics contribution clearly distinguished from prior SQL formalization work
- [ ] Projection-kernel formulation validated with real optimizer divergence examples
- [ ] Grounded corpus demonstrates breadth (≥6 engines) and depth (≥200 rules)
- [ ] User-facing utility demonstrated through case study or qualitative feedback
- [ ] Clear articulation of when OptSem-C contracts are/aren't useful

### VLDB Venue Fit
- [ ] Substantial systems contribution with empirical validation
- [ ] Novel technical content beyond taxonomy/survey
- [ ] Reproducible artifact supporting all major claims
- [ ] Writing quality suitable for archival publication
- [ ] Addresses important problem in database systems

---

## Final Recommendation

**Current state:** The work has strong ideas (optimizer contract formalization, projection-kernel analysis) but insufficient empirical validation for VLDB Regular. The synthetic-only validation is a critical gap that undermines all portability claims.

**Path forward:** With real-engine validation (Phase 1), strengthened evidence (Phase 2), and polish (Phase 3), this could become a solid VLDB paper. However, reaching best-paper level requires the full signoff checklist, particularly: real-engine validation, external baselines, case study evidence, and addressing the circular validation issues.

**Realistic timeline:** 7-10 weeks of focused work to reach submission quality, additional 2-3 weeks for best-paper polish.

**Alternative venue:** If real-engine validation proves infeasible, consider reframing as a taxonomy/formalization paper for a workshop (DBTest, TaPP) or short paper track. The grounded corpus alone is valuable, but VLDB Regular expects systems-level empirical validation.