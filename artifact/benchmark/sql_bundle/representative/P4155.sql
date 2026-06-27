-- OptSemBench-C probe P4155
-- features: adaptivity_trigger=stage_boundary, aggregation=none, connector_capability=not_applicable, control_surface=none_control, distribution_trigger=shuffle, join_shape=star, join_type=inner, order_limit=none, predicate_class=none, reuse_structure=none, source_boundary=local, statistics_need=low
SELECT f.key, d1.attr, d2.attr
FROM fact f JOIN dim1 d1 ON f.k1=d1.k JOIN dim2 d2 ON f.k2=d2.k;
