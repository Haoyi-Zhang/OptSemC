# Reference Guard Audit

- Input: `Paper\latex\refs.bib`
- Generated: 2026-07-03 17:58:44 UTC
- Policy profile: `cs-conference` - Strict computer-science conference gate emphasizing DBLP, arXiv, OpenReview, DOI, and web identifiers.
- Policy mode: fail-closed; REVIEW/FAIL require human resolution before submission.
- Strict source-error gate: enabled
- Summary: PASS 0 | REVIEW 63 | FAIL 10 | Total 73
- Source limitations: 73 item(s) had at least one source error.

## Results

### 1. REVIEW - codd1970relational

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: A Relational Model of Data for Large Shared Data Banks
- Supplied authors: E. F. Codd
- Supplied year: 1970
- Supplied DOI: `10.1145/362384.362685`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1970 | match | [A relational model of data for large shared data banks](https://doi.org/10.1145/362384.362685) |
| Crossref | 1.000 | 1.000 | 1970 | match | [A relational model of data for large shared data banks](https://doi.org/10.1145/362384.362685) |
| DBLP | 1.000 | 1.000 | 1970 | match | [A Relational Model of Data for Large Shared Data Banks](https://dblp.org/rec/journals/cacm/Codd70) |
| Crossref | 1.000 | 1.000 | 2002 | conflict | [A Relational Model of Data for Large Shared Data Banks](https://doi.org/10.1007/978-3-642-59412-0_16) |
| Crossref | 1.000 | 1.000 | 2001 | conflict | [A Relational Model of Data for Large Shared Data Banks](https://doi.org/10.1007/978-3-642-48354-7_4) |

### 2. REVIEW - selinger1979access

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Access Path Selection in a Relational Database Management System
- Supplied authors: P. G. Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie, T. G. Price
- Supplied year: 1979
- Supplied DOI: `10.1145/582095.582099`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1979 | match | [Access path selection in a relational database management system](https://doi.org/10.1145/582095.582099) |
| Crossref | 1.000 | 1.000 | 1979 | match | [Access path selection in a relational database management system](https://doi.org/10.1145/582095.582099) |
| DBLP | 1.000 | 1.000 | 1979 | match | [Access Path Selection in a Relational Database Management System](https://dblp.org/rec/conf/sigmod/SelingerACLP79) |
| Crossref | 1.000 | 1.000 | 1989 | conflict | [Access Path Selection in a Relational Database Management System](https://doi.org/10.1016/b978-0-934613-53-8.50038-8) |
| DBLP | 0.948 | 0.000 | 1999 | n/a | [Review - Access Path Selection in a Relational Database Management System](https://dblp.org/rec/journals/dr/Haas99a) |

### 3. REVIEW - graefe1990volcano

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Encapsulation of Parallelism in the Volcano Query Processing System
- Supplied authors: G. Graefe
- Supplied year: 1990
- Supplied DOI: `10.1145/93597.98720`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1990 | match | [Encapsulation of parallelism in the Volcano query processing system](https://doi.org/10.1145/93597.98720) |
| Crossref | 1.000 | 1.000 | 1990 | match | [Encapsulation of parallelism in the Volcano query processing system](https://doi.org/10.1145/93597.98720) |
| DBLP | 1.000 | 1.000 | 1990 | match | [Encapsulation of Parallelism in the Volcano Query Processing System](https://dblp.org/rec/conf/sigmod/Graefe90) |
| Crossref | 1.000 | 1.000 | 1990 | conflict | [Encapsulation of parallelism in the Volcano query processing system](https://doi.org/10.1145/93605.98720) |
| Crossref | 0.311 | 0.000 | None | conflict | [Inter-Query Parallelism](https://doi.org/10.1007/springerreference_64384) |

### 4. REVIEW - graefe1993volcano

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: The Volcano Optimizer Generator: Extensibility and Efficient Search
- Supplied authors: G. Graefe, W. J. McKenna
- Supplied year: 1993
- Supplied DOI: `10.1109/icde.1993.344061`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | None | match | [The Volcano optimizer generator: extensibility and efficient search](https://doi.org/10.1109/icde.1993.344061) |
| Crossref | 1.000 | 1.000 | None | match | [The Volcano optimizer generator: extensibility and efficient search](https://doi.org/10.1109/icde.1993.344061) |
| DBLP | 1.000 | 1.000 | 1993 | match | [The Volcano Optimizer Generator: Extensibility and Efficient Search](https://dblp.org/rec/conf/icde/GraefeM93) |
| Crossref | 0.559 | 0.000 | 2022 | conflict | [A neural architecture generator for efficient search space](https://doi.org/10.1016/j.neucom.2021.10.118) |
| Crossref | 0.331 | 0.000 | 2022 | conflict | [Efficient Non-Parametric Optimizer Search for Diverse Tasks](https://doi.org/10.52202/068431-2215) |

### 5. REVIEW - graefe1995cascades

- Verdict: Single-source strong match
- Supplied title: The Cascades Framework for Query Optimization
- Supplied authors: G. Graefe
- Supplied year: 1995
- Supplied URL: https://www.sigmod.org/publications/dblp/db/journals/debu/Graefe95a.html
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 1995 | n/a | [The Cascades Framework for Query Optimization](https://dblp.org/rec/journals/debu/Graefe95a) |
| Crossref | 0.780 | 0.000 | None | n/a | [A framework for multiple-query optimization](https://doi.org/10.1109/ride.1992.227411) |
| Crossref | 0.438 | 0.000 | 2019 | n/a | [What Does A Slow Query Look Like?](https://doi.org/10.1007/978-1-4842-5144-7_1) |
| Crossref | 0.338 | 0.000 | 2019 | n/a | [How Is A Query Processed?](https://doi.org/10.1007/978-1-4842-5144-7_2) |
| Crossref | 0.313 | 0.000 | 2019 | n/a | [Turning On and Using Query Execution Plans](https://doi.org/10.1007/978-1-4842-5144-7_3) |

### 6. REVIEW - chaudhuri1998overview

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: An Overview of Query Optimization in Relational Systems
- Supplied authors: S. Chaudhuri
- Supplied year: 1998
- Supplied DOI: `10.1145/275487.275492`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: HTTPError: HTTP Error 429: Unknown Error

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1998 | match | [An overview of query optimization in relational systems](https://doi.org/10.1145/275487.275492) |
| Crossref | 1.000 | 1.000 | 1998 | match | [An overview of query optimization in relational systems](https://doi.org/10.1145/275487.275492) |
| DBLP | 1.000 | 1.000 | 1998 | match | [An Overview of Query Optimization in Relational Systems](https://dblp.org/rec/conf/pods/Chaudhuri98) |
| Crossref | 0.920 | 0.000 | None | conflict | [An overview of parallel query optimization in relational systems](https://doi.org/10.1109/dexa.2000.875090) |
| Crossref | 0.792 | 0.000 | 2011 | conflict | [Query Optimization in Relational Database Systems](https://doi.org/10.1201/b10711-5) |

### 7. REVIEW - ioannidis1996query

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Query Optimization
- Supplied authors: Y. E. Ioannidis
- Supplied year: 1996
- Supplied DOI: `10.1145/234313.234367`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1996 | match | [Query optimization](https://doi.org/10.1145/234313.234367) |
| Crossref | 0.571 | 0.000 | 2019 | conflict | [Introduction to SQL Server Query Optimization](https://doi.org/10.1007/978-1-4842-5144-7) |
| DBLP | 0.356 | 0.000 | 2004 | conflict | [Green Query Optimization: Taming Query Optimization Overheads through Plan Recycling](https://dblp.org/rec/conf/vldb/SardaH04) |
| DBLP | 0.350 | 0.000 | 2025 | conflict | [InfoMin-based Query Embedding Optimization For Query-based Universal Sound Separation](https://dblp.org/rec/conf/icassp/Wang0ZZ25) |
| Crossref | 0.333 | 0.000 | 2019 | conflict | [How Is A Query Processed?](https://doi.org/10.1007/978-1-4842-5144-7_2) |

### 8. REVIEW - steinbrunn1997heuristic

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Heuristic and Randomized Optimization for the Join Ordering Problem
- Supplied authors: M. Steinbrunn, G. Moerkotte, A. Kemper
- Supplied year: 1997
- Supplied DOI: `10.1007/s007780050040`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1997 | match | [Heuristic and randomized optimization for the join ordering problem](https://doi.org/10.1007/s007780050040) |
| Crossref | 1.000 | 1.000 | 1997 | match | [Heuristic and randomized optimization for the join ordering problem](https://doi.org/10.1007/s007780050040) |
| DBLP | 1.000 | 1.000 | 1997 | match | [Heuristic and Randomized Optimization for the Join Ordering Problem](https://dblp.org/rec/journals/vldb/SteinbrunnMK97) |
| Crossref | 0.686 | 0.000 | 2011 | conflict | [Genetic optimization for the join ordering problem of database queries](https://doi.org/10.1109/indcon.2011.6139336) |
| Crossref | 0.643 | 0.000 | 2019 | conflict | [Primal Heuristic for the Linear Ordering Problem](https://doi.org/10.5220/0007406300002104) |

### 9. REVIEW - moerkotte2006dpccp

- Verdict: Single-source strong match
- Supplied title: Analysis of Two Existing and One New Dynamic Programming Algorithm for the Generation of Optimal Bushy Join Trees without Cross Products
- Supplied authors: G. Moerkotte, T. Neumann
- Supplied year: 2006
- Supplied URL: https://dblp.org/rec/conf/vldb/MoerkotteN06.html
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 2006 | n/a | [Analysis of Two Existing and One New Dynamic Programming Algorithm for the Generation of Optimal Bushy Join Trees without Cross Products](https://dblp.org/rec/conf/vldb/MoerkotteN06) |
| Crossref | 0.961 | 0.500 | 2018 | n/a | [Errata for "Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products"](https://doi.org/10.14778/3231751.3231756) |
| DBLP | 0.961 | 0.500 | 2018 | n/a | [Errata for "Analysis of two existing and one new dynamic programming algorithm for the generation of optimal bushy join trees without cross products"](https://dblp.org/rec/journals/pvldb/MeisterMS18) |
| Crossref | 0.550 | 0.000 | 2014 | n/a | [Dynamic Programming Algorithm for Generation of Optimal Elimination Trees for Multi-frontal Direct Solver Over H-refined Grids](https://doi.org/10.1016/j.procs.2014.05.085) |
| Crossref | 0.486 | 0.000 | 2015 | n/a | [A Simple Dynamic Programming Algorithm for Counting Red Nodes in Red-Black Trees](https://doi.org/10.7763/ijfcc.2015.v4.357) |

### 10. REVIEW - leis2015good

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: How Good Are Query Optimizers, Really?
- Supplied authors: V. Leis, A. Gubichev, A. Mirchev, P. Boncz, A. Kemper, T. Neumann
- Supplied year: 2015
- Supplied DOI: `10.14778/2850583.2850594`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2015 | match | [How good are query optimizers, really?](https://doi.org/10.14778/2850583.2850594) |
| Crossref | 1.000 | 1.000 | 2015 | match | [How good are query optimizers, really?](https://doi.org/10.14778/2850583.2850594) |
| DBLP | 1.000 | 1.000 | 2015 | match | [How Good Are Query Optimizers, Really?](https://dblp.org/rec/journals/pvldb/LeisGMBK015) |
| Crossref | 0.847 | 1.000 | 2025 | conflict | [Still Asking: How Good Are Query Optimizers, Really?](https://doi.org/10.14778/3750601.3760521) |
| DBLP | 0.847 | 1.000 | 2025 | conflict | [Still Asking: How Good Are Query Optimizers, Really?](https://dblp.org/rec/journals/pvldb/LeisGMBKN25) |

### 11. REVIEW - leis2018looking

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Query Optimization Through the Looking Glass, and What We Found Running the Join Order Benchmark
- Supplied authors: V. Leis, B. Radke, A. Gubichev, A. Mirchev, P. Boncz, A. Kemper, T. Neumann
- Supplied year: 2018
- Supplied DOI: `10.1007/s00778-017-0480-7`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: DataCite: HTTPError: HTTP Error 404: Not Found; OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2017 | match | [Query optimization through the looking glass, and what we found running the Join Order Benchmark](https://doi.org/10.1007/s00778-017-0480-7) |
| Crossref | 1.000 | 1.000 | 2017 | match | [Query optimization through the looking glass, and what we found running the Join Order Benchmark](https://doi.org/10.1007/s00778-017-0480-7) |
| DBLP | 1.000 | 1.000 | 2018 | match | [Query optimization through the looking glass, and what we found running the Join Order Benchmark](https://dblp.org/rec/journals/vldb/LeisRGMBKN18) |
| Crossref | 0.659 | 0.000 | 2012 | conflict | [Introduction / Issue 17: Through the Looking Glass, and What We Found There: Ourselves](https://doi.org/10.47761/494a02f6.433e684d) |
| Crossref | 0.639 | 0.000 | 2012 | conflict | [Contributors / Issue 17: Through the Looking Glass, and What We Found There](https://doi.org/10.47761/494a02f6.c0699445) |

### 12. REVIEW - chaudhuri2009exact

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Exact Cardinality Query Optimization for Optimizer Testing
- Supplied authors: S. Chaudhuri, V. R. Narasayya, R. Ramamurthy
- Supplied year: 2009
- Supplied DOI: `10.14778/1687627.1687739`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; arXiv: HTTPError: HTTP Error 429: Too Many Requests

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2009 | match | [Exact cardinality query optimization for optimizer testing](https://doi.org/10.14778/1687627.1687739) |
| Crossref | 1.000 | 1.000 | 2009 | match | [Exact cardinality query optimization for optimizer testing](https://doi.org/10.14778/1687627.1687739) |
| Semantic Scholar DOI | 1.000 | 1.000 | 2009 | match | [Exact Cardinality Query Optimization for Optimizer Testing](https://www.semanticscholar.org/paper/acfe6f5c19e8f9d02145da5d9e57cc9ba4660b2c) |
| Semantic Scholar | 1.000 | 1.000 | 2009 | match | [Exact Cardinality Query Optimization for Optimizer Testing](https://www.semanticscholar.org/paper/acfe6f5c19e8f9d02145da5d9e57cc9ba4660b2c) |
| DBLP | 1.000 | 1.000 | 2009 | match | [Exact Cardinality Query Optimization for Optimizer Testing](https://dblp.org/rec/journals/pvldb/ChaudhuriNR09) |

### 13. REVIEW - markl2004progressive

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Robust Query Processing Through Progressive Optimization
- Supplied authors: V. Markl, V. Raman, D. Simmen, G. Lohman, H. Pirahesh, M. Cilimdzic
- Supplied year: 2004
- Supplied DOI: `10.1145/1007568.1007642`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2004 | match | [Robust query processing through progressive optimization](https://doi.org/10.1145/1007568.1007642) |
| Crossref | 1.000 | 1.000 | 2004 | match | [Robust query processing through progressive optimization](https://doi.org/10.1145/1007568.1007642) |
| DBLP | 1.000 | 0.833 | 2004 | match | [Robust Query Processing through Progressive Optimization](https://dblp.org/rec/conf/sigmod/MarklRSLP04) |
| Crossref | 0.660 | 0.000 | None | conflict | [Logical Query Processing and Optimization](https://doi.org/10.1007/springerreference_65236) |
| Crossref | 0.660 | 0.000 | None | conflict | [Datalog Query Processing and Optimization](https://doi.org/10.1007/springerreference_64761) |

### 14. REVIEW - kabra1998reoptimization

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Efficient Mid-Query Re-Optimization of Sub-Optimal Query Execution Plans
- Supplied authors: N. Kabra, D. J. DeWitt
- Supplied year: 1998
- Supplied DOI: `10.1145/276304.276315`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1998 | match | [Efficient mid-query re-optimization of sub-optimal query execution plans](https://doi.org/10.1145/276304.276315) |
| Crossref | 1.000 | 1.000 | 1998 | match | [Efficient mid-query re-optimization of sub-optimal query execution plans](https://doi.org/10.1145/276304.276315) |
| DBLP | 1.000 | 1.000 | 1998 | match | [Efficient Mid-Query Re-Optimization of Sub-Optimal Query Execution Plans](https://dblp.org/rec/conf/sigmod/KabraD98) |
| Crossref | 1.000 | 1.000 | 1998 | conflict | [Efficient mid-query re-optimization of sub-optimal query execution plans](https://doi.org/10.1145/276305.276315) |
| Crossref | 0.544 | 0.000 | 2019 | conflict | [Turning On and Using Query Execution Plans](https://doi.org/10.1007/978-1-4842-5144-7_3) |

### 15. REVIEW - deshpande2007adaptive

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Adaptive Query Processing
- Supplied authors: A. Deshpande, Z. Ives, V. Raman
- Supplied year: 2007
- Supplied DOI: `10.1561/1900000001`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 404: Not Found; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2007 | match | [Adaptive Query Processing](https://doi.org/10.1561/1900000001) |
| Crossref | 1.000 | 1.000 | 2007 | conflict | [Adaptive Query Processing](https://doi.org/10.1561/9781601980359) |
| Crossref | 1.000 | 0.000 | None | conflict | [Adaptive Query Processing](https://doi.org/10.1007/springerreference_63891) |
| Crossref | 1.000 | 0.000 | 2016 | conflict | [Adaptive Query Processing](https://doi.org/10.1007/978-1-4899-7993-3_865-2) |
| DBLP | 0.676 | 0.000 | 2013 | conflict | [Adaptive Query Processing in Distributed Settings](https://dblp.org/rec/series/isrl/GounarisTM13) |

### 16. REVIEW - avnur2000eddies

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Eddies: Continuously Adaptive Query Processing
- Supplied authors: R. Avnur, J. M. Hellerstein
- Supplied year: 2000
- Supplied DOI: `10.1145/342009.335420`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2000 | match | [Eddies: continuously adaptive query processing](https://doi.org/10.1145/342009.335420) |
| DBLP | 1.000 | 1.000 | 2000 | match | [Eddies: Continuously Adaptive Query Processing](https://dblp.org/rec/conf/sigmod/HellersteinA00) |
| Crossref | 0.235 | 1.000 | 2000 | match | [Eddies](https://doi.org/10.1145/342009.335420) |
| Crossref | 0.714 | 0.000 | None | conflict | [Adaptive Query Processing](https://doi.org/10.1007/springerreference_63891) |
| Crossref | 0.714 | 0.000 | 2007 | conflict | [Adaptive Query Processing](https://doi.org/10.1561/9781601980359) |

### 17. REVIEW - ives1999tukwila

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: An Adaptive Query Execution System for Data Integration
- Supplied authors: Z. G. Ives, D. Florescu, M. Friedman, A. Levy, D. S. Weld
- Supplied year: 1999
- Supplied DOI: `10.1145/304181.304209`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 404: Not Found

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1999 | match | [An adaptive query execution system for data integration](https://doi.org/10.1145/304181.304209) |
| Crossref | 1.000 | 1.000 | 1999 | match | [An adaptive query execution system for data integration](https://doi.org/10.1145/304181.304209) |
| Crossref | 1.000 | 1.000 | 1999 | conflict | [An adaptive query execution system for data integration](https://doi.org/10.1145/304182.304209) |
| DBLP | 1.000 | 1.000 | 1999 | conflict | [An Adaptive Query Execution System for Data Integration](https://dblp.org/rec/conf/sigmod/IvesFFLW99) |
| Crossref | 0.716 | 0.000 | 2010 | conflict | [Adaptive query execution for data management in the cloud](https://doi.org/10.1145/1871929.1871933) |

### 18. REVIEW - cole1994optimization

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Optimization of Dynamic Query Evaluation Plans
- Supplied authors: R. L. Cole, G. Graefe
- Supplied year: 1994
- Supplied DOI: `10.1145/191839.191872`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1994 | match | [Optimization of dynamic query evaluation plans](https://doi.org/10.1145/191839.191872) |
| Crossref | 1.000 | 1.000 | 1994 | match | [Optimization of dynamic query evaluation plans](https://doi.org/10.1145/191839.191872) |
| Semantic Scholar DOI | 1.000 | 1.000 | 1994 | match | [Optimization of dynamic query evaluation plans](https://www.semanticscholar.org/paper/a71d88bb81df4a0841bb5b06dbbe0835fa75876a) |
| Semantic Scholar | 1.000 | 1.000 | 1994 | match | [Optimization of dynamic query evaluation plans](https://www.semanticscholar.org/paper/a71d88bb81df4a0841bb5b06dbbe0835fa75876a) |
| DBLP | 1.000 | 1.000 | 1994 | match | [Optimization of Dynamic Query Evaluation Plans](https://dblp.org/rec/conf/sigmod/ColeG94) |

### 19. REVIEW - galindo1997outerjoin

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Outerjoin Simplification and Reordering for Query Optimization
- Supplied authors: Cesar A. Galindo-Legaria, Arnon Rosenthal
- Supplied year: 1997
- Supplied DOI: `10.1145/244810.244812`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1997 | match | [Outerjoin simplification and reordering for query optimization](https://doi.org/10.1145/244810.244812) |
| Crossref | 1.000 | 1.000 | 1997 | match | [Outerjoin simplification and reordering for query optimization](https://doi.org/10.1145/244810.244812) |
| DBLP | 1.000 | 1.000 | 1997 | match | [Outerjoin Simplification and Reordering for Query Optimization](https://dblp.org/rec/journals/tods/Galindo-LegariaR97) |
| Crossref | 0.645 | 0.000 | 2017 | conflict | [Distance-Based Triple Reordering for SPARQL Query Optimization](https://doi.org/10.1109/icde.2017.227) |
| Crossref | 0.500 | 0.000 | 1996 | conflict | [SQL query optimization](https://doi.org/10.1145/235968.233318) |

### 20. REVIEW - neumann2011efficient

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Efficiently Compiling Efficient Query Plans for Modern Hardware
- Supplied authors: T. Neumann
- Supplied year: 2011
- Supplied DOI: `10.14778/2002938.2002940`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2011 | match | [Efficiently compiling efficient query plans for modern hardware](https://doi.org/10.14778/2002938.2002940) |
| Crossref | 1.000 | 1.000 | 2011 | match | [Efficiently compiling efficient query plans for modern hardware](https://doi.org/10.14778/2002938.2002940) |
| DBLP | 1.000 | 1.000 | 2011 | match | [Efficiently Compiling Efficient Query Plans for Modern Hardware](https://dblp.org/rec/journals/pvldb/Neumann11) |
| Crossref | 0.603 | 0.000 | None | conflict | [Efficiently ordering query plans for data integration](https://doi.org/10.1109/icde.2002.994753) |
| Crossref | 0.569 | 0.000 | 2017 | conflict | [Many-query join: efficient shared execution of relational joins on modern hardware](https://doi.org/10.1007/s00778-017-0475-4) |

### 21. REVIEW - armbrust2015spark

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Spark SQL: Relational Data Processing in Spark
- Supplied authors: Michael Armbrust, Reynold S. Xin, Cheng Lian, Yin Huai, Davies Liu, Joseph K. Bradley, Xiangrui Meng, Tomer Kaftan, Michael J. Franklin, Ali Ghodsi, Matei Zaharia
- Supplied year: 2015
- Supplied DOI: `10.1145/2723372.2742797`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2015 | match | [Spark SQL: Relational Data Processing in Spark](https://doi.org/10.1145/2723372.2742797) |
| DBLP | 1.000 | 1.000 | 2015 | match | [Spark SQL: Relational Data Processing in Spark](https://dblp.org/rec/conf/sigmod/ArmbrustXLHLBMK15) |
| Crossref | 0.333 | 1.000 | 2015 | match | [Spark SQL](https://doi.org/10.1145/2723372.2742797) |
| Crossref | 0.485 | 0.000 | 2018 | conflict | [Spark SQL (Foundations)](https://doi.org/10.1007/978-1-4842-3579-9_4) |
| Crossref | 0.462 | 0.000 | 2021 | conflict | [Spark SQL: Foundation](https://doi.org/10.1007/978-1-4842-7383-8_3) |

### 22. REVIEW - begoli2018calcite

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Apache Calcite: A Foundational Framework for Optimized Query Processing Over Heterogeneous Data Sources
- Supplied authors: E. Begoli, J. Camacho-Rodriguez, J. Hyde, M. J. Mior, D. Lemire
- Supplied year: 2018
- Supplied DOI: `10.1145/3183713.3190662`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2018 | match | [Apache Calcite: A Foundational Framework for Optimized Query Processing Over Heterogeneous Data Sources](https://doi.org/10.1145/3183713.3190662) |
| DBLP | 1.000 | 1.000 | 2018 | match | [Apache Calcite: A Foundational Framework for Optimized Query Processing Over Heterogeneous Data Sources](https://dblp.org/rec/conf/sigmod/BegoliCHML18) |
| Crossref | 0.241 | 1.000 | 2018 | match | [Apache Calcite](https://doi.org/10.1145/3183713.3190662) |
| DBLP | 1.000 | 1.000 | 2018 | n/a | [Apache Calcite: A Foundational Framework for Optimized Query Processing Over Heterogeneous Data Sources](https://dblp.org/rec/journals/corr/abs-1802-10233) |
| Crossref | 0.700 | 0.000 | 2015 | conflict | [A Unified Framework for Flexible Query Answering over Heterogeneous Data Sources](https://doi.org/10.1007/978-3-319-26154-6_22) |

### 23. REVIEW - soliman2014orca

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Orca: A Modular Query Optimizer Architecture for Big Data
- Supplied authors: Mohamed A. Soliman, Lyublena Antova, Venkatesh Raghavan, Amr El-Helw, Zhongxian Gu, Entong Shen, George C. Caragea, Carlos Garcia-Alvarado, Foyzur Rahman, Michalis Petropoulos, Florian Waas, Sivaramakrishnan Narayanan, Konstantinos Krikellas, Rhonda Baldwin
- Supplied year: 2014
- Supplied DOI: `10.1145/2588555.2595637`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2014 | match | [Orca: a modular query optimizer architecture for big data](https://doi.org/10.1145/2588555.2595637) |
| DBLP | 1.000 | 1.000 | 2014 | match | [Orca: a modular query optimizer architecture for big data](https://dblp.org/rec/conf/sigmod/SolimanAREGSCGRPWNKB14) |
| Crossref | 0.133 | 1.000 | 2014 | match | [Orca](https://doi.org/10.1145/2588555.2595637) |
| Crossref | 0.629 | 0.000 | None | conflict | [A modular query optimizer generator](https://doi.org/10.1109/icde.1990.113464) |
| Crossref | 0.619 | 0.000 | 1997 | conflict | [ModParOpt: a Modular Query Optimizer for Multi-query Parallel Databases](https://doi.org/10.14236/ewic/adbis1997.7) |

### 24. REVIEW - melnik2010dremel

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Dremel: Interactive Analysis of Web-Scale Datasets
- Supplied authors: Sergey Melnik, Andrey Gubarev, Jing Jing Long, Geoffrey Romer, Shiva Shivakumar, Matt Tolton, Theo Vassilakis
- Supplied year: 2010
- Supplied DOI: `10.14778/1920841.1920886`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2010 | match | [Dremel: interactive analysis of web-scale datasets](https://doi.org/10.14778/1920841.1920886) |
| DBLP | 1.000 | 1.000 | 2010 | match | [Dremel: Interactive Analysis of Web-Scale Datasets](https://dblp.org/rec/journals/pvldb/MelnikGLRSTV10) |
| Crossref | 0.218 | 1.000 | 2010 | match | [Dremel](https://doi.org/10.14778/1920841.1920886) |
| Semantic Scholar DOI | 0.218 | 1.000 | 2010 | match | [Dremel](https://www.semanticscholar.org/paper/4543690861cb95c3d220ee53df09b7c84f10ac1f) |
| Semantic Scholar | 1.000 | 1.000 | 2010 | n/a | [Dremel: Interactive Analysis of Web-Scale Datasets](https://www.semanticscholar.org/paper/03363ed04e9d4d2e8c9348551815e80615969611) |

### 25. REVIEW - dageville2016snowflake

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: The Snowflake Elastic Data Warehouse
- Supplied authors: Benoit Dageville, Thierry Cruanes, Marcin Zukowski, Vadim Antonov, Artin Avanes, Jon Bock, Jonathan Claybaugh, Daniel Engovatov, Martin Hentschel, Jiansheng Huang, Allison W. Lee, Ashish Motivala, Abdul Q. Munir, Steven Pelley, Peter Povinec, Greg Rahn, Spyridon Triantafyllis, Philipp Unterbrunner
- Supplied year: 2016
- Supplied DOI: `10.1145/2882903.2903741`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2016 | match | [The Snowflake Elastic Data Warehouse](https://doi.org/10.1145/2882903.2903741) |
| Semantic Scholar DOI | 1.000 | 1.000 | 2016 | match | [The Snowflake Elastic Data Warehouse](https://www.semanticscholar.org/paper/00a2aeb87287d59eaf118e96f0cdbb622a7fec42) |
| Semantic Scholar | 1.000 | 1.000 | 2016 | match | [The Snowflake Elastic Data Warehouse](https://www.semanticscholar.org/paper/00a2aeb87287d59eaf118e96f0cdbb622a7fec42) |
| DBLP | 1.000 | 1.000 | 2016 | match | [The Snowflake Elastic Data Warehouse](https://dblp.org/rec/conf/sigmod/DagevilleCZAABC16) |
| Crossref | 0.426 | 0.000 | 2017 | conflict | [Transformation of Data Warehouse Using Snowflake Scheme Method](https://doi.org/10.5013/ijssst.a.17.35.16) |

### 26. REVIEW - raasveldt2019duckdb

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: DuckDB: An Embeddable Analytical Database
- Supplied authors: M. Raasveldt, H. Muehleisen
- Supplied year: 2019
- Supplied DOI: `10.1145/3299869.3320212`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; arXiv: TimeoutError: The read operation timed out

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 0.500 | 2019 | match | [DuckDB: an Embeddable Analytical Database](https://doi.org/10.1145/3299869.3320212) |
| DBLP | 1.000 | 0.500 | 2019 | match | [DuckDB: an Embeddable Analytical Database](https://dblp.org/rec/conf/sigmod/RaasveldtM19) |
| Crossref | 0.261 | 0.500 | 2019 | match | [DuckDB](https://doi.org/10.1145/3299869.3320212) |
| Crossref | 0.492 | 0.000 | 2024 | conflict | [DuckDB vs dplyr vs base R](https://doi.org/10.59350/q6650-vdq47) |
| Crossref | 0.440 | 0.500 | 2020 | conflict | [duckdb: DBI Package for the DuckDB Database Management System](https://doi.org/10.32614/cran.package.duckdb) |

### 27. REVIEW - boncz2005monetdb

- Verdict: Single-source strong match
- Supplied title: MonetDB/X100: Hyper-Pipelining Query Execution
- Supplied authors: P. A. Boncz, M. Zukowski, N. Nes
- Supplied year: 2005
- Supplied URL: https://www.cidrdb.org/cidr2005/papers/P19.pdf
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 2005 | n/a | [MonetDB/X100: Hyper-Pipelining Query Execution](https://dblp.org/rec/conf/cidr/BonczZN05) |
| Crossref | 0.703 | 0.000 | None | n/a | [Pipelining in query execution](https://doi.org/10.1109/parbse.1990.77227) |
| Crossref | 0.556 | 0.000 | None | n/a | [Partitioned Query Execution](https://doi.org/10.1007/springerreference_65467) |
| Crossref | 0.462 | 0.000 | None | n/a | [Query Execution Plan](https://doi.org/10.1007/springerreference_65581) |
| Crossref | 0.448 | 0.000 | None | n/a | [Query Execution Engine](https://doi.org/10.1007/springerreference_65579) |

### 28. REVIEW - gupta2015redshift

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Amazon Redshift and the Case for Simpler Data Warehouses
- Supplied authors: Anurag Gupta, Deepak Agarwal, Derek Tan, Jakub Kulesza, Rahul Pathak, Stefano Stefani, Vidhya Srinivasan
- Supplied year: 2015
- Supplied DOI: `10.1145/2723372.2742795`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2015 | match | [Amazon Redshift and the Case for Simpler Data Warehouses](https://doi.org/10.1145/2723372.2742795) |
| Crossref | 1.000 | 1.000 | 2015 | match | [Amazon Redshift and the Case for Simpler Data Warehouses](https://doi.org/10.1145/2723372.2742795) |
| DBLP | 1.000 | 1.000 | 2015 | match | [Amazon Redshift and the Case for Simpler Data Warehouses](https://dblp.org/rec/conf/sigmod/GuptaATKPSS15) |
| Crossref | 0.557 | 0.000 | 2016 | conflict | [Amazon Redshift : Avoid data redistribution](https://doi.org/10.59350/pj1vz-fz749) |
| Crossref | 0.557 | 0.000 | 2016 | conflict | [Amazon Redshift : Avoid data redistribution](https://doi.org/10.59350/tybv4-sw356) |

### 29. REVIEW - shute2013f1

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: F1: A Distributed SQL Database That Scales
- Supplied authors: Jeff Shute, Radek Vingralek, Bart Samwel, Ben Handy, Chad Whipkey, Eric Rollins, Mircea Oancea, Kyle Littlefield, David Menestrina, Stephan Ellner, John Cieslewicz, Ian Rae, Traian Stancescu, Himani Apte
- Supplied year: 2013
- Supplied DOI: `10.14778/2536222.2536232`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2013 | match | [F1: a distributed SQL database that scales](https://doi.org/10.14778/2536222.2536232) |
| DBLP | 1.000 | 1.000 | 2013 | match | [F1: A Distributed SQL Database That Scales](https://dblp.org/rec/journals/pvldb/ShuteVSHWROLMECRSA13) |
| Crossref | 0.093 | 1.000 | 2013 | match | [F1](https://doi.org/10.14778/2536222.2536232) |
| Crossref | 0.694 | 0.000 | 2015 | conflict | [10. Distributed Database Systems](https://doi.org/10.1515/9783110441413-014) |
| Crossref | 0.494 | 0.000 | 2015 | conflict | [2. Relational Database Management Systems](https://doi.org/10.1515/9783110441413-006) |

### 30. REVIEW - zaharia2012resilient

- Verdict: Single-source strong match
- Supplied title: Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing
- Supplied authors: Matei Zaharia, Mosharaf Chowdhury, Tathagata Das, Ankur Dave, Justin Ma, Murphy McCauley, Michael J. Franklin, Scott Shenker, Ion Stoica
- Supplied year: 2012
- Supplied URL: https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 0.889 | 2012 | n/a | [Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing](https://dblp.org/rec/conf/nsdi/ZahariaCDDMMFSS12) |
| Crossref | 0.528 | 0.000 | None | n/a | [Bibliography for fault-tolerant distributed computing](https://doi.org/10.1007/bfb0042342) |
| Crossref | 0.520 | 0.000 | None | n/a | [The “Engineering” of fault-tolerant distributed computing systems](https://doi.org/10.1007/bfb0042341) |
| Crossref | 0.489 | 0.000 | None | n/a | [Auditable register : a basic abstraction for privacy by design fault-tolerant distributed computing](https://doi.org/10.70675/29960b54z0592z4a27za0fez6a71b0f3e8d9) |
| Crossref | 0.448 | 0.000 | 2019 | n/a | [Gossip based fault tolerant protocol in distributed transactional memory using quorum based replication system](https://doi.org/10.1007/s10586-019-02973-7) |

### 31. REVIEW - chu2017cosette

- Verdict: Single-source strong match
- Supplied title: Cosette: An Automated Prover for SQL
- Supplied authors: S. Chu, C. Wang, K. Weitz, A. Cheung
- Supplied year: 2017
- Supplied URL: https://www.cidrdb.org/cidr2017/papers/p51-chu-cidr17.pdf
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 2017 | n/a | [Cosette: An Automated Prover for SQL](https://dblp.org/rec/conf/cidr/ChuWWC17) |
| Crossref | 0.571 | 0.750 | 2017 | n/a | [Demonstration of the Cosette Automated SQL Prover](https://doi.org/10.1145/3035918.3058728) |
| Crossref | 0.571 | 0.250 | 2009 | n/a | [Automated Theorem Prover for Pointer Logic](https://doi.org/10.3724/sp.j.1001.2009.00572) |
| Crossref | 0.471 | 0.000 | None | n/a | [Designing an Automated Concurrent Tableau-Based Theorem Prover for First-Order Logic](https://doi.org/10.70675/b8a908cfzea79z4efdza9dezd3589d30dd25) |
| Crossref | 0.436 | 0.000 | 2001 | n/a | [Theo:A Resolution—Refutation Theorem Prover](https://doi.org/10.1007/978-1-4613-0089-2_9) |

### 32. REVIEW - chu2018usemiring

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Axiomatic Foundations and Algorithms for Deciding Semantic Equivalences of SQL Queries
- Supplied authors: S. Chu, B. Murphy, J. Roesch, A. Cheung, D. Suciu
- Supplied year: 2018
- Supplied DOI: `10.14778/3236187.3236200`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2018 | match | [Axiomatic foundations and algorithms for deciding semantic equivalences of SQL queries](https://doi.org/10.14778/3236187.3236200) |
| Crossref | 1.000 | 1.000 | 2018 | match | [Axiomatic foundations and algorithms for deciding semantic equivalences of SQL queries](https://doi.org/10.14778/3236187.3236200) |
| DBLP | 1.000 | 1.000 | 2018 | match | [Axiomatic Foundations and Algorithms for Deciding Semantic Equivalences of SQL Queries](https://dblp.org/rec/journals/pvldb/ChuMRCS18) |
| arXiv title | 1.000 | 1.000 | 2018 | n/a | [Axiomatic Foundations and Algorithms for Deciding Semantic Equivalences of SQL Queries](http://arxiv.org/abs/1802.02229v3) |
| DBLP | 1.000 | 0.600 | 2018 | n/a | [Axiomatic Foundations and Algorithms for Deciding Semantic Equivalences of SQL Queries](https://dblp.org/rec/journals/corr/abs-1802-02229) |

### 33. REVIEW - wang2024qed

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: QED: A Powerful Query Equivalence Decider for SQL
- Supplied authors: S. Wang, S. Pan, A. Cheung
- Supplied year: 2024
- Supplied DOI: `10.14778/3681954.3682024`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2024 | match | [QED: A Powerful Query Equivalence Decider for SQL](https://doi.org/10.14778/3681954.3682024) |
| Crossref | 1.000 | 1.000 | 2024 | match | [QED: A Powerful Query Equivalence Decider for SQL](https://doi.org/10.14778/3681954.3682024) |
| DBLP | 1.000 | 1.000 | 2024 | match | [QED: A Powerful Query Equivalence Decider for SQL](https://dblp.org/rec/journals/pvldb/WangPC24) |
| Crossref | 0.436 | 0.000 | 2009 | conflict | [SQL Query Performance Analysis](https://doi.org/10.1007/978-1-4302-1903-3_3) |
| Crossref | 0.436 | 0.000 | 2012 | conflict | [SQL Query Performance Analysis](https://doi.org/10.1007/978-1-4302-4204-8_3) |

### 34. REVIEW - rigger2020norec

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Detecting Optimization Bugs in Database Engines via Non-Optimizing Reference Engine Construction
- Supplied authors: M. Rigger, Z. Su
- Supplied year: 2020
- Supplied DOI: `10.1145/3368089.3409710`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2020 | match | [Detecting optimization bugs in database engines via non-optimizing reference engine construction](https://doi.org/10.1145/3368089.3409710) |
| Crossref | 1.000 | 1.000 | 2020 | match | [Detecting optimization bugs in database engines via non-optimizing reference engine construction](https://doi.org/10.1145/3368089.3409710) |
| DBLP | 1.000 | 1.000 | 2020 | match | [Detecting optimization bugs in database engines via non-optimizing reference engine construction](https://dblp.org/rec/conf/sigsoft/RiggerS20) |
| DBLP | 1.000 | 1.000 | 2020 | n/a | [Detecting Optimization Bugs in Database Engines via Non-Optimizing Reference Engine Construction](https://dblp.org/rec/journals/corr/abs-2007-08292) |
| arXiv title | 1.000 | 1.000 | 2020 | n/a | [Detecting Optimization Bugs in Database Engines via Non-Optimizing Reference Engine Construction](http://arxiv.org/abs/2007.08292v1) |

### 35. REVIEW - rigger2020sqlancer

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Testing Database Engines via Pivoted Query Synthesis
- Supplied authors: Manuel Rigger, Zhendong Su
- Supplied year: 2020
- Supplied URL: https://www.usenix.org/conference/osdi20/presentation/rigger
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 2020 | n/a | [Testing Database Engines via Pivoted Query Synthesis](https://dblp.org/rec/conf/osdi/RiggerS20) |
| DBLP | 1.000 | 1.000 | 2020 | n/a | [Testing Database Engines via Pivoted Query Synthesis](https://dblp.org/rec/journals/corr/abs-2001-04174) |
| arXiv title | 1.000 | 1.000 | 2020 | n/a | [Testing Database Engines via Pivoted Query Synthesis](http://arxiv.org/abs/2001.04174v1) |
| Crossref | 0.740 | 0.500 | 2023 | n/a | [Testing Database Engines via Query Plan Guidance](https://doi.org/10.1109/icse48619.2023.00174) |
| Crossref | 0.705 | 1.000 | 2023 | n/a | [Testing Graph Database Engines via Query Partitioning](https://doi.org/10.1145/3597926.3598044) |

### 36. REVIEW - slutz1998massive

- Verdict: Single-source strong match
- Supplied title: Massive Stochastic Testing of SQL
- Supplied authors: Donald R. Slutz
- Supplied year: 1998
- Supplied URL: https://www.vldb.org/conf/1998/p618.pdf
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 1998 | n/a | [Massive Stochastic Testing of SQL](https://dblp.org/rec/conf/vldb/Slutz98) |
| Crossref | 0.448 | 0.000 | 2009 | n/a | [Testing for SQL Injection](https://doi.org/10.1016/b978-1-59749-424-3.00002-5) |
| Crossref | 0.448 | 0.000 | 2012 | n/a | [Testing for SQL Injection](https://doi.org/10.1016/b978-1-59-749963-7.00002-5) |
| Crossref | 0.423 | 0.000 | 2011 | n/a | [PL/SQL Unit Testing](https://doi.org/10.1007/978-1-4302-3486-9_5) |
| Crossref | 0.350 | 0.000 | 2020 | n/a | [Testing](https://doi.org/10.1007/978-1-4842-5590-2_11) |

### 37. FAIL - sqlsmith

- Verdict: Unverifiable under fail-closed policy
- Supplied title: SQLsmith: Randomized SQL Testing
- Supplied authors: Andreas Seltenreich
- Supplied year: 2015
- Supplied URL: https://github.com/anse1/sqlsmith
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 0.568 | 0.000 | 2015 | n/a | [anse1/sqlsmith: A random SQL query generator](https://github.com/anse1/sqlsmith) |
| Crossref | 0.520 | 0.000 | 2011 | n/a | [PL/SQL Unit Testing](https://doi.org/10.1007/978-1-4302-3486-9_5) |
| Crossref | 0.368 | 0.000 | 2020 | n/a | [Testing](https://doi.org/10.1007/978-1-4842-5590-2_11) |
| Crossref | 0.368 | 0.000 | 2023 | n/a | [Testing](https://doi.org/10.1007/978-1-4842-9256-3_11) |
| Crossref | 0.250 | 0.000 | 2009 | n/a | [Testing for SQL Injection](https://doi.org/10.1016/b978-1-59749-424-3.00002-5) |

### 38. REVIEW - chandra1977optimal

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Optimal Implementation of Conjunctive Queries in Relational Data Bases
- Supplied authors: A. K. Chandra, P. M. Merlin
- Supplied year: 1977
- Supplied DOI: `10.1145/800105.803397`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1977 | match | [Optimal implementation of conjunctive queries in relational data bases](https://doi.org/10.1145/800105.803397) |
| Crossref | 1.000 | 1.000 | 1977 | match | [Optimal implementation of conjunctive queries in relational data bases](https://doi.org/10.1145/800105.803397) |
| Semantic Scholar DOI | 1.000 | 1.000 | 1977 | match | [Optimal implementation of conjunctive queries in relational data bases](https://www.semanticscholar.org/paper/fac319a34a9a1b93cb772d4cdb42cdb8741f2edc) |
| Semantic Scholar | 1.000 | 1.000 | 1977 | match | [Optimal implementation of conjunctive queries in relational data bases](https://www.semanticscholar.org/paper/fac319a34a9a1b93cb772d4cdb42cdb8741f2edc) |
| DBLP | 1.000 | 1.000 | 1977 | match | [Optimal Implementation of Conjunctive Queries in Relational Data Bases](https://dblp.org/rec/conf/stoc/ChandraM77) |

### 39. REVIEW - aho1979equivalences

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Equivalences among Relational Expressions
- Supplied authors: A. V. Aho, Y. Sagiv, J. D. Ullman
- Supplied year: 1979
- Supplied DOI: `10.1137/0208017`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 1979 | match | [Equivalences among Relational Expressions](https://doi.org/10.1137/0208017) |
| Crossref | 1.000 | 1.000 | 1979 | match | [Equivalences among Relational Expressions](https://doi.org/10.1137/0208017) |
| DBLP | 1.000 | 1.000 | 1979 | match | [Equivalences Among Relational Expressions](https://dblp.org/rec/journals/siamcomp/AhoSU79) |
| Crossref | 0.828 | 0.000 | 1994 | conflict | [Algebraic equivalences among nested relational expressions](https://doi.org/10.1145/191246.191287) |
| DBLP | 0.828 | 0.000 | 1994 | conflict | [Algebraic Equivalences Among Nested Relational Expressions](https://dblp.org/rec/conf/cikm/LiuR94) |

### 40. REVIEW - green2007provenance

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Provenance Semirings
- Supplied authors: T. J. Green, G. Karvounarakis, V. Tannen
- Supplied year: 2007
- Supplied DOI: `10.1145/1265530.1265535`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 404: Not Found

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2007 | match | [Provenance semirings](https://doi.org/10.1145/1265530.1265535) |
| Crossref | 1.000 | 1.000 | 2007 | match | [Provenance semirings](https://doi.org/10.1145/1265530.1265535) |
| DBLP | 1.000 | 1.000 | 2007 | match | [Provenance semirings](https://dblp.org/rec/conf/pods/GreenKT07) |
| Crossref | 0.481 | 0.000 | None | conflict | [Pre-Semirings, Semirings and Dioids](https://doi.org/10.1007/978-0-387-75450-5_1) |
| Crossref | 0.471 | 0.000 | 2019 | conflict | [Querying Attributed DL-Lite Ontologies Using Provenance Semirings](https://doi.org/10.1609/aaai.v33i01.33012719) |

### 41. REVIEW - buneman2001why

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Why and Where: A Characterization of Data Provenance
- Supplied authors: P. Buneman, S. Khanna, W.-C. Tan
- Supplied year: 2001
- Supplied DOI: `10.1007/3-540-44503-x_20`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 2001 | match | [Why and Where: A Characterization of Data Provenance](https://dblp.org/rec/conf/icdt/BunemanKT01) |
| Crossref DOI | 1.000 | 0.667 | 2001 | match | [Why and Where: A Characterization of Data Provenance](https://doi.org/10.1007/3-540-44503-x_20) |
| Crossref | 1.000 | 0.667 | 2001 | match | [Why and Where: A Characterization of Data Provenance](https://doi.org/10.1007/3-540-44503-x_20) |
| Crossref | 0.529 | 0.000 | None | conflict | [Semantic Interoperability and Characterization of Data Provenance in Computational Molecular Engineering](https://doi.org/10.1021/acs.jced.9b00739.s006) |
| Crossref | 0.529 | 0.000 | None | conflict | [Semantic Interoperability and Characterization of Data Provenance in Computational Molecular Engineering](https://doi.org/10.1021/acs.jced.9b00739.s002) |

### 42. REVIEW - cheney2009provenance

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Provenance in Databases: Why, How, and Where
- Supplied authors: J. Cheney, L. Chiticariu, W.-C. Tan
- Supplied year: 2009
- Supplied DOI: `10.1561/1900000006`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2009 | match | [Provenance in Databases: Why, How, and Where](https://doi.org/10.1561/1900000006) |
| Crossref | 1.000 | 1.000 | 2009 | match | [Provenance in Databases: Why, How, and Where](https://doi.org/10.1561/1900000006) |
| DBLP | 1.000 | 1.000 | 2009 | match | [Provenance in Databases: Why, How, and Where](https://dblp.org/rec/journals/ftdb/CheneyCT09) |
| Crossref | 1.000 | 1.000 | 2007 | conflict | [Provenance in Databases: Why, How, and Where](https://doi.org/10.1561/9781601982339) |
| Crossref | 0.613 | 0.000 | None | conflict | [Provenance in Scientific Databases](https://doi.org/10.1007/springerreference_63406) |

### 43. REVIEW - green2011containment

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Containment of Conjunctive Queries on Annotated Relations
- Supplied authors: T. J. Green
- Supplied year: 2011
- Supplied DOI: `10.1007/s00224-011-9327-6`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2011 | match | [Containment of Conjunctive Queries on Annotated Relations](https://doi.org/10.1007/s00224-011-9327-6) |
| Crossref | 1.000 | 1.000 | 2011 | match | [Containment of Conjunctive Queries on Annotated Relations](https://doi.org/10.1007/s00224-011-9327-6) |
| DBLP | 1.000 | 1.000 | 2011 | match | [Containment of Conjunctive Queries on Annotated Relations](https://dblp.org/rec/journals/mst/Green11) |
| Crossref | 1.000 | 1.000 | 2009 | conflict | [Containment of conjunctive queries on annotated relations](https://doi.org/10.1145/1514894.1514930) |
| DBLP | 1.000 | 1.000 | 2009 | conflict | [Containment of conjunctive queries on annotated relations](https://dblp.org/rec/conf/icdt/Green09) |

### 44. REVIEW - han2021cardest

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Cardinality Estimation in DBMS: A Comprehensive Benchmark Evaluation
- Supplied authors: Yuxing Han, Ziniu Wu, Peizhi Wu, Rong Zhu, Jingyi Yang, Liang Wei Tan, Kai Zeng, Gao Cong, Yanzhao Qin, Andreas Pfadler, Zhengping Qian, Jingren Zhou, Jiangneng Li, Bin Cui
- Supplied year: 2021
- Supplied DOI: `10.14778/3503585.3503586`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: DataCite: HTTPError: HTTP Error 404: Not Found; OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2021 | match | [Cardinality estimation in DBMS: a comprehensive benchmark evaluation](https://doi.org/10.14778/3503585.3503586) |
| DBLP | 1.000 | 1.000 | 2021 | match | [Cardinality Estimation in DBMS: A Comprehensive Benchmark Evaluation](https://dblp.org/rec/journals/pvldb/HanWWZYTZCQPQZL21) |
| Crossref | 0.619 | 1.000 | 2021 | match | [Cardinality estimation in DBMS](https://doi.org/10.14778/3503585.3503586) |
| DBLP | 1.000 | 1.000 | 2021 | n/a | [Cardinality Estimation in DBMS: A Comprehensive Benchmark Evaluation](https://dblp.org/rec/journals/corr/abs-2109-05877) |
| arXiv title | 1.000 | 1.000 | 2021 | n/a | [Cardinality Estimation in DBMS: A Comprehensive Benchmark Evaluation](http://arxiv.org/abs/2109.05877v3) |

### 45. REVIEW - kipf2019learned

- Verdict: Single-source strong match
- Supplied title: Learned Cardinalities: Estimating Correlated Joins with Deep Learning
- Supplied authors: Andreas Kipf, Thomas Kipf, Bernhard Radke, Viktor Leis, Peter Boncz, Alfons Kemper
- Supplied year: 2019
- Supplied URL: https://www.cidrdb.org/cidr2019/papers/p101-kipf-cidr19.pdf
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 2019 | n/a | [Learned Cardinalities: Estimating Correlated Joins with Deep Learning](https://dblp.org/rec/conf/cidr/KipfKRLBK19) |
| DBLP | 1.000 | 1.000 | 2018 | n/a | [Learned Cardinalities: Estimating Correlated Joins with Deep Learning](https://dblp.org/rec/journals/corr/abs-1809-00677) |
| arXiv title | 1.000 | 1.000 | 2018 | n/a | [Learned Cardinalities: Estimating Correlated Joins with Deep Learning](http://arxiv.org/abs/1809.00677v2) |
| Crossref | 0.523 | 1.000 | 2019 | n/a | [Estimating Cardinalities with Deep Sketches](https://doi.org/10.1145/3299869.3320218) |
| Crossref | 0.403 | 0.000 | 2009 | n/a | [Order statistics and estimating cardinalities of massive data sets](https://doi.org/10.1016/j.dam.2008.06.020) |

### 46. REVIEW - yang2019neurocard

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Deep Unsupervised Cardinality Estimation
- Supplied authors: Z. Yang, E. Liang, A. Kamsetty, C. Wu, Y. Duan, X. Chen, P. Abbeel, J. M. Hellerstein, S. Krishnan, I. Stoica
- Supplied year: 2019
- Supplied DOI: `10.14778/3368289.3368294`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2019 | match | [Deep unsupervised cardinality estimation](https://doi.org/10.14778/3368289.3368294) |
| Crossref | 1.000 | 1.000 | 2019 | match | [Deep unsupervised cardinality estimation](https://doi.org/10.14778/3368289.3368294) |
| DBLP | 1.000 | 1.000 | 2019 | match | [Deep Unsupervised Cardinality Estimation](https://dblp.org/rec/journals/pvldb/YangLKWDCAHKS19) |
| arXiv title | 1.000 | 1.000 | 2019 | n/a | [Deep Unsupervised Cardinality Estimation](http://arxiv.org/abs/1905.04278v2) |
| Crossref | 0.814 | 0.000 | 2022 | conflict | [Unsupervised Model with Cardinality Estimation](https://doi.org/10.1109/scset55041.2022.00056) |

### 47. REVIEW - hilprecht2020deepdb

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: DeepDB: Learn from Data, Not from Queries!
- Supplied authors: B. Hilprecht, A. Schmidt, M. Kulessa, A. Molina, K. Kersting, C. Binnig
- Supplied year: 2020
- Supplied DOI: `10.14778/3384345.3384349`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2020 | match | [DeepDB: learn from data, not from queries!](https://doi.org/10.14778/3384345.3384349) |
| DBLP | 1.000 | 1.000 | 2020 | match | [DeepDB: Learn from Data, not from Queries!](https://dblp.org/rec/journals/pvldb/HilprechtSKMKB20) |
| Crossref | 0.267 | 1.000 | 2020 | match | [DeepDB](https://doi.org/10.14778/3384345.3384349) |
| DBLP | 1.000 | 1.000 | 2019 | n/a | [DeepDB: Learn from Data, not from Queries!](https://dblp.org/rec/journals/corr/abs-1909-00607) |
| arXiv title | 1.000 | 1.000 | 2019 | n/a | [DeepDB: Learn from Data, not from Queries!](http://arxiv.org/abs/1909.00607v1) |

### 48. REVIEW - wu2023factorjoin

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: FactorJoin: A New Cardinality Estimation Framework for Join Queries
- Supplied authors: Z. Wu, P. Negi, M. Alizadeh, T. Kraska, S. Madden
- Supplied year: 2023
- Supplied DOI: `10.1145/3588721`
- Supplied URL: https://doi.org/10.1145/3588721
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2023 | match | [FactorJoin: A New Cardinality Estimation Framework for Join Queries](https://doi.org/10.1145/3588721) |
| Crossref | 1.000 | 1.000 | 2023 | match | [FactorJoin: A New Cardinality Estimation Framework for Join Queries](https://doi.org/10.1145/3588721) |
| DBLP | 1.000 | 1.000 | 2023 | match | [FactorJoin: A New Cardinality Estimation Framework for Join Queries](https://dblp.org/rec/journals/pacmmod/WuNAKM23) |
| DBLP | 1.000 | 1.000 | 2022 | conflict | [FactorJoin: A New Cardinality Estimation Framework for Join Queries](https://dblp.org/rec/journals/corr/abs-2212-05526) |
| arXiv title | 1.000 | 1.000 | 2022 | n/a | [FactorJoin: A New Cardinality Estimation Framework for Join Queries](http://arxiv.org/abs/2212.05526v1) |

### 49. REVIEW - chronis2024cardbench

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: CardBench: A Benchmark for Learned Cardinality Estimation in Relational Databases
- Supplied authors: Y. Chronis, Y. Wang, Y. Gan, S. Abu-El-Haija, C. Lin, C. Binnig, F. Ozcan
- Supplied year: 2024
- Supplied arXiv: `2408.16170`
- Supplied URL: https://arxiv.org/abs/2408.16170
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| arXiv ID | 1.000 | 1.000 | 2024 | match | [CardBench: A Benchmark for Learned Cardinality Estimation in Relational Databases](http://arxiv.org/abs/2408.16170v1) |
| arXiv title | 1.000 | 1.000 | 2024 | match | [CardBench: A Benchmark for Learned Cardinality Estimation in Relational Databases](http://arxiv.org/abs/2408.16170v1) |
| DBLP | 1.000 | 1.000 | 2024 | n/a | [CardBench: A Benchmark for Learned Cardinality Estimation in Relational Databases](https://dblp.org/rec/journals/corr/abs-2408-16170) |
| URL metadata | 1.000 | 0.000 | 2024 | n/a | [CardBench: A Benchmark for Learned Cardinality Estimation in Relational Databases](https://arxiv.org/abs/2408.16170) |
| Crossref | 0.614 | 0.000 | 2013 | n/a | [Frame Time and Cardinality Indeterminacy in Temporal Relational Databases](https://doi.org/10.5220/0004422302690276) |

### 50. REVIEW - marcus2019neo

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Neo: A Learned Query Optimizer
- Supplied authors: R. Marcus, O. Papaemmanouil
- Supplied year: 2019
- Supplied DOI: `10.14778/3342263.3342644`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; DBLP: HTTPError: HTTP Error 503: Service Unavailable

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2019 | match | [Neo: a learned query optimizer](https://doi.org/10.14778/3342263.3342644) |
| Crossref | 0.188 | 1.000 | 2019 | match | [Neo](https://doi.org/10.14778/3342263.3342644) |
| arXiv title | 1.000 | 1.000 | 2019 | n/a | [Neo: A Learned Query Optimizer](http://arxiv.org/abs/1904.03711v1) |
| Crossref | 0.933 | 0.000 | 2022 | conflict | [DeepO: A Learned Query Optimizer](https://doi.org/10.1145/3514221.3520167) |
| Crossref | 0.720 | 0.000 | 2024 | conflict | [FOSS: A Self-Learned Doctor for Query Optimizer](https://doi.org/10.1109/icde60146.2024.00330) |

### 51. REVIEW - marcus2021bao

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Bao: Making Learned Query Optimization Practical
- Supplied authors: Ryan Marcus, Parimarjan Negi, Hongzi Mao, Nesime Tatbul, Mohammad Alizadeh, Tim Kraska
- Supplied year: 2021
- Supplied DOI: `10.1145/3448016.3452838`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2021 | match | [Bao: Making Learned Query Optimization Practical](https://doi.org/10.1145/3448016.3452838) |
| Crossref | 1.000 | 1.000 | 2021 | match | [Bao: Making Learned Query Optimization Practical](https://doi.org/10.1145/3448016.3452838) |
| DBLP | 1.000 | 1.000 | 2021 | match | [Bao: Making Learned Query Optimization Practical](https://dblp.org/rec/conf/sigmod/MarcusNMTAK21) |
| DBLP | 1.000 | 1.000 | 2022 | conflict | [Bao: Making Learned Query Optimization Practical](https://dblp.org/rec/journals/sigmod/MarcusNMTAK22) |
| Crossref | 0.956 | 0.000 | 2022 | conflict | [Making Learned Query Optimization Practical](https://doi.org/10.1145/3542700.3542702) |


### 53. REVIEW - justen2024polar

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance
- Supplied authors: David Justen, Daniel Ritter, Campbell Fraser, Andrew Lamb, Allison Lee, Thomas Bodner, Mhd Yamen Haddad, Steffen Zeuch, Volker Markl, Matthias Boehm
- Supplied year: 2024
- Supplied DOI: `10.14778/3648160.3648175`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2024 | match | [POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance](https://doi.org/10.14778/3648160.3648175) |
| Crossref | 1.000 | 1.000 | 2024 | match | [POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance](https://doi.org/10.14778/3648160.3648175) |
| DBLP | 1.000 | 1.000 | 2024 | match | [POLAR: Adaptive and Non-invasive Join Order Selection via Plans of Least Resistance](https://dblp.org/rec/journals/pvldb/JustenRFLTLBHZMB24) |
| Crossref | 0.391 | 0.000 | 2001 | conflict | [Least third-order cumulant method with adaptive regularization parameter selection for neural networks](https://doi.org/10.1016/s0004-3702(01)00061-3) |
| Crossref | 0.390 | 0.000 | 1989 | conflict | [Order Selection for Non-Stationary AR Models by Predictive Least-Squares](https://doi.org/10.23919/acc.1989.4790374) |

### 54. FAIL - tpcds

- Verdict: Unverifiable under fail-closed policy
- Supplied title: TPC Benchmark DS Standard Specification
- Supplied authors: Transaction Processing Performance Council
- Supplied year: 2024
- Supplied URL: https://www.tpc.org/tpcds/
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DataCite | 1.000 | 0.000 | 2015 | n/a | [TPC Benchmark DS Standard Specification](https://www.researchgate.net/doi/10.13140/RG.2.1.1039.8484) |
| Crossref | 0.411 | 0.000 | None | n/a | [Standard Specification for:Drawing Steel (DS), Sheet, Carbon, Cold-Rolled](https://doi.org/10.1520/a0620_a0620m-97) |
| Crossref | 0.388 | 0.000 | 2022 | n/a | [Beyond TPC-DS, a benchmark for Big Data OLAP systems (BDOLAP-Bench)](https://doi.org/10.1016/j.future.2022.02.015) |
| Crossref | 0.379 | 0.000 | None | n/a | [Standard Specification for:Drawing Steel (DS), Sheet and Strip, Carbon, Hot-Rolled](https://doi.org/10.1520/a0622_a0622m-97) |
| Crossref | 0.346 | 0.000 | 2019 | n/a | [Lessons Learned from the Industry’s First TPC Benchmark DS (TPC-DS)](https://doi.org/10.1007/978-3-030-11404-6_11) |

### 55. FAIL - tpch

- Verdict: Unverifiable under fail-closed policy
- Supplied title: TPC Benchmark H Standard Specification
- Supplied authors: Transaction Processing Performance Council
- Supplied year: 2024
- Supplied URL: https://www.tpc.org/tpch/
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DataCite | 1.000 | 0.000 | 2010 | n/a | [TPC Benchmark H Standard Specification](https://www.researchgate.net/doi/10.13140/RG.2.1.1883.9288) |
| Crossref | 0.516 | 0.000 | 2019 | n/a | [TPC Express Benchmark HS](https://doi.org/10.1007/978-3-319-77525-8_100340) |
| Crossref | 0.406 | 0.000 | 1992 | n/a | [TPC releases new benchmark](https://doi.org/10.1145/141858.141861) |
| URL metadata | 0.346 | 0.000 | 2024 | n/a | [TPC-H Homepage](https://www.tpc.org/tpch/) |
| Crossref | 0.333 | 0.000 | 2021 | n/a | [Identifying Standard Candles in Liquid Argon TPC at MeV Energies](https://doi.org/10.2172/1835867) |

### 56. REVIEW - oneil2009ssb

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: The Star Schema Benchmark and Augmented Fact Table Indexing
- Supplied authors: P. O'Neil, E. O'Neil, X. Chen, S. Revilak
- Supplied year: 2009
- Supplied DOI: `10.1007/978-3-642-10424-4_17`
- Supplied URL: https://www.cs.umb.edu/~poneil/StarSchemaB.PDF
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: DataCite: HTTPError: HTTP Error 404: Not Found; OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2009 | match | [The Star Schema Benchmark and Augmented Fact Table Indexing](https://doi.org/10.1007/978-3-642-10424-4_17) |
| Crossref | 1.000 | 1.000 | 2009 | match | [The Star Schema Benchmark and Augmented Fact Table Indexing](https://doi.org/10.1007/978-3-642-10424-4_17) |
| DBLP | 1.000 | 1.000 | 2009 | match | [The Star Schema Benchmark and Augmented Fact Table Indexing](https://dblp.org/rec/conf/tpctc/ONeilOCR09) |
| Crossref | 0.443 | 0.000 | None | conflict | [Avaliação do Star Schema Benchmark aplicado a bancos de dados NoSQL distribuídos e orientados a colunas](https://doi.org/10.11606/d.55.2016.tde-26102016-113544) |
| Crossref | 0.355 | 0.000 | 2003 | conflict | [Index structure for the fact table of a star-join schema and template query processing](https://doi.org/10.1145/973620.973646) |

### 57. REVIEW - erling2015ldbc

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: The LDBC Social Network Benchmark: Interactive Workload
- Supplied authors: Orri Erling, Alex Averbuch, Josep Larriba-Pey, Hassan Chafi, Andrey Gubichev, Arnau Prat, Minh-Duc Pham, Peter Boncz
- Supplied year: 2015
- Supplied DOI: `10.1145/2723372.2742786`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: DataCite: HTTPError: HTTP Error 404: Not Found; OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2015 | match | [The LDBC Social Network Benchmark: Interactive Workload](https://doi.org/10.1145/2723372.2742786) |
| DBLP | 1.000 | 0.875 | 2015 | match | [The LDBC Social Network Benchmark: Interactive Workload](https://dblp.org/rec/conf/sigmod/ErlingALCGPPB15) |
| Crossref | 0.734 | 1.000 | 2015 | match | [The LDBC Social Network Benchmark](https://doi.org/10.1145/2723372.2742786) |
| Crossref | 0.734 | 0.125 | 2022 | conflict | [The LDBC Social Network Benchmark](https://doi.org/10.14778/3574245.3574270) |
| Crossref | 0.692 | 0.375 | 2018 | conflict | [An early look at the LDBC social network benchmark's business intelligence workload](https://doi.org/10.1145/3210259.3210268) |

### 58. REVIEW - bitton1983wisconsin

- Verdict: Single-source strong match
- Supplied title: Benchmarking Database Systems: A Systematic Approach
- Supplied authors: D. Bitton, D. J. DeWitt, C. Turbyfill
- Supplied year: 1983
- Supplied URL: https://www.vldb.org/conf/1983/P008.PDF
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 1983 | n/a | [Benchmarking Database Systems A Systematic Approach](https://dblp.org/rec/conf/vldb/BittonDT83) |
| DBLP | 0.936 | 0.000 | 1999 | n/a | [Review - Benchmarking Database Systems A Systematic Approach](https://dblp.org/rec/journals/dr/Gray99) |
| Crossref | 0.582 | 0.000 | 2019 | n/a | [A platform for benchmarking Database Management Systems: CyDIW](https://doi.org/10.31274/cc-20240624-57) |
| Crossref | 0.444 | 0.000 | 2018 | n/a | [Benchmarking Mistakes](https://doi.org/10.1007/978-1-4842-4008-3_5) |
| Crossref | 0.388 | 0.000 | None | n/a | [Systematic Benchmarking of High-Throughput Subcellular Spatial Transcriptomics Platforms](https://doi.org/10.6019/s-biad1900) |

### 59. REVIEW - turbyfill1993as3ap

- Verdict: Single-source strong match
- Supplied title: AS3AP: An ANSI SQL Standard Scaleable and Portable Benchmark for Relational Database Systems
- Supplied authors: C. Turbyfill, C. Orji, D. Bitton
- Supplied year: 1993
- Supplied URL: https://www.odbms.org/2014/03/benchmark-handbook-1993/
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DBLP | 1.000 | 1.000 | 1993 | n/a | [AS3AP - An ANSI SQL Standard Scaleable and Portable Benchmark for Relational Database Systems](https://dblp.org/rec/books/mk/gray93/TurbyfillOB93) |
| DBLP | 1.000 | 1.000 | 1991 | n/a | [AS3AP: An ANSI SQL Standard Scaleable and Portable Benchmark for Relational Database Systems](https://dblp.org/rec/books/mk/gray91/TurbyfillOB91) |
| Crossref | 0.419 | 0.000 | 2005 | n/a | [Relational Database Systems and Oracle](https://doi.org/10.1007/978-1-4302-0000-0_1) |
| Crossref | 0.406 | 0.000 | 2019 | n/a | [SQL, An International Standard Database Language](https://doi.org/10.1007/978-1-4842-3841-7_1) |
| Crossref | 0.344 | 0.000 | 2016 | n/a | [Reusable Standard Database Components](https://doi.org/10.1007/978-1-4842-1973-7_12) |

### 60. REVIEW - deng2024lakebench

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: LakeBench: A Benchmark for Discovering Joinable and Unionable Tables in Data Lakes
- Supplied authors: Yuhao Deng, Chengliang Chai, Lei Cao, Qin Yuan, Siyuan Chen, Yanrui Yu, Zhaoze Sun, Junyi Wang, Jiajun Li, Ziqi Cao, Kaisen Jin, Chi Zhang, Yuqing Jiang, Yuanfang Zhang, Yuping Wang, Ye Yuan, Guoren Wang, Nan Tang
- Supplied year: 2024
- Supplied DOI: `10.14778/3659437.3659448`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: DataCite: HTTPError: HTTP Error 404: Not Found; OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2024 | match | [LakeBench: A Benchmark for Discovering Joinable and Unionable Tables in Data Lakes](https://doi.org/10.14778/3659437.3659448) |
| Crossref | 1.000 | 1.000 | 2024 | match | [LakeBench: A Benchmark for Discovering Joinable and Unionable Tables in Data Lakes](https://doi.org/10.14778/3659437.3659448) |
| DBLP | 1.000 | 1.000 | 2024 | match | [LakeBench: A Benchmark for Discovering Joinable and Unionable Tables in Data Lakes](https://dblp.org/rec/journals/pvldb/DengCCYCYSWLCJZJZWYWT24) |
| Crossref | 0.494 | 0.000 | 2023 | conflict | [NumJoin: Discovering Numeric Joinable Tables with Semantically Related Columns](https://doi.org/10.1145/3583780.3614750) |
| Crossref | 0.379 | 0.077 | 2023 | conflict | [High-efficient Joinable Tables Discovery in Data Lakes: A Grey Relational Model-based Approach](https://doi.org/10.1109/cbd63341.2023.00047) |

### 61. REVIEW - clickbench

- Verdict: Single-source strong match
- Supplied title: ClickBench: A Benchmark for Analytical DBMS
- Supplied authors: ClickHouse Inc.
- Supplied year: 2024
- Supplied URL: https://benchmark.clickhouse.com/
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 1.000 | 0.000 | 2024 | n/a | [ClickBench — a Benchmark For Analytical DBMS](https://benchmark.clickhouse.com/) |
| Crossref | 0.562 | 0.000 | 2022 | n/a | [DBMS-Benchmarker: Benchmark and Evaluate DBMS in
Python](https://doi.org/10.21105/joss.04628) |
| Crossref | 0.483 | 0.000 | 2009 | n/a | [A Trust-Based Benchmark for DBMS Configurations](https://doi.org/10.1109/prdc.2009.31) |
| Crossref | 0.375 | 0.000 | 1996 | n/a | [Documentation of analytical values in food DBMS/ Computer demonstration](https://doi.org/10.1016/0308-8146(96)89043-1) |
| Crossref | 0.283 | 0.000 | 2009 | n/a | [On Analytical Performance Measurement of Concurrency Control Protocols in DBMS](https://doi.org/10.7763/ijcee.2009.v1.43) |

### 62. REVIEW - carey1995garlic

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: Towards Heterogeneous Multimedia Information Systems: The Garlic Approach
- Supplied authors: Michael J. Carey, Laura M. Haas, Peter M. Schwarz, Manish Arya, William F. Cody, Ronald Fagin, Myron Flickner, Allen W. Luniewski, Wayne Niblack, Dragutin Petkovic, John Thomas, John H. Williams, Edward L. Wimmers
- Supplied year: 1995
- Supplied DOI: `10.1109/ride.1995.378736`
- Supplied URL: https://research.ibm.com/publications/towards-heterogeneous-multimedia-information-systems-the-garlic-approach
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | None | match | [Towards heterogeneous multimedia information systems: the Garlic approach](https://doi.org/10.1109/ride.1995.378736) |
| Crossref | 1.000 | 1.000 | None | match | [Towards heterogeneous multimedia information systems: the Garlic approach](https://doi.org/10.1109/ride.1995.378736) |
| DBLP | 1.000 | 1.000 | 1995 | match | [Towards Heterogeneous Multimedia Information Systems: The Garlic Approach](https://dblp.org/rec/conf/ride/CareyHSACFFLNPTWW95) |
| Crossref | 0.607 | 0.000 | 1997 | conflict | [Towards a model for multimedia geographical information systems](https://doi.org/10.1201/9781482272956-15) |
| Crossref | 0.466 | 0.000 | 2005 | conflict | [Towards a theory of multimedia metacomputing](https://doi.org/10.1016/j.is.2004.06.001) |

### 63. REVIEW - stonebraker2015bigdawg

- Verdict: Passed available evidence, but source/API failures remain
- Supplied title: The BigDAWG Polystore System
- Supplied authors: Jennie Duggan, Aaron J. Elmore, Michael Stonebraker, Magda Balazinska, Bill Howe, Jeremy Kepner, Sam Madden, David Maier, Tim Mattson, Stan Zdonik
- Supplied year: 2015
- Supplied DOI: `10.1145/2814710.2814713`
- Issues: Strict final gate requires rerunning or manually documenting failed sources.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref DOI | 1.000 | 1.000 | 2015 | match | [The BigDAWG Polystore System](https://doi.org/10.1145/2814710.2814713) |
| Crossref | 1.000 | 1.000 | 2015 | match | [The BigDAWG Polystore System](https://doi.org/10.1145/2814710.2814713) |
| Crossref | 1.000 | 0.200 | 2018 | conflict | [The BigDAWG polystore system](https://doi.org/10.1145/3226595.3226620) |
| DBLP | 1.000 | 0.200 | 2019 | conflict | [The BigDAWG polystore system](https://dblp.org/rec/books/mc/19/MattsonRE14) |
| Crossref | 0.738 | 0.600 | 2016 | conflict | [The BigDAWG polystore system and architecture](https://doi.org/10.1109/hpec.2016.7761636) |

### 64. FAIL - postgresql_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: PostgreSQL Documentation: 18: 14.1. Using EXPLAIN
- Supplied authors: PostgreSQL Global Development Group
- Supplied year: 2026
- Supplied URL: https://www.postgresql.org/docs/18/using-explain.html
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: DataCite: HTTPError: HTTP Error 400: Bad Request; OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 0.562 | 0.000 | 2026 | n/a | [14.1. Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) |
| Crossref | 0.494 | 0.000 | None | n/a | [Accessing PostgreSQL from C Using libpq](https://doi.org/10.1007/978-1-4302-0018-5_13) |
| Crossref | 0.478 | 0.000 | None | n/a | [Accessing PostgreSQL from C Using Embedded SQL](https://doi.org/10.1007/978-1-4302-0018-5_14) |
| Crossref | 0.441 | 0.000 | 1972 | n/a | [Documentation](https://doi.org/10.7551/mitpress/1343.003.0008) |
| Crossref | 0.368 | 0.000 | 2025 | n/a | [PostgreSQL System Architecture](https://doi.org/10.1007/979-8-8688-1507-2_1) |

### 65. REVIEW - trino_docs

- Verdict: Single-source strong match
- Supplied title: Cost-Based Optimizations: Trino 482 Documentation
- Supplied authors: Trino Software Foundation
- Supplied year: 2026
- Supplied URL: https://trino.io/docs/482/optimizer/cost-based-optimizations.html
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 1.000 | 0.000 | 2026 | n/a | [Cost-based optimizations — Trino 482 Documentation](https://trino.io/docs/482/optimizer/cost-based-optimizations.html) |
| Crossref | 0.472 | 0.000 | 1962 | n/a | [DOKUMENTATION / DOCUMENTATION / DOCUMENTATION](https://doi.org/10.1515/mt-1962-041208) |
| Crossref | 0.432 | 0.000 | None | n/a | [Performance and monetary cost optimizations for HPC applications in the cloud](https://doi.org/10.32657/10356/69201) |
| Crossref | 0.273 | 0.000 | 2011 | n/a | [Trino, Francesco da](https://doi.org/10.1093/benz/9780199773787.article.b00185309) |
| Crossref | 0.230 | 0.000 | 2011 | n/a | [Trino, Gaspare](https://doi.org/10.1093/benz/9780199773787.article.b00185310) |

### 66. REVIEW - bigquery_docs

- Verdict: Single-source strong match
- Supplied title: Query Plan and Timeline
- Supplied authors: Google Cloud
- Supplied year: 2026
- Supplied URL: https://cloud.google.com/bigquery/docs/query-plan-explanation
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 1.000 | 0.000 | 2026 | n/a | [Query plan and timeline](https://cloud.google.com/bigquery/docs/query-plan-explanation) |
| Crossref | 0.606 | 0.000 | None | n/a | [Query Plan](https://doi.org/10.1007/springerreference_63890) |
| Crossref | 0.516 | 0.000 | 2014 | n/a | [Timeline](https://doi.org/10.1515/9781438453002-001) |
| Crossref | 0.465 | 0.000 | None | n/a | [Query Execution Plan](https://doi.org/10.1007/springerreference_65581) |
| Crossref | 0.464 | 0.000 | 2004 | n/a | [Yucca Mountain Disposal Decision Plan Timeline](https://doi.org/10.2172/837487) |

### 67. FAIL - spark_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: Performance Tuning: Spark 4.1.2 Documentation
- Supplied authors: Apache Software Foundation
- Supplied year: 2026
- Supplied URL: https://spark.apache.org/docs/4.1.2/sql-performance-tuning.html
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 0.581 | 0.000 | 2026 | n/a | [Performance Tuning](https://spark.apache.org/docs/4.1.2/sql-performance-tuning.html) |
| Crossref | 0.581 | 0.000 | 2016 | n/a | [Performance Tuning](https://doi.org/10.1002/9781119254805.ch3) |
| Crossref | 0.525 | 0.000 | 2018 | n/a | [Tuning Performance of Spark Programs](https://doi.org/10.1109/ic2e.2018.00057) |
| Crossref | 0.484 | 0.000 | 2023 | n/a | [Apache Spark Big data Analysis, Performance Tuning, and Spark Application Optimization](https://doi.org/10.1109/easct59475.2023.10393086) |
| Crossref | 0.241 | 0.000 | None | n/a | [Improving Automatic Tuning of Hadoop and Spark by Analysing Container Performance Metrics](https://doi.org/10.22215/etd/2019-13908) |

### 68. FAIL - snowflake_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: EXPLAIN: Snowflake Documentation
- Supplied authors: Snowflake Inc.
- Supplied year: 2026
- Supplied URL: https://docs.snowflake.com/en/sql-reference/sql/explain
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: ; DBLP: HTTPError: HTTP Error 503: Service Unavailable

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref | 0.540 | 0.000 | 2021 | n/a | [Snowflake Organization Structure](https://doi.org/10.1007/978-1-4842-7389-0_1) |
| Crossref | 0.531 | 0.000 | 2022 | n/a | [Snowflake Security](https://doi.org/10.1007/978-1-4842-7389-0) |
| Crossref | 0.528 | 0.000 | 2021 | n/a | [Snowflake for Security](https://doi.org/10.1007/978-1-4842-7389-0_9) |
| Crossref | 0.450 | 0.000 | 2019 | n/a | [Snowflake](https://doi.org/10.5040/9781784606183.00000002) |
| Crossref | 0.431 | 0.000 | 2021 | n/a | [Secure Data Sharing with Snowflake](https://doi.org/10.1007/978-1-4842-7389-0_8) |

### 69. FAIL - duckdb_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: DuckDB Documentation: WITH Clause and CTE Materialization
- Supplied authors: DuckDB Foundation
- Supplied year: 2026
- Supplied URL: https://duckdb.org/docs/stable/sql/query_syntax/with.html
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref | 0.475 | 0.000 | 2019 | n/a | [DOCUMENTATION AND DOCUMENT CONTROL (CLAUSE 7.5)](https://doi.org/10.2307/j.ctvb4bsqs.12) |
| Crossref | 0.473 | 0.000 | 2011 | n/a | [Sovereign Debt Documentation and the Pari Passu Clause](https://doi.org/10.1002/9781118267073.ch24) |
| Crossref | 0.328 | 0.000 | 2020 | n/a | [duckdb: DBI Package for the DuckDB Database Management System](https://doi.org/10.32614/cran.package.duckdb) |
| Crossref | 0.321 | 0.000 | 2024 | n/a | [DuckDB vs dplyr vs base R](https://doi.org/10.59350/q6650-vdq47) |
| Crossref | 0.321 | 0.000 | 2024 | n/a | [DuckDB vs dplyr vs base R](https://doi.org/10.59350/xsdnt-jdm19) |

### 70. REVIEW - clickhouse_docs

- Verdict: Single-source strong match
- Supplied title: Using JOINs in ClickHouse
- Supplied authors: ClickHouse Inc.
- Supplied year: 2026
- Supplied URL: https://clickhouse.com/docs/guides/joining-tables
- Issues: Only one source produced a strict match; EMNLP-style audit should manually verify this item.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 1.000 | 0.000 | 2026 | n/a | [Using JOINs in ClickHouse](https://clickhouse.com/docs/guides/joining-tables) |
| Crossref | 0.524 | 0.000 | 2019 | n/a | [Using Inner Joins](https://doi.org/10.1007/978-1-4842-4905-5_4) |
| Crossref | 0.524 | 0.000 | 2019 | n/a | [Using Cross Joins](https://doi.org/10.1007/978-1-4842-4905-5_9) |
| Crossref | 0.468 | 0.000 | 2019 | n/a | [Using Left Outer Joins](https://doi.org/10.1007/978-1-4842-4905-5_5) |
| Crossref | 0.468 | 0.000 | 2019 | n/a | [Using Full Outer Joins](https://doi.org/10.1007/978-1-4842-4905-5_7) |

### 71. FAIL - calcite_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: Apache Calcite Documentation
- Supplied authors: Apache Software Foundation
- Supplied year: 2026
- Supplied URL: https://calcite.apache.org/docs/
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| DataCite | 0.361 | 0.000 | 2026 | n/a | [Locating Faults not Mentioned in Bug Reports](https://zenodo.org/doi/10.5281/zenodo.19344932) |
| Crossref | 0.290 | 0.000 | 2024 | n/a | [Stories in the Moment of Encounter:](https://doi.org/10.2307/jj.10286089.9) |
| Crossref | 0.286 | 0.000 | 2001 | n/a | [Transforming documentation from the XML doctypes used for the apache website to DITA](https://doi.org/10.1145/501546.501548) |
| Crossref | 0.286 | 0.000 | 2001 | n/a | [Transforming documentation from the XML doctypes used for the apache website to DITA](https://doi.org/10.1145/501516.501548) |
| Crossref | 0.238 | 0.000 | 2024 | n/a | [Sustainability:](https://doi.org/10.2307/jj.10286089.12) |

### 72. FAIL - datafusion_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: Reading Explain Plans
- Supplied authors: Apache Software Foundation
- Supplied year: 2026
- Supplied URL: https://datafusion.apache.org/user-guide/explain-usage.html
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| Crossref | 0.765 | 0.000 | 2019 | n/a | [Reading plans](https://doi.org/10.1201/9780429264054-2) |
| URL metadata | 0.568 | 0.000 | 2026 | n/a | [Reading Explain Plans — Apache DataFusion documentation](https://datafusion.apache.org/user-guide/explain-usage.html) |
| Crossref | 0.455 | 0.000 | 2026 | n/a | [Start Reading Change of Plans by Sarah Dessen](https://doi.org/10.55277/researchhub.bze6rwvo.1) |
| Crossref | 0.400 | 0.000 | 2008 | n/a | [Can Prospect Theory Explain the Popularity of Savings Plans?](https://doi.org/10.2139/ssrn.1681343) |
| Crossref | 0.389 | 0.000 | 2024 | n/a | [Further Reading](https://doi.org/10.12987/9780300277616-016) |

### 73. FAIL - presto_docs

- Verdict: Unverifiable under fail-closed policy
- Supplied title: Cost Based Optimizations: Presto 0.298.1 Documentation
- Supplied authors: Presto Foundation
- Supplied year: 2026
- Supplied URL: https://prestodb.github.io/docs/current/optimizer/cost-based-optimizations.html
- Issues: Candidates exist but none match the supplied title/authors/year closely enough.
- Source errors: OpenAlex: HTTPError: HTTP Error 429: Too Many Requests; Semantic Scholar: HTTPError: HTTP Error 429: 

| Source | Title similarity | Author overlap | Year | Identifier | Candidate |
| --- | ---: | ---: | --- | --- | --- |
| URL metadata | 0.623 | 0.000 | 2026 | n/a | [Cost based optimizations](https://prestodb.github.io/docs/current/optimizer/cost-based-optimizations.html) |
| Crossref | 0.452 | 0.000 | 2003 | n/a | [Presto Theory Documentation: Rigid Bodies](https://doi.org/10.2172/809988) |
| Crossref | 0.447 | 0.000 | 1964 | n/a | [DOKUMENTATION / DOCUMENTATION / DOCUMENTATION](https://doi.org/10.1515/mt-1964-060813) |
| Crossref | 0.415 | 0.000 | None | n/a | [Performance and monetary cost optimizations for HPC applications in the cloud](https://doi.org/10.32657/10356/69201) |
| Crossref | 0.291 | 0.000 | 2015 | n/a | [Cost Effective Implementation of Fixed Point Adders for LUT based FPGAs using Technology Dependent Optimizations](https://doi.org/10.7251/els1519014k) |

### PASS - trino_pushdown_docs

- Title: Pushdown: Trino 482 Documentation
- Source: Official URL
- Identifier: https://trino.io/docs/current/optimizer/pushdown.html
- Note: http=200; official page; final=https://trino.io/docs/current/optimizer/pushdown.html

### PASS - trino_dynamic_filtering_docs

- Title: Dynamic Filtering: Trino 482 Documentation
- Source: Official URL
- Identifier: https://trino.io/docs/current/admin/dynamic-filtering.html
- Note: http=200; official page; final=https://trino.io/docs/current/admin/dynamic-filtering.html

### PASS - bigquery_federated_docs

- Title: Introduction to Federated Queries
- Source: Official URL
- Identifier: https://docs.cloud.google.com/bigquery/docs/federated-queries-intro
- Note: http=200; official page; final=https://docs.cloud.google.com/bigquery/docs/federated-queries-intro
