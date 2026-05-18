# TODO: Advanced Visualization Roadmap

This list captures the remaining visualization recommendations that have not
already been implemented in the `advanced-visual-grammar` branch and excludes
existing `geom_edgebundle` support.

Each item is written so a future coding agent can pick it up independently.
Keep ggplot2/R-compatible public argument names where applicable, add focused
pytest coverage, add or extend a notebook example, render impacted notebooks,
capture PNGs with Node/NPM Playwright, and inspect images for semantic
correctness.

See `GGPLOT2_GAP_ANALYSIS.md` for the full ggplot2 parity audit against the
official ggplot2 4.0.3 reference index.

## Working Contract For Each Item

- Preserve ggplot2-style names: prefer `na_rm`, `show_legend`, `binwidth`,
  `breaks`, `labels`, `limits`, `position`, `stat`, `geom`, etc. when they map
  to R concepts. Keep existing aliases such as `colour` where relevant.
- Keep stat transforms pure: dataframe in, dataframe plus mapping updates out.
- Keep Plotly mutation inside geom draw methods or scale apply methods.
- Add exports in `ggplotly/geoms/__init__.py`, `ggplotly/stats/__init__.py`,
  `ggplotly/scales/__init__.py`, and top-level `ggplotly/__init__.py` when the
  feature is public.
- Add focused tests under `pytest/`. Tests should assert trace type, key
  coordinates, scale/legend behavior, empty-data behavior, and mapping updates,
  not only that drawing succeeds.
- Add visual examples to a docs/gallery notebook or a new notebook if the topic
  deserves one.
- Verification for visual work:
  - Run targeted pytest.
  - Run full pytest when the change touches shared draw/stat/scale behavior.
  - Execute impacted notebooks.
  - Render HTML.
  - Capture chart PNGs with Node Playwright, not desktop Chrome/Kaleido.
  - Review each PNG against chart intent.

## ggplot2 Parity Backlog

- [ ] Add an API parity harness for ggplot2 function names and aliases.
  - Source of truth: create a grouped expected API list from the official
    ggplot2 reference index and compare it to `ggplotly.__all__`.
  - Include `color`/`colour` aliases, underscore/compact aliases such as
    `geom_bin_2d()` vs `geom_bin2d()` where ggplot2 supports them, and all
    public constructors added by parity work.
  - Add tests that import every expected public name and assert aliases point to
    compatible implementations.

- [ ] Audit public argument names for ggplot2 compatibility.
  - Preserve ggplot2-style names such as `na_rm`, `show_legend`, `binwidth`,
    `bins`, `breaks`, `labels`, `limits`, `position`, `stat`, `geom`,
    `linewidth`, `lineend`, `linejoin`, `orientation`, and `inherit_aes`.
  - Keep any existing Pythonic aliases only as backward-compatible aliases.
  - For R names containing dots, consider support through `**params` for
    generated/transpiled code while keeping normal Python identifiers valid.

- [ ] Add missing core ggplot2 geoms.
  - Implement or alias: `geom_blank()`, `geom_curve()`, `geom_spoke()`,
    `geom_polygon()`, `geom_quantile()`, `geom_function()`,
    `geom_density_2d()`, `geom_density2d()`,
    `geom_density_2d_filled()`, `geom_density2d_filled()`,
    `geom_bin_2d()`, `geom_sf_text()`, and `geom_sf_label()`.
  - Tests should cover trace shape, scale training, grouping, mapped
    aesthetics, empty data, and alias imports.
  - Add a parity gallery notebook with examples for blank scale training,
    curved annotations, vector spokes, polygons, quantile lines, function
    overlays, 2D density contours, and sf labels.

- [ ] Add missing core ggplot2 stats.
  - Implement or alias: `stat_align()`, `stat_unique()`,
    `stat_summary_hex()`, `stat_contour_filled()`, `stat_bin_2d()`,
    `stat_density2d()`, `stat_ydensity()`, and `stat_sf()`.
  - Keep stat transforms pure: dataframe in, dataframe plus mapping updates
    out.
  - Tests should assert computed columns, grouping, NA behavior, empty input,
    and compatibility with the expected paired geoms.

- [ ] Complete ggplot2 color/fill scale families.
  - Add continuous, gradient2, gradientn, steps, steps2, stepsn, distiller,
    fermenter, viridis continuous/binned, hue, grey, discrete, identity, manual,
    brewer, and binned variants for both `color` and `colour` spellings plus
    `fill`.
  - Use shared implementation where possible; wrappers should only bind
    aesthetic and spelling.
  - Tests should cover limits, breaks, labels, palettes, direction, midpoint,
    binned boundaries, NA colors, colorbar/legend output, and alias imports.

- [ ] Complete size, linewidth, shape, linetype, and alpha scale families.
  - Add `scale_linewidth*()` variants, missing `scale_size*()` variants
    including area/binned-area/radius, missing `scale_shape*()` variants,
    `scale_linetype()`/`scale_linetype_binned()`, and
    `scale_alpha_binned()`.
  - Tests should verify Plotly marker sizes, line widths, marker symbols, dash
    styles, alpha values, guide labels, and that point size and line width do
    not conflict.

- [ ] Complete x/y positional and date/time scale symmetry.
  - Add `scale_x_binned()`, `scale_y_binned()`, `scale_x_log2()`,
    `scale_y_log2()`, `scale_y_date()`, `scale_y_datetime()`,
    `scale_x_time()`, and `scale_y_time()`.
  - Tests should cover trace values, tick labels, limits, reverse transforms,
    date/datetime preservation, and interactions with stats.

- [ ] Add missing coordinates and audit coordinate behavior.
  - Implement `coord_trans()` and `coord_radial()`.
  - Decide whether `coord_map()` and `coord_quickmap()` should be aliases,
    documented non-goals, or implemented for legacy compatibility.
  - Add notebook examples for scale transform vs coord transform differences,
    radial plots, polar bars, and map aspect behavior.

- [ ] Expand facets and labellers to ggplot2 parity.
  - Add `facet_null()`, `vars()`, `labeller()`, `as_labeller()`,
    `label_context()`, `label_parsed()`, `label_bquote()`, and
    `label_wrap_gen()`.
  - Audit `facet_wrap()` and `facet_grid()` arguments including `scales`,
    `space`, `margins`, `switch`, `drop`, `strip.position`, `axes`, and
    `axis.labels`.
  - Visual review must inspect free scales, long strip labels, wrapped labels,
    multi-row/column facets, and margin panels.

- [ ] Complete themes and theme element helpers.
  - Add `theme_gray()`, `theme_grey()`, `theme_bw()`, `theme_light()`,
    `theme_linedraw()`, `theme_void()`, `theme_test()`, `theme_get()`,
    `theme_set()`, `theme_update()`, `theme_replace()`, `element_blank()`,
    `element_geom()`, `element_point()`, `element_polygon()`, `margin()`,
    `margin_part()`, and `rel()`.
  - If theme state is introduced, tests must isolate and reset global state.
  - Add a theme comparison notebook and inspect backgrounds, grids, axes,
    legend boxes, text, margins, and blanked elements.

- [ ] Complete guide and annotation helpers.
  - Add `guide_axis()`, `guide_axis_logticks()`, `guide_axis_stack()`,
    `guide_bins()`, `guide_colorsteps()`, `guide_colourbar()`,
    `guide_coloursteps()`, `guide_none()`, `guide_custom()`,
    `annotation_custom()`, `annotation_logticks()`, `annotation_map()`,
    `annotation_raster()`, `annotation_borders()`, and `borders()`.
  - Tests should cover guide suppression, colorbar vs legend behavior, binned
    labels, axis label angle/dodging, log tick placement, raster extents, map
    annotation geo context, and spelling aliases.

- [ ] Add lower-priority ggplot2 utility parity.
  - Only implement helpers where behavior maps cleanly to Python/Plotly.
  - Consider `ggplot_build()`, `layer_data()`, `get_layer_data()`,
    `ggplot_gtable()`, `ggplotGrob()`, `last_plot()`, `is_ggplot()`,
    `update_geom_defaults()`, `update_stat_defaults()`, `qplot()`,
    `quickplot()`, `autoplot()`, and `fortify()`.
  - Treat grid/gtable/S3-style APIs as compatibility shims unless there is a
    clear Plotly-native equivalent.

- [ ] Add ggplot2 dataset parity checks.
  - Verify local availability, columns, and dtypes for ggplot2 datasets:
    `diamonds`, `economics`, `economics_long`, `faithfuld`, `luv_colours`,
    `midwest`, `mpg`, `msleep`, `presidential`, `seals`, and `txhousing`.
  - Add tests that translated ggplot2 examples can load these datasets with
    expected column names and basic dtype behavior.

## Geospatial And Movement Analytics

- [ ] `stat_h3bin()`
  - Goal: Aggregate lat/lon points into hierarchical H3 cells for scalable
    spatial summaries.
  - Public API: `stat_h3bin(mapping=None, data=None, resolution=7,
    fun="count", value=None, na_rm=False, keep_geometry=True, **params)`.
  - Inputs: `aes(x='lon', y='lat')` or explicit `aes(lon='lon', lat='lat')`;
    optional `weight` or `fill`/`z` value column for summaries.
  - Output columns: `h3`, `count`, `value`, `lon`, `lat`, optionally polygon
    boundary coordinates or GeoJSON-ready geometry. Mapping update should set
    `fill` to `count` or summarized `value`.
  - Implementation notes: Use optional `h3` dependency if installed. If absent,
    raise a clear ImportError only when the stat is used. Do not make this a
    hard dependency unless explicitly decided. Keep the pure aggregation logic
    in `ggplotly/stats/`.
  - Tests: aggregation count totals equal input rows; weighted summaries match
    pandas groupby; empty input returns stable columns; missing optional
    dependency error is clear.
  - Notebook example: dense point map aggregated by H3 resolution with at least
    two resolutions to show hierarchy.

- [ ] `geom_h3()`
  - Goal: Draw H3 cell polygons or centroids from `stat_h3bin()` output.
  - Public API: `geom_h3(mapping=None, data=None, stat="h3bin",
    resolution=7, color=None, fill=None, alpha=1, linewidth=0,
    show_legend=True, **params)`.
  - Expected behavior: Use `go.Choropleth` with GeoJSON polygons for map cells
    when boundaries are available. Fall back to `Scattergeo` centroids if only
    centroids are present.
  - Implementation notes: Reuse existing `geom_tile`/`geom_map` geo-context
    patterns. Respect facet geo domains and global color limits.
  - Tests: creates choropleth trace with one location per H3 cell; colorbar
    title follows `fill`; faceting preserves map layout.
  - Notebook example: spatial density of simulated events.

- [ ] `geom_h3_choropleth()`
  - Goal: Draw precomputed H3-indexed values without recomputing bins.
  - Public API: `geom_h3_choropleth(mapping=None, data=None, h3='h3',
    fill=None, resolution=None, color=None, alpha=1, **params)`.
  - Inputs: dataframe with H3 index column and value column.
  - Implementation notes: Convert H3 indices to polygon boundaries, build
    GeoJSON, use `go.Choropleth`.
  - Tests: accepts precomputed H3 indices; missing `h3` column raises helpful
    `ColumnNotFoundError`; categorical and continuous fill both render.
  - Notebook example: regional risk score choropleth by hex cell.

- [ ] `geom_flowmap()`
  - Goal: Draw origin-destination flows on maps with direction, width, color,
    and optional curvature.
  - Public API: `geom_flowmap(mapping=None, data=None, curvature=0.25,
    arrow=False, arrow_size=12, great_circle=True, lineend="round",
    na_rm=False, **params)`.
  - Required aesthetics: `x`, `y`, `xend`, `yend`; optional `weight`, `color`,
    `alpha`, `tooltip`, `data_id`.
  - Implementation notes: Use `Scattergeo` line traces. For great-circle arcs,
    interpolate spherical points. Width should map from `weight` with a
    configurable range. Handle antimeridian paths defensively.
  - Tests: one trace or trace group per flow; lon/lat endpoints preserved;
    weight maps to line width; optional arrows do not break non-geo plots.
  - Notebook example: freight lanes between cities.

- [ ] `geom_od_arc()`
  - Goal: Draw curved origin-destination arcs in Cartesian coordinates for
    non-map flow diagrams.
  - Public API: `geom_od_arc(mapping=None, data=None, curvature=0.35,
    n=50, arrow=False, **params)`.
  - Required aesthetics: `x`, `y`, `xend`, `yend`; optional `weight`, `color`,
    `group`.
  - Implementation notes: Build quadratic Bezier paths. This should be a
    Cartesian sibling of `geom_flowmap`, not a map-only geom.
  - Tests: generated paths start/end at mapped endpoints; `n` controls point
    count; grouped arcs create distinct legend entries.
  - Notebook example: network flows between ordered facilities.

- [ ] `geom_tripline()`
  - Goal: Draw timestamped movement trajectories from ordered points.
  - Public API: `geom_tripline(mapping=None, data=None, group=None,
    time=None, color=None, size=1, alpha=0.8, **params)`.
  - Required aesthetics: `x`, `y`; optional `time`, `group`, `color`.
  - Implementation notes: Sort within each group by `time`, draw lines and
    optionally add animation frames when combined with `transition_time`.
  - Tests: group ordering by time is stable; missing time preserves input
    order; map context uses `Scattergeo`.
  - Notebook example: delivery vehicle GPS paths with color by trip type.

- [ ] `stat_od_matrix()`
  - Goal: Aggregate event-level trips into origin-destination counts or
    weighted flows.
  - Public API: `stat_od_matrix(mapping=None, data=None, origin=None,
    destination=None, weight=None, fun="sum", drop=True, **params)`.
  - Output columns: `origin`, `destination`, `count`, `weight`, optional
    origin/destination coordinates when available.
  - Implementation notes: Pure groupby transform. Should feed `geom_flowmap`,
    `geom_chord`, and `geom_arc_diagram`.
  - Tests: counts equal input trips; weighted sums match expected values;
    missing coordinate joins fail clearly.
  - Notebook example: OD matrix to flow map and chord diagram.

- [ ] `geom_cartogram()`
  - Goal: Value-distorted map where geography size reflects a metric.
  - Public API: `geom_cartogram(mapping=None, data=None, map=None,
    map_id=None, fill=None, value=None, method="dorling", **params)`.
  - Implementation notes: Start with Dorling cartogram circles because true
    polygon cartograms are harder and need extra dependencies. Compute circle
    positions from centroids, radius from `value`, and draw `Scattergeo`.
  - Tests: radius scale tracks value; labels/hover preserve map ids; no value
    falls back to equal circles.
  - Notebook example: population-adjusted US state comparison.

## Large Data, Progressive Rendering, And Approximation

- [ ] `geom_datashade()`
  - Goal: Render very large scatter/line datasets as image rasters instead of
    Plotly vector traces.
  - Public API: `geom_datashade(mapping=None, data=None, width=800,
    height=500, aggregator="count", cmap="viridis", dynamic=False,
    **params)`.
  - Required aesthetics: `x`, `y`; optional `color`, `weight`.
  - Implementation notes: Prefer optional `datashader` if installed. If absent,
    implement a numpy histogram2d fallback for count aggregation. Output should
    be a Plotly `go.Image` or `go.Heatmap` with proper axis extents.
  - Tests: large input produces one raster trace; extent matches data bounds;
    fallback path works without datashader; empty input is no-op.
  - Notebook example: million-point cloud or dense line simulation.

- [ ] `stat_rasterize()`
  - Goal: Convert point/line layers into fixed-resolution aggregate rasters.
  - Public API: `stat_rasterize(mapping=None, data=None, width=512,
    height=512, aggregator="count", limits=None, **params)`.
  - Output columns: `x`, `y`, `z`, `count` or `value`, ready for `geom_raster`
    or `geom_tile`.
  - Implementation notes: Pure numpy/pandas transform. Keep coordinate extent
    metadata available through attrs or params if needed by geom.
  - Tests: bin totals equal input count; limits clip or keep values according
    to documented behavior; numeric precision is stable.
  - Notebook example: dense scatter rendered as raster heatmap.

- [ ] `stat_density_canvas()`
  - Goal: Estimate density directly on a canvas grid for large point clouds.
  - Public API: `stat_density_canvas(mapping=None, data=None, width=512,
    height=512, bandwidth=None, method="kde", **params)`.
  - Implementation notes: Use scipy KDE for moderate data; for larger data,
    use histogram smoothing. Avoid quadratic memory behavior.
  - Tests: returns grid with expected dimensions; density is nonnegative;
    constant input does not crash.
  - Notebook example: density field behind sampled points.

- [ ] `stat_sketch()`
  - Goal: Approximate large datasets with mergeable sketches for fast visual
    summaries.
  - Public API: `stat_sketch(mapping=None, data=None, method="tdigest",
    bins=100, by=None, **params)`.
  - Implementation notes: Start with quantile sketches for distributions and
    histograms. Keep optional dependencies optional; provide a pandas fallback.
  - Tests: approximate quantiles are within tolerance; grouping works;
    deterministic seed where sampling is used.
  - Notebook example: approximate distribution over millions of simulated rows.

- [ ] `stat_reservoir_sample()`
  - Goal: Sample bounded rows from streaming/large datasets for plotting while
    preserving unbiased inclusion.
  - Public API: `stat_reservoir_sample(mapping=None, data=None, n=10000,
    seed=None, by=None, **params)`.
  - Implementation notes: Pure stat. For grouped sampling, maintain a reservoir
    per group. Should work with dataframe inputs and iterables only if the repo
    already supports iterable stats.
  - Tests: output row count cap; seed reproducibility; grouped sample caps per
    group.
  - Notebook example: compare full density raster with sampled overlay.

- [ ] `geom_progressive()`
  - Goal: Support progressive/approximate visualization states that refine over
    time or by sample budget.
  - Public API: `geom_progressive(base_geom, steps=(1000, 10000, 100000),
    stat=None, seed=None, show_uncertainty=True, **params)`.
  - Implementation notes: Likely a wrapper that expands into layers or Plotly
    animation frames. Use existing transition frame pattern. Document that this
    is for notebook/HTML exploration rather than live streaming.
  - Tests: creates expected frames; final frame includes all or largest sample;
    uncertainty layer toggles correctly.
  - Notebook example: progressive reveal of dense point cloud.

## Set, Categorical Flow, And Relationship Diagrams

- [ ] `geom_upset()`
  - Goal: Visualize set intersections as a scalable alternative to Venn
    diagrams.
  - Public API: `geom_upset(mapping=None, data=None, sets=None,
    min_size=1, n_intersections=None, sort_by="degree", **params)`.
  - Inputs: either boolean set columns or long form `item`/`set` mappings.
  - Implementation notes: Compute intersection membership matrix, draw top bar
    chart for intersection sizes and dot-matrix panel for set membership.
    This may need a custom subplot figure inside the geom.
  - Tests: intersection counts match hand-computed example; ordering options
    work; long and wide forms both accepted.
  - Notebook example: feature/cohort overlap analysis.

- [ ] `geom_chord()`
  - Goal: Circular category-to-category flow diagram.
  - Public API: `geom_chord(mapping=None, data=None, source=None,
    target=None, weight=None, directed=True, sort=True, **params)`.
  - Implementation notes: Plotly has no native chord trace. Build sectors and
    ribbons using scatter polygons or shapes. Start with aggregate matrix from
    `stat_od_matrix`. Keep labels readable and document limits for many nodes.
  - Tests: total ribbon weights equal input weights; directed/undirected modes
    aggregate correctly; self-loops are handled or documented.
  - Notebook example: customer movement between segments.

- [ ] `geom_arc_diagram()`
  - Goal: Draw relationship arcs above an ordered axis.
  - Public API: `geom_arc_diagram(mapping=None, data=None, source=None,
    target=None, weight=None, node_order=None, curvature=0.5, **params)`.
  - Implementation notes: Place nodes on a line, draw semicircular Bezier arcs.
    Support categorical labels and optional node point/label layer.
  - Tests: node order respected; arc endpoints align to node positions; weight
    maps to linewidth.
  - Notebook example: dependencies between ordered process stages.

- [ ] `geom_parallel_sets()`
  - Goal: Show categorical flow across multiple dimensions, more general than
    alluvium.
  - Public API: `geom_parallel_sets(mapping=None, data=None, axes=None,
    weight=None, fill=None, alpha=0.6, **params)`.
  - Inputs: wide categorical columns listed in `axes`; optional weight column.
  - Implementation notes: Compute strata per axis and ribbons between adjacent
    axes. Can share some logic with alluvium but should support more than
    three categorical dimensions cleanly.
  - Tests: weighted totals preserved between axes; axis order respected;
    missing values handled.
  - Notebook example: product -> region -> channel -> outcome.

## Network, Hierarchy, And Knowledge Graph Views

- [ ] `geom_hive()`
  - Goal: Deterministic radial network visualization using axes instead of
    force-directed randomness.
  - Public API: `geom_hive(mapping=None, data=None, axis=None, radius=None,
    node=None, group=None, **params)`.
  - Inputs: node table with node, axis, radius, optional label/color/size.
  - Implementation notes: Draw nodes in polar-to-Cartesian coordinates. Pair
    with `geom_hive_edges` for links.
  - Tests: axis angles and radial positions are deterministic; labels align;
    empty axes do not crash.
  - Notebook example: explainable network with nodes grouped by role.

- [ ] `geom_hive_edges()`
  - Goal: Draw curved edges between hive plot axes.
  - Public API: `geom_hive_edges(mapping=None, data=None, from=None,
    to=None, node_data=None, curvature=0.25, weight=None, **params)`.
  - Implementation notes: Join edge list to hive node coordinates, draw Bezier
    curves. Support edge color/alpha/width.
  - Tests: joins fail clearly for missing nodes; edge starts/ends match node
    coordinates; weight maps to line width.
  - Notebook example: hive nodes plus edges in one plot.

- [ ] `geom_kg_map()`
  - Goal: Map view for spatiotemporal knowledge graph entities and relations.
  - Public API: `geom_kg_map(mapping=None, data=None, relation_data=None,
    entity_id=None, lon=None, lat=None, time=None, **params)`.
  - Implementation notes: Draw entity points and optional relation arcs on a
    map. Should preserve `data_id` and tooltip metadata for linking.
  - Tests: entity points and relation traces render; time filtering/faceting
    works; missing coordinates are dropped only with `na_rm=True`.
  - Notebook example: incidents, assets, and relations across a region.

- [ ] `geom_kg_tree()`
  - Goal: Tree/hierarchy projection for knowledge graph subsets.
  - Public API: `geom_kg_tree(mapping=None, data=None, root=None,
    parent=None, child=None, layout="tidy", **params)`.
  - Implementation notes: Use networkx or a small tidy-tree layout. Output
    edge and node traces; support labels and depth coloring.
  - Tests: root placement deterministic; depth ordering correct; cycles raise
    a helpful error or are broken explicitly.
  - Notebook example: taxonomy or incident causal hierarchy.

- [ ] `geom_kg_net()`
  - Goal: Network projection for knowledge graph entities and typed relations.
  - Public API: `geom_kg_net(mapping=None, data=None, relation_type=None,
    layout="spring", seed=1, **params)`.
  - Implementation notes: Build on existing `graph_layout`, `geom_edge_link`,
    and node geoms but add relation types, direction, and entity metadata.
  - Tests: relation types map to linetype/color; layout seed reproducible;
    directed arrows optional.
  - Notebook example: typed entity-relation network.

- [ ] `facet_time_graph()`
  - Goal: Facet or animate graph/network views over time slices.
  - Public API: `facet_time_graph(time, ncol=None, cumulative=False,
    layout_stability="fixed", **params)`.
  - Implementation notes: Compute one layout across all time slices by default
    so nodes do not jump between facets. Allow cumulative edge display.
  - Tests: fixed layout coordinates identical across panels; cumulative mode
    includes previous edges; missing time values handled.
  - Notebook example: evolving incident or trade network.

- [ ] `geom_hyperbolic_graph()`
  - Goal: Visualize large hierarchies in a Poincare disk / hyperbolic layout.
  - Public API: `geom_hyperbolic_graph(mapping=None, data=None,
    layout="poincare", root=None, focus=None, **params)`.
  - Implementation notes: Implement or wrap `layout_poincare()`. Draw disk
    boundary, edges, nodes, and labels. Keep coordinates in unit disk.
  - Tests: all node coordinates are inside unit disk; root/focus location is
    stable; hierarchy levels increase radially.
  - Notebook example: package/module hierarchy or taxonomy.

- [ ] `layout_poincare()`
  - Goal: Compute hyperbolic/Poincare disk node positions for trees or DAGs.
  - Public API: `layout_poincare(edges, root=None, radius_step=None,
    angular_spacing="subtree", **params)`.
  - Implementation notes: Start with a deterministic radial tree layout mapped
    into the Poincare disk. Advanced hyperbolic optimization can be later.
  - Tests: deterministic output; handles one node, chain, balanced tree;
    raises on disconnected graph unless `component` behavior is specified.
  - Notebook example: compare Euclidean tree layout vs Poincare layout.

## Topological Data Analysis

- [ ] `stat_mapper()`
  - Goal: Compute a Mapper graph from high-dimensional data.
  - Public API: `stat_mapper(mapping=None, data=None, filter=None,
    cover_bins=10, overlap=0.3, clusterer=None, metric="euclidean",
    **params)`.
  - Implementation notes: Keep optional dependencies optional. A minimal
    implementation can use sklearn clustering and interval covers. Output node
    table and edge table or a bundled object consumed by `geom_mapper`.
  - Tests: simple two-cluster data produces expected node/edge counts; overlap
    changes connectivity; empty input stable.
  - Notebook example: Mapper graph of synthetic manifold data.

- [ ] `geom_mapper()`
  - Goal: Draw Mapper graph output with node size/color summaries.
  - Public API: `geom_mapper(mapping=None, data=None, node_data=None,
    edge_data=None, layout="spring", **params)`.
  - Implementation notes: Accept stat output directly and use graph geoms under
    the hood. Node size should map to member count; color to summary value.
  - Tests: draws nodes and edges from stat output; hover shows member counts;
    colorbar works for continuous summaries.
  - Notebook example: Mapper graph with linked scatter reference.

- [ ] `geom_persistence_diagram()`
  - Goal: Draw birth/death topological persistence points.
  - Public API: `geom_persistence_diagram(mapping=None, data=None,
    birth='birth', death='death', dimension='dimension', **params)`.
  - Implementation notes: Draw diagonal reference line, points colored by
    homology dimension, optional infinite-death handling.
  - Tests: diagonal spans plot range; infinite deaths are clipped or marked;
    dimension legend stable.
  - Notebook example: persistence diagram for synthetic circle/noise data.

- [ ] `geom_barcode()`
  - Goal: Draw persistence barcode intervals.
  - Public API: `geom_barcode(mapping=None, data=None, birth='birth',
    death='death', dimension='dimension', **params)`.
  - Implementation notes: Sort intervals by dimension and lifetime, draw
    horizontal segments.
  - Tests: segment endpoints equal birth/death; sorting deterministic;
    infinite intervals are visually indicated.
  - Notebook example: barcode paired with persistence diagram.

## Uncertainty And Decision Analytics

- [ ] `geom_hypothetical_outcomes()`
  - Goal: Show uncertainty distributions as animated or tiled hypothetical
    outcome draws.
  - Public API: `geom_hypothetical_outcomes(mapping=None, data=None,
    draw=None, n_frames=None, mode="animation", **params)`.
  - Implementation notes: Use Plotly frames for outcome draws, or small
    multiples if animation is disabled.
  - Tests: frame count matches draws; static mode produces expected facets;
    deterministic ordering by draw id.
  - Notebook example: simulation uncertainty for forecasted KPI.

- [ ] `geom_ensemble_fan()`
  - Goal: Draw quantile/fan intervals from ensemble simulations.
  - Public API: `geom_ensemble_fan(mapping=None, data=None, x=None,
    y=None, group=None, probs=(0.5, 0.8, 0.95), **params)`.
  - Implementation notes: Compute quantiles by x and draw nested ribbons.
    Existing fanchart code may be reusable; this should be grammar-friendly.
  - Tests: quantile bands nested correctly; median line optional; grouped
    ensembles work.
  - Notebook example: probabilistic forecast fan.

- [ ] `geom_uncertainty_surface()`
  - Goal: Show uncertainty or loss surfaces over two input dimensions.
  - Public API: `geom_uncertainty_surface(mapping=None, data=None,
    x=None, y=None, z=None, mode="heatmap", contours=True, **params)`.
  - Implementation notes: Use heatmap/contour/surface depending on mode.
    Should work with gridded data and optionally interpolate scattered data.
  - Tests: gridded z shape correct; contour mode creates contour traces;
    missing grid cells handled.
  - Notebook example: objective uncertainty over parameter space.

- [ ] `geom_decision_frontier()`
  - Goal: Draw Pareto frontiers and feasible/infeasible decision regions.
  - Public API: `geom_decision_frontier(mapping=None, data=None,
    objective_x=None, objective_y=None, feasible=None, label=None,
    **params)`.
  - Implementation notes: Compute nondominated points for minimize/maximize
    directions. Draw all candidates, highlight frontier, optional labels.
  - Tests: Pareto set matches hand-computed example; direction arguments work;
    feasible mask affects frontier.
  - Notebook example: cost/risk frontier for candidate policies.

## Causal And Model Explanation Visuals

- [ ] `geom_dag()`
  - Goal: Draw directed acyclic graphs for causal structure.
  - Public API: `geom_dag(mapping=None, data=None, from=None, to=None,
    layout="sugiyama", node_data=None, **params)`.
  - Implementation notes: Use deterministic layered layout. Highlight
    treatments, outcomes, colliders, or adjusted variables via node metadata.
  - Tests: DAG ordering respects edges; cycles raise clear errors; node styles
    map from metadata.
  - Notebook example: treatment -> mediator -> outcome causal DAG.

- [ ] `geom_counterfactual_paths()`
  - Goal: Visualize actual vs counterfactual trajectories per entity.
  - Public API: `geom_counterfactual_paths(mapping=None, data=None,
    id=None, scenario=None, time=None, value=None, actual="actual",
    **params)`.
  - Implementation notes: Draw paired paths by id/scenario, with actual path
    emphasized and counterfactuals lighter or dashed.
  - Tests: sorting by time; scenario linetype mapping; actual scenario
    highlighted.
  - Notebook example: intervention effect over time for sample entities.

- [ ] `geom_treatment_effect()`
  - Goal: Draw average/conditional treatment effect intervals.
  - Public API: `geom_treatment_effect(mapping=None, data=None,
    estimate=None, ymin=None, ymax=None, group=None, **params)`.
  - Implementation notes: Can wrap pointrange/errorbar geoms but should have
    treatment-effect-friendly defaults and labels.
  - Tests: intervals and points align; group/facet support; zero reference line
    optional.
  - Notebook example: subgroup treatment effect forest plot.

- [ ] `geom_ice()`
  - Goal: Individual Conditional Expectation curves for model explanations.
  - Public API: `geom_ice(mapping=None, data=None, feature=None,
    prediction=None, id=None, center=False, alpha=0.15, **params)`.
  - Implementation notes: Draw many grouped lines with optional centered ICE.
    Add optional PDP overlay in same helper or via `geom_pdp`.
  - Tests: one line per id; centered mode subtracts baseline; PDP overlay
    optional.
  - Notebook example: model response to feature across observations.

- [ ] `geom_pdp()`
  - Goal: Partial Dependence Plot summary curve.
  - Public API: `geom_pdp(mapping=None, data=None, feature=None,
    prediction=None, ymin=None, ymax=None, **params)`.
  - Implementation notes: Aggregate predictions by feature value, draw line
    and optional interval ribbon.
  - Tests: mean aggregation correct; intervals drawn when present; supports
    categorical features.
  - Notebook example: PDP plus ICE overlay.

- [ ] `geom_shap_beeswarm()`
  - Goal: SHAP-style feature attribution beeswarm.
  - Public API: `geom_shap_beeswarm(mapping=None, data=None,
    feature=None, shap=None, value=None, max_features=20, **params)`.
  - Implementation notes: Sort features by mean absolute attribution, use
    beeswarm/quasirandom y offsets, color by feature value.
  - Tests: feature ordering correct; max feature filtering; color scale works.
  - Notebook example: model explanation beeswarm for synthetic features.

- [ ] `geom_calibration()`
  - Goal: Model calibration/reliability diagram.
  - Public API: `geom_calibration(mapping=None, data=None, truth=None,
    estimate=None, bins=10, confidence=True, **params)`.
  - Implementation notes: Bin predicted probabilities, compute observed event
    rate, draw diagonal reference and optional binomial confidence intervals.
  - Tests: bin summaries match expected values; diagonal trace present;
    handles empty bins.
  - Notebook example: calibrated vs overconfident classifier.

## Embeddings And ML Exploration

- [ ] `stat_umap()`
  - Goal: Compute 2D UMAP embeddings from high-dimensional feature columns.
  - Public API: `stat_umap(mapping=None, data=None, columns=None,
    n_neighbors=15, min_dist=0.1, metric="euclidean", seed=1, **params)`.
  - Implementation notes: Optional `umap-learn` dependency. If absent, raise a
    clear ImportError when used. Output `x`, `y`, and original metadata.
  - Tests: deterministic with seed; output row count equals input; metadata
    columns preserved.
  - Notebook example: clustered synthetic high-dimensional observations.

- [ ] `stat_tsne()`
  - Goal: Compute 2D t-SNE embeddings.
  - Public API: `stat_tsne(mapping=None, data=None, columns=None,
    perplexity=30, learning_rate="auto", seed=1, **params)`.
  - Implementation notes: Use sklearn TSNE already available through project
    dependency if compatible. Keep defaults stable for small notebooks.
  - Tests: output shape; seed reproducibility within tolerance; handles small
    sample sizes with clear perplexity checks.
  - Notebook example: t-SNE compared with UMAP.

- [ ] `geom_embedding_density()`
  - Goal: Overlay density contours/heatmaps on embedding scatter plots.
  - Public API: `geom_embedding_density(mapping=None, data=None,
    bins=100, contour=True, fill=True, **params)`.
  - Implementation notes: Build on `stat_density_2d` and `geom_contour` or
    heatmap. Must handle overplotting and continuous colorbars.
  - Tests: density grid nonempty; contours render; works when layered below
    `geom_point`.
  - Notebook example: embedding scatter with density background.

- [ ] `geom_cluster_hull()`
  - Goal: Draw convex or concave hulls around embedding clusters.
  - Public API: `geom_cluster_hull(mapping=None, data=None, group=None,
    hull="convex", alpha=0.2, expand=0, **params)`.
  - Implementation notes: Start with scipy convex hull. Concave hull can be
    optional or later. Draw filled polygon per cluster.
  - Tests: hull encloses cluster points for simple shapes; groups with fewer
    than three points handled; alpha/fill respected.
  - Notebook example: cluster hulls on UMAP/t-SNE embedding.

## Dense Time-Series And Analytical Matrices

- [ ] `geom_horizon()`
  - Goal: Compact horizon graph for dense time-series comparison.
  - Public API: `geom_horizon(mapping=None, data=None, bands=3,
    origin=0, positive_colors=None, negative_colors=None, **params)`.
  - Required aesthetics: `x`, `y`; optional `group`.
  - Implementation notes: Split positive/negative values into bands, fold
    bands over baseline, draw layered area traces.
  - Tests: band assignment correct; negative values use negative palette;
    grouped series render separately or facet cleanly.
  - Notebook example: many sensor time series in compact panels.

- [ ] `geom_streamgraph()`
  - Goal: Smoothed stacked area chart with centered/wiggle baseline.
  - Public API: `geom_streamgraph(mapping=None, data=None,
    baseline="wiggle", smoothing=None, **params)`.
  - Required aesthetics: `x`, `y`, `fill` or `group`.
  - Implementation notes: Compute stacked offsets with baseline strategy.
    Support negative-value rejection or documented behavior.
  - Tests: total stack height equals group sum; baseline options deterministic;
    missing time/category combinations filled with zero.
  - Notebook example: topic/category composition over time.

- [ ] `geom_clustermap()`
  - Goal: Heatmap with row/column dendrogram ordering.
  - Public API: `geom_clustermap(mapping=None, data=None, x=None,
    y=None, fill=None, cluster_rows=True, cluster_cols=True,
    method="average", metric="euclidean", **params)`.
  - Implementation notes: Use scipy hierarchical clustering. Compose heatmap
    with dendrogram traces or at least reorder axes initially.
  - Tests: row/column order changes for clusterable matrix; disabled clustering
    preserves input order; missing values handled.
  - Notebook example: clustered feature correlation or expression matrix.

- [ ] `geom_dendro_heatmap()`
  - Goal: Explicit dendrogram plus heatmap layout.
  - Public API: `geom_dendro_heatmap(matrix=None, row_linkage=None,
    col_linkage=None, labels=None, **params)`.
  - Implementation notes: More specialized than `geom_clustermap`, likely a
    helper returning a composed Plotly figure. Keep it compatible with ggplotly
    layer addition if practical.
  - Tests: subplot count and axes alignment; linkage order matches scipy;
    labels not clipped.
  - Notebook example: clustered matrix with dendrograms on top/left.

## Specialized Coordinate Systems

- [ ] `geom_ternary()`
  - Goal: Plot three-part compositional data on ternary axes.
  - Public API: `geom_ternary(mapping=None, data=None, a=None, b=None,
    c=None, color=None, size=None, **params)`.
  - Required aesthetics: `a`, `b`, `c`; optional `color`, `size`, `label`.
  - Implementation notes: Use Plotly `Scatterternary`. Validate that
    compositions are nonnegative; optionally normalize rows to sum to one.
  - Tests: creates scatterternary trace; normalization works; invalid negative
    values raise clear error.
  - Notebook example: product mix or soil composition ternary plot.
