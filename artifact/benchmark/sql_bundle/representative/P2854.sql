-- OptSemBench-C probe P2854
-- features: adaptivity_trigger=none, aggregation=none, connector_capability=not_applicable, control_surface=pg_enable_indexonlyscan_off, distribution_trigger=none, join_shape=clique, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT a.k
FROM a a JOIN b b ON a.k=b.k JOIN c c ON a.k=c.k JOIN d d ON b.k=d.k;
