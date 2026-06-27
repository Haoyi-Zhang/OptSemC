-- OptSemBench-C probe P3797
-- features: adaptivity_trigger=runtime_stats, aggregation=none, connector_capability=not_applicable, control_surface=none_control, distribution_trigger=broadcast_candidate, join_shape=chain, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT a.k, COUNT(*)
FROM a a JOIN b b ON a.k=b.k JOIN c c ON b.k=c.k JOIN d d ON c.k=d.k;
