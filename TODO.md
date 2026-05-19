# TODO: Easy-To-Hard Visualization Roadmap

This roadmap groups the remaining ggplotly work into project-sized chunks,
ordered from easiest to hardest. Work through the projects in order unless a
user need or dependency makes a later project urgent.

The list includes:

- ggplot2 parity work from `GGPLOT2_GAP_ANALYSIS.md`.
- Advanced visualization recommendations not already implemented in the
  `advanced-visual-grammar` branch.
- Existing `geom_edgebundle()` support is intentionally excluded.

## Working Contract For Every Project

- Preserve ggplot2-style names: prefer `na_rm`, `show_legend`, `binwidth`,
  `bins`, `breaks`, `labels`, `limits`, `position`, `stat`, `geom`,
  `linewidth`, `lineend`, `linejoin`, `orientation`, and `inherit_aes` when
  they map to ggplot2 concepts.
- Keep any existing Pythonic aliases only as backward-compatible aliases. The
  ggplot2/R-compatible spelling should be canonical in docs and examples.
- Keep stat transforms pure: dataframe in, dataframe plus mapping updates out.
- Keep Plotly mutation inside geom draw methods, scale apply methods, theme
  application, or final figure composition.
- Add exports in `ggplotly/geoms/__init__.py`, `ggplotly/stats/__init__.py`,
  `ggplotly/scales/__init__.py`, and top-level `ggplotly/__init__.py` when a
  feature is public.
- Add focused pytest coverage. Tests should assert trace type, key coordinates,
  scale/legend behavior, empty-data behavior, alias imports, and mapping
  updates, not only that drawing succeeds.
- Add or extend a docs/gallery notebook for visual behavior.
- Verification for visual work:
  - Run targeted pytest.
  - Run full pytest when touching shared draw/stat/scale/facet/coord/theme
    behavior.
  - Execute impacted notebooks.
  - Render HTML.
  - Capture chart PNGs with Node/NPM Playwright, not desktop Chrome/Kaleido.
  - Review each PNG against chart intent.

## Difficulty Rubric

- Easy: mostly tests, docs, aliases, wrappers, or dataframe transforms with
  little Plotly layout risk.
- Medium: visible rendering work using existing Plotly trace types and local
  grammar patterns.
- Hard: broad shared APIs, layout composition, optional dependencies, or charts
  that need custom geometry.
- Frontier: research-heavy, math-heavy, performance-heavy, or likely to require
  new layout abstractions.

## Easy

### Project 01: ggplot2 Parity Guardrails

- [ ] Build the parity safety harness before adding more parity features.
  - Goal: make missing ggplot2 names and accidental Pythonic renames visible in
    tests.
  - Included work:
    - [ ] Add a grouped expected ggplot2 API list from the official ggplot2
      reference index.
    - [ ] Compare that list to `ggplotly.__all__`.
    - [ ] Add import/export tests for `color`/`colour` aliases.
    - [ ] Add import/export tests for compact vs underscore aliases, such as
      `geom_bin2d()` and `geom_bin_2d()`, where ggplot2 supports both.
    - [ ] Add constructor signature tests for high-use geoms, stats, scales,
      facets, guides, coords, and themes.
    - [ ] Audit public argument names and document any intentional Python-only
      deviation.
  - Tests: this should be a pure pytest project; no notebook is required unless
    the audit finds visible behavior changes.
  - Notes: this is the safest first project because it prevents future parity
    work from drifting away from ggplot2 naming.

### Project 02: Dataset And Example Compatibility Checks

- [x] Add ggplot2 dataset parity checks.
  - Goal: make translated ggplot2 examples load expected data with expected
    columns and basic dtypes.
  - Datasets to verify: `diamonds`, `economics`, `economics_long`,
    `faithfuld`, `luv_colours`, `midwest`, `mpg`, `msleep`, `presidential`,
    `seals`, and `txhousing`.
  - Tests: availability, expected column names, stable row counts where the
    local dataset intentionally mirrors ggplot2, and basic dtype behavior for
    dates, categories, numerics, and strings.
  - Notebook: optional. Add one only if a dataset issue changes visible output.

### Project 03: Low-Risk ggplot2 Alias And Wrapper Pass

- [x] Add aliases and thin wrappers that should not change rendering behavior.
  - Goal: improve drop-in compatibility without touching shared rendering math.
  - Included APIs:
    - [x] `geom_bin_2d()` alias for existing `geom_bin2d()`.
    - [x] `stat_bin_2d()` alias for existing `stat_bin2d()`.
    - [x] `stat_density2d()` alias for existing `stat_density_2d()`.
    - [x] `geom_density2d()` and `geom_density_2d()` wrappers over 2D density
      stat plus contour rendering.
    - [x] `geom_density2d_filled()` and `geom_density_2d_filled()` wrappers
      over 2D filled density stat plus filled contour rendering.
    - [x] `stat_contour_filled()` export if existing contour-filled internals
      can support it directly.
    - [x] `stat_sf()` no-op/simple-feature stat wrapper if `geom_sf()` already
      owns geometry handling.
    - [x] `guide_colourbar()` alias for `guide_colorbar()`.
    - [x] `guide_coloursteps()` alias when colorsteps support exists. Not
      applicable in Project 03 because `guide_colorsteps()` support does not
      exist yet; Project 06 owns color-steps guide support.
  - Tests: import/export, alias identity or compatible class, basic draw for
    geom wrappers, and no behavior change for existing names.
  - Notebook: add a small ggplot2-parity notebook cell only if wrapper behavior
    is visual.

### Project 04: Simple Core Stats And No-Op Geoms

- [x] Add the pure or nearly pure ggplot2 primitives.
  - Goal: cover common translated code paths with low Plotly risk.
  - Included APIs:
    - [x] `geom_blank(mapping=None, data=None, show_legend=False, **params)`.
      It should train scales and limits but produce no visible trace.
    - [x] `stat_unique(mapping=None, data=None, na_rm=False, **params)`.
      It should return unique rows over mapped aesthetics and grouping columns.
    - [x] `stat_align(mapping=None, data=None, **params)`. It should align
      area/ribbon-like groups to a shared x-domain with deterministic
      interpolation.
    - [x] `stat_summary_hex(mapping=None, data=None, bins=30, fun="mean",
      na_rm=False, **params)`. It should aggregate `z`/`weight` values over
      existing hex-bin logic.
    - [x] `stat_ydensity(mapping=None, data=None, bw="nrd0", adjust=1,
      kernel="gaussian", trim=True, scale="area", na_rm=False, **params)`.
      It should expose violin-compatible density columns as a public stat.
    - [x] `geom_function(mapping=None, data=None, fun=None, xlim=None,
      n=101, args=None, **params)` as a wrapper over `stat_function()` plus a
      line geom.
    - [x] `geom_quantile(mapping=None, data=None, quantiles=(0.25, 0.5, 0.75),
      formula=None, method="rq", **params)` as a wrapper over
      `stat_quantile()` plus paths.
  - Tests: empty data, grouping, alias imports, computed columns, scale
    training for `geom_blank()`, area alignment, hex summary aggregation,
    y-density output, and trace coordinates for wrapper geoms.
  - Notebook: show blank scale training, function overlays, and quantile lines.

## Medium

### Project 05: Core ggplot2 Geometry Primitives

- [ ] Add missing core geoms that use existing Cartesian traces.
  - Goal: close the most visible ggplot2 geom gaps before harder layout work.
  - Included APIs:
    - [ ] `geom_polygon(mapping=None, data=None, stat="identity",
      position="identity", linewidth=None, lineend="butt",
      linejoin="round", na_rm=False, show_legend=True, inherit_aes=True)`.
      Group by `group`, close paths, draw filled Plotly scatter polygons, and
      respect `fill`, `colour`, `alpha`, and `linewidth`.
    - [ ] `geom_curve(mapping=None, data=None, curvature=0.5, angle=90,
      ncp=5, arrow=None, lineend="butt", na_rm=False, **params)`. Generate
      Bezier points from `x`, `y`, `xend`, `yend`.
    - [ ] `geom_spoke(mapping=None, data=None, angle=None, radius=None,
      na_rm=False, **params)`. Convert `angle` and `radius` to segment
      endpoints and delegate to segment-like drawing.
    - [ ] `geom_sf_text(mapping=None, data=None, geometry=None, label=None,
      na_rm=False, **params)`. Compute representative points or centroids.
    - [ ] `geom_sf_label(mapping=None, data=None, geometry=None, label=None,
      na_rm=False, **params)`. Same as sf text with label styling where Plotly
      supports it.
  - Tests: grouped polygons, closed coordinates, fill/outline separation,
    curved path endpoints, spoke endpoint math, sf centroid behavior, empty
    input, and mapped aesthetics.
  - Notebook: polygon, curve annotation, vector field spokes, and sf label/text
    examples.

### Project 06: Color And Fill Scale Parity

- [ ] Complete ggplot2 color/fill scale families.
  - Goal: close the largest drop-in compatibility gap with shared scale
    implementation plus thin wrappers.
  - Included APIs:
    - [ ] Continuous: `scale_colour_continuous()`,
      `scale_color_continuous()`, `scale_fill_continuous()`.
    - [ ] Gradients: `scale_colour_gradient2()`, `scale_color_gradient2()`,
      `scale_fill_gradient2()`, `scale_colour_gradientn()`,
      `scale_color_gradientn()`, `scale_fill_gradientn()`.
    - [ ] Steps: `scale_colour_steps()`, `scale_color_steps()`,
      `scale_fill_steps()`, `scale_colour_steps2()`, `scale_color_steps2()`,
      `scale_fill_steps2()`, `scale_colour_stepsn()`,
      `scale_color_stepsn()`, `scale_fill_stepsn()`.
    - [ ] Palette scales: `scale_colour_distiller()`,
      `scale_color_distiller()`, `scale_fill_distiller()`,
      `scale_colour_fermenter()`, `scale_color_fermenter()`,
      `scale_fill_fermenter()`, `scale_colour_viridis_c()`,
      `scale_color_viridis_c()`, `scale_colour_viridis_b()`,
      `scale_color_viridis_b()`, `scale_fill_viridis_b()`,
      `scale_colour_hue()`, `scale_color_hue()`, `scale_fill_hue()`,
      `scale_colour_grey()`, `scale_color_grey()`, `scale_fill_grey()`.
    - [ ] Discrete/default aliases: `scale_colour_discrete()`,
      `scale_color_discrete()`, `scale_fill_discrete()`.
    - [ ] Audit existing manual, identity, brewer, and binned color/fill
      scales for full `color`/`colour`/`fill` spelling coverage:
      `scale_color_manual()`, `scale_colour_manual()`,
      `scale_fill_manual()`, `scale_color_identity()`,
      `scale_colour_identity()`, `scale_fill_identity()`,
      `scale_color_brewer()`, `scale_colour_brewer()`,
      `scale_fill_brewer()`, `scale_color_binned()`,
      `scale_colour_binned()`, and `scale_fill_binned()`.
  - Tests: limits, breaks, labels, palettes, direction, midpoint, binned
    boundaries, NA colors, colorbar/legend output, and alias imports.
  - Notebook: one scale comparison notebook with discrete, continuous,
    gradient2, gradientn, steps, brewer, distiller, fermenter, viridis, hue,
    grey, and NA handling examples.

### Project 07: Size, Linewidth, Shape, Linetype, Alpha, And Position Scales

- [ ] Complete non-color scale families and x/y symmetry.
  - Goal: make translated ggplot2 aesthetic scales work consistently across
    points, lines, paths, bars, labels, and facets.
  - Included APIs:
    - [ ] `scale_linewidth()`, `scale_linewidth_continuous()`,
      `scale_linewidth_binned()`, `scale_linewidth_discrete()`,
      `scale_linewidth_identity()`, `scale_linewidth_manual()`.
    - [ ] `scale_size_continuous()`, `scale_size_discrete()`,
      `scale_size_manual()`, `scale_size_area()`, `scale_size_binned()`,
      `scale_size_binned_area()`, `scale_radius()`,
      `scale_size_ordinal()`.
    - [ ] `scale_shape()`, `scale_shape_discrete()`,
      `scale_shape_binned()`.
    - [ ] `scale_linetype()`, `scale_linetype_binned()`,
      `scale_alpha_binned()`.
    - [ ] `scale_x_binned()`, `scale_y_binned()`, `scale_x_log2()`,
      `scale_y_log2()`, `scale_y_date()`, `scale_y_datetime()`,
      `scale_x_time()`, and `scale_y_time()`.
    - [ ] Check whether `scale_discrete_manual()`,
      `scale_continuous_identity()`, and `scale_discrete_identity()` should be
      implemented as public wrappers.
  - Tests: marker sizes, line widths, symbols, dash styles, alpha values,
    guides, date/datetime preservation, transformed axes, reversed ranges, and
    interactions with stats.
  - Notebook: scale matrix showing points, lines, dates, datetimes, binned
    axes, and guide behavior.

### Project 08: Themes And Theme Element Parity

- [ ] Complete ggplot2 theme families and element helpers.
  - Goal: make translated ggplot2 theme code render close enough for visual
    parity.
  - Included APIs:
    - [ ] `theme_gray()`, `theme_grey()`, `theme_bw()`, `theme_light()`,
      `theme_linedraw()`, `theme_void()`, `theme_test()`.
    - [ ] `theme_get()`, `theme_set()`, `theme_update()`,
      `theme_replace()`.
    - [ ] `element_blank()`, `element_geom()`, `element_point()`,
      `element_polygon()`, `margin()`, `margin_part()`, and `rel()`.
  - Implementation notes: if global theme state is introduced, add reset
    helpers and isolate tests to avoid leaking state.
  - Tests: backgrounds, grids, axes, legend boxes, text sizing, relative sizes,
    margins, blanked elements, and theme state reset.
  - Notebook: theme comparison matrix across every built-in theme and selected
    element overrides.

### Project 09: Guides And Annotation Helpers

- [ ] Complete guides and annotation helpers.
  - Goal: close common legend/colorbar/axis-guide and annotation translation
    gaps.
  - Included APIs:
    - [ ] `guide_axis()`, `guide_axis_logticks()`, `guide_axis_stack()`,
      `guide_bins()`, `guide_colorsteps()`, `guide_colourbar()`,
      `guide_coloursteps()`, `guide_none()`, and `guide_custom()`.
    - [ ] `annotation_custom()`, `annotation_logticks()`,
      `annotation_map()`, `annotation_raster()`, `annotation_borders()`, and
      `borders()`.
    - [ ] Audit `guides()` to accept named aesthetics, `None`/`"none"`
      suppression, explicit guide objects, and both `color` and `colour`.
  - Tests: guide suppression, colorbar vs legend selection, binned labels,
    axis label angle/dodging, log tick placement, raster extents, map
    annotation geo context, and spelling aliases.
  - Notebook: guide stress test plus annotation examples on linear, log, and
    map plots.

### Project 10: Facets, Labellers, And Coordinate Parity

- [ ] Expand facets, labellers, and missing coordinate systems.
  - Goal: make common multi-panel translated ggplot2 workflows behave
    predictably.
  - Included APIs:
    - [ ] `facet_null()`.
    - [ ] `vars()`.
    - [ ] `labeller()`, `as_labeller()`, `label_context()`,
      `label_parsed()`, `label_bquote()`, and `label_wrap_gen()`.
    - [ ] Audit `facet_wrap()` arguments: `nrow`, `ncol`, `scales`,
      `shrink`, `labeller`, `as.table`, `switch`, `drop`, `dir`,
      `strip.position`, `axes`, and `axis.labels`.
    - [ ] Audit `facet_grid()` arguments: `rows`, `cols`, `scales`, `space`,
      `shrink`, `labeller`, `as.table`, `switch`, `drop`, `margins`, `axes`,
      and `axis.labels`.
    - [ ] `coord_trans()` and `coord_radial()`.
    - [ ] Decide whether `coord_map()` and `coord_quickmap()` should be
      aliases, documented non-goals, or implemented for legacy compatibility.
  - Tests: free scales, strip labels, wrapped labels, margins, panel sizing,
    scale transform vs coord transform behavior, radial axes, polar bars, and
    map aspect behavior.
  - Notebook: nested facets, free scales, long labels, radial/polar examples,
    and coord-transform comparison.

### Project 11: Lower-Priority ggplot2 Utilities

- [ ] Add utility parity where it maps cleanly to Python/Plotly.
  - Goal: support translated ggplot2 workflows without recreating R internals
    that do not fit Plotly.
  - Included APIs to evaluate:
    - [ ] `ggplot_build()`, `layer_data()`, `get_layer_data()`,
      `ggplot_gtable()`, `ggplotGrob()`, `last_plot()`, and `is_ggplot()`.
    - [ ] `update_geom_defaults()` and `update_stat_defaults()`.
    - [ ] `qplot()` and `quickplot()`.
    - [ ] `autoplot()` and `fortify()`.
  - Implementation notes: grid/gtable/S3-style APIs should be compatibility
    shims unless there is a clear Plotly-native equivalent. Avoid global
    mutable defaults unless reset behavior is explicit and tested.
  - Tests: introspection output, layer data extraction, default isolation,
    and clear errors for unsupported R-specific behavior.
  - Notebook: optional unless utilities expose user-visible plots.

### Project 12: Model Explanation And Statistical Diagnostic Views

- [ ] Add model explanation geoms that mostly compose existing traces.
  - Goal: support practical model review visuals without major new layout
    systems.
  - Included APIs:
    - [ ] `geom_treatment_effect(mapping=None, data=None, estimate=None,
      ymin=None, ymax=None, group=None, **params)`.
    - [ ] `geom_ice(mapping=None, data=None, feature=None, prediction=None,
      id=None, center=False, alpha=0.15, **params)`.
    - [ ] `geom_pdp(mapping=None, data=None, feature=None, prediction=None,
      ymin=None, ymax=None, **params)`.
    - [ ] `geom_shap_beeswarm(mapping=None, data=None, feature=None,
      shap=None, value=None, max_features=20, **params)`.
    - [ ] `geom_calibration(mapping=None, data=None, truth=None,
      estimate=None, bins=10, confidence=True, **params)`.
  - Tests: interval alignment, one ICE line per id, centered ICE math, PDP
    aggregation, SHAP feature ordering, max-feature filtering, calibration bin
    summaries, diagonal reference, and empty bins.
  - Notebook: treatment-effect forest plot, ICE/PDP overlay, SHAP beeswarm,
    and calibration/reliability diagram.

### Project 13: Embeddings And Cluster Overlays

- [ ] Add embedding stats and overlays.
  - Goal: support ML exploration while keeping optional dependencies optional.
  - Included APIs:
    - [ ] `stat_umap(mapping=None, data=None, columns=None, n_neighbors=15,
      min_dist=0.1, metric="euclidean", seed=1, **params)`.
    - [ ] `stat_tsne(mapping=None, data=None, columns=None, perplexity=30,
      learning_rate="auto", seed=1, **params)`.
    - [ ] `geom_embedding_density(mapping=None, data=None, bins=100,
      contour=True, fill=True, **params)`.
    - [ ] `geom_cluster_hull(mapping=None, data=None, group=None,
      hull="convex", alpha=0.2, expand=0, **params)`.
  - Implementation notes: `umap-learn` should be optional with a clear
    ImportError only when used. `stat_tsne()` can use sklearn if available.
    Start hull support with scipy convex hull; concave hull can be optional.
  - Tests: deterministic seed behavior, output row count, metadata
    preservation, small-sample perplexity checks, density grid, contour output,
    hulls with fewer than three points, and layered rendering.
  - Notebook: UMAP/t-SNE comparison with density background and cluster hulls.

### Project 14: Analytical Time-Series, Matrices, And Ternary Views

- [ ] Add specialized but bounded analytical views.
  - Goal: cover common dense analytical visual forms that use existing Plotly
    primitives.
  - Included APIs:
    - [ ] `geom_horizon(mapping=None, data=None, bands=3, origin=0,
      positive_colors=None, negative_colors=None, **params)`.
    - [ ] `geom_streamgraph(mapping=None, data=None, baseline="wiggle",
      smoothing=None, **params)`.
    - [ ] `geom_clustermap(mapping=None, data=None, x=None, y=None,
      fill=None, cluster_rows=True, cluster_cols=True, method="average",
      metric="euclidean", **params)`.
    - [ ] `geom_dendro_heatmap(matrix=None, row_linkage=None,
      col_linkage=None, labels=None, **params)`.
    - [ ] `geom_ternary(mapping=None, data=None, a=None, b=None, c=None,
      color=None, size=None, **params)`.
  - Tests: horizon band assignment, negative palette behavior, streamgraph
    stack totals, baseline determinism, missing time/category zeros,
    cluster ordering, disabled clustering preserving order, dendrogram/heatmap
    axis alignment, ternary normalization, and negative-value validation.
  - Notebook: horizon graph, streamgraph, clustermap, dendro heatmap, and
    ternary composition examples.

## Hard

### Project 15: Geospatial Binning, Movement, And Cartograms

- [ ] Add geospatial aggregation and movement analytics.
  - Goal: support spatial workflows beyond simple map points and choropleths.
  - Included APIs:
    - [ ] `stat_od_matrix(mapping=None, data=None, origin=None,
      destination=None, weight=None, fun="sum", drop=True, **params)`.
    - [ ] `geom_od_arc(mapping=None, data=None, curvature=0.35, n=50,
      arrow=False, **params)`.
    - [ ] `geom_flowmap(mapping=None, data=None, curvature=0.25,
      arrow=False, arrow_size=12, great_circle=True, lineend="round",
      na_rm=False, **params)`.
    - [ ] `geom_tripline(mapping=None, data=None, group=None, time=None,
      color=None, size=1, alpha=0.8, **params)`.
    - [ ] `stat_h3bin(mapping=None, data=None, resolution=7, fun="count",
      value=None, na_rm=False, keep_geometry=True, **params)`.
    - [ ] `geom_h3(mapping=None, data=None, stat="h3bin", resolution=7,
      color=None, fill=None, alpha=1, linewidth=0, show_legend=True,
      **params)`.
    - [ ] `geom_h3_choropleth(mapping=None, data=None, h3="h3", fill=None,
      resolution=None, color=None, alpha=1, **params)`.
    - [ ] `geom_cartogram(mapping=None, data=None, map=None, map_id=None,
      fill=None, value=None, method="dorling", **params)`.
  - Implementation notes: keep `h3` optional; raise a clear ImportError only
    when H3 APIs are used. Start cartograms with Dorling circles. Flow maps
    should use `Scattergeo` and handle antimeridian paths defensively. OD
    matrix should be a pure groupby transform usable by flow maps, chord
    diagrams, and arc diagrams.
  - Tests: OD counts and weighted sums, Bezier arc endpoints, flow endpoints,
    great-circle interpolation, width mapping, grouped tripline ordering,
    H3 aggregation totals, H3 GeoJSON/centroid fallback, faceted geo domains,
    Dorling radius scaling, and missing optional dependency errors.
  - Notebook: H3 density at two resolutions, precomputed H3 choropleth,
    freight flow map, tripline GPS paths, OD arc diagram, and Dorling
    cartogram.

### Project 16: Set, Categorical Flow, And Relationship Diagrams

- [ ] Add multi-category relationship diagrams.
  - Goal: support categorical set/flow/network structures that are not simple
    Cartesian geoms.
  - Included APIs:
    - [ ] `geom_upset(mapping=None, data=None, sets=None, min_size=1,
      n_intersections=None, sort_by="degree", **params)`.
    - [ ] `geom_chord(mapping=None, data=None, source=None, target=None,
      weight=None, directed=True, sort=True, **params)`.
    - [ ] `geom_arc_diagram(mapping=None, data=None, source=None,
      target=None, weight=None, node_order=None, curvature=0.5, **params)`.
    - [ ] `geom_parallel_sets(mapping=None, data=None, axes=None,
      weight=None, fill=None, alpha=0.6, **params)`.
  - Implementation notes: UpSet likely needs a composed subplot-style figure.
    Chord diagrams need custom sectors and ribbons because Plotly has no
    native chord trace. Parallel sets can share logic with alluvium but must
    handle more than three categorical dimensions.
  - Tests: intersection counts, long/wide set input, chord total weights,
    directed/undirected aggregation, self-loop behavior, arc endpoint
    alignment, node ordering, weighted totals between parallel-set axes,
    missing values, labels, and legend behavior.
  - Notebook: feature/cohort overlap UpSet, customer movement chord,
    process-dependency arc diagram, and product-region-channel-outcome
    parallel sets.

### Project 17: Causal, Counterfactual, And Decision Visuals

- [ ] Add causal and decision-analysis visuals.
  - Goal: support high-value statistical workflows that require careful
    semantics but mostly use known traces.
  - Included APIs:
    - [ ] `geom_dag(mapping=None, data=None, from=None, to=None,
      layout="sugiyama", node_data=None, **params)`.
    - [ ] `geom_counterfactual_paths(mapping=None, data=None, id=None,
      scenario=None, time=None, value=None, actual="actual", **params)`.
    - [ ] `geom_hypothetical_outcomes(mapping=None, data=None, draw=None,
      n_frames=None, mode="animation", **params)`.
    - [ ] `geom_ensemble_fan(mapping=None, data=None, x=None, y=None,
      group=None, probs=(0.5, 0.8, 0.95), **params)`.
    - [ ] `geom_uncertainty_surface(mapping=None, data=None, x=None, y=None,
      z=None, mode="heatmap", contours=True, **params)`.
    - [ ] `geom_decision_frontier(mapping=None, data=None,
      objective_x=None, objective_y=None, feasible=None, label=None,
      **params)`.
  - Implementation notes: DAG layout must be deterministic and reject cycles
    clearly. Counterfactual paths should emphasize actual vs alternatives.
    Ensemble fan can reuse fanchart/ribbon logic. Decision frontier must
    compute nondominated points for configurable objective directions.
  - Tests: DAG ordering and cycle errors, path sorting by time, actual scenario
    highlighting, frame count for hypothetical outcomes, nested quantile bands,
    gridded surface handling, contour output, Pareto set correctness, feasible
    masks, and labels.
  - Notebook: causal DAG, counterfactual trajectories, hypothetical outcomes,
    ensemble fan, uncertainty surface, and cost/risk frontier.

### Project 18: Large-Data Rendering And Approximation

- [ ] Add large-data rendering and approximation primitives.
  - Goal: keep visual exploration usable for large point/line datasets without
    emitting huge Plotly vector traces.
  - Included APIs:
    - [ ] `stat_rasterize(mapping=None, data=None, width=512, height=512,
      aggregator="count", limits=None, **params)`.
    - [ ] `geom_datashade(mapping=None, data=None, width=800, height=500,
      aggregator="count", cmap="viridis", dynamic=False, **params)`.
    - [ ] `stat_density_canvas(mapping=None, data=None, width=512,
      height=512, bandwidth=None, method="kde", **params)`.
    - [ ] `stat_sketch(mapping=None, data=None, method="tdigest", bins=100,
      by=None, **params)`.
    - [ ] `stat_reservoir_sample(mapping=None, data=None, n=10000,
      seed=None, by=None, **params)`.
    - [ ] `geom_progressive(base_geom, steps=(1000, 10000, 100000),
      stat=None, seed=None, show_uncertainty=True, **params)`.
  - Implementation notes: prefer optional `datashader` if installed, but keep
    a numpy histogram2d fallback for count aggregation. Sketches should have a
    pandas fallback and deterministic sampling where applicable. Progressive
    output likely maps to Plotly animation frames or expanded layers.
  - Tests: bin totals, extents, clipping, density grid shape, nonnegative
    density, constant input, approximate quantile tolerance, sample caps, seed
    reproducibility, grouped reservoirs, frame counts, final frame content, and
    no-op empty input.
  - Notebook: million-point datashade/raster example, density canvas,
    approximate distribution sketch, reservoir-sampled overlay, and progressive
    reveal.

## Frontier

### Project 19: Knowledge Graph And Hierarchy Views

- [ ] Add knowledge graph, hierarchy, and stable time-faceted graph views.
  - Goal: support complex graph exploration with deterministic layouts and
    domain metadata.
  - Included APIs:
    - [ ] `geom_kg_map(mapping=None, data=None, relation_data=None,
      entity_id=None, lon=None, lat=None, time=None, **params)`.
    - [ ] `geom_kg_tree(mapping=None, data=None, root=None, parent=None,
      child=None, layout="tidy", **params)`.
    - [ ] `geom_kg_net(mapping=None, data=None, relation_type=None,
      layout="spring", seed=1, **params)`.
    - [ ] `facet_time_graph(time, ncol=None, cumulative=False,
      layout_stability="fixed", **params)`.
    - [ ] `geom_hive(mapping=None, data=None, axis=None, radius=None,
      node=None, group=None, **params)`.
    - [ ] `geom_hive_edges(mapping=None, data=None, from=None, to=None,
      node_data=None, curvature=0.25, weight=None, **params)`.
  - Implementation notes: build on existing `graph_layout`,
    `geom_edge_link()`, `geom_node_point()`, and `geom_node_text()` when
    possible. Graph facets should use one layout across all time slices by
    default to avoid node jumping. Hive layouts should be deterministic.
  - Tests: entity/relation traces, map relation arcs, missing coordinate
    handling, tree root/depth ordering, cycle errors, relation type styling,
    layout seed reproducibility, fixed coordinates across time panels,
    cumulative mode, hive axis/radius coordinates, and edge joins.
  - Notebook: spatiotemporal KG map, causal or taxonomy tree, typed KG network,
    evolving graph facets, and hive plot.

### Project 20: Hyperbolic Graph Layouts

- [ ] Add Poincare/hyperbolic hierarchy visualization.
  - Goal: support large hierarchy views where Euclidean tree layouts waste
    space.
  - Included APIs:
    - [ ] `layout_poincare(edges, root=None, radius_step=None,
      angular_spacing="subtree", **params)`.
    - [ ] `geom_hyperbolic_graph(mapping=None, data=None,
      layout="poincare", root=None, focus=None, **params)`.
  - Implementation notes: start with a deterministic radial tree layout mapped
    into the Poincare disk. Draw disk boundary, edges, nodes, and labels. More
    advanced hyperbolic optimization can come later.
  - Tests: deterministic output, one-node/chain/balanced-tree cases,
    disconnected graph errors unless behavior is specified, all coordinates
    inside the unit disk, root/focus stability, and radial depth ordering.
  - Notebook: Euclidean tree vs Poincare disk comparison.

### Project 21: Topological Data Analysis

- [ ] Add Mapper and persistence visualizations.
  - Goal: cover complex shape/topology workflows for high-dimensional data.
  - Included APIs:
    - [ ] `stat_mapper(mapping=None, data=None, filter=None, cover_bins=10,
      overlap=0.3, clusterer=None, metric="euclidean", **params)`.
    - [ ] `geom_mapper(mapping=None, data=None, node_data=None,
      edge_data=None, layout="spring", **params)`.
    - [ ] `geom_persistence_diagram(mapping=None, data=None, birth="birth",
      death="death", dimension="dimension", **params)`.
    - [ ] `geom_barcode(mapping=None, data=None, birth="birth",
      death="death", dimension="dimension", **params)`.
  - Implementation notes: keep optional TDA dependencies optional. A minimal
    Mapper implementation can use sklearn clustering and interval covers.
    Persistence geoms can consume precomputed birth/death intervals first,
    with computation added later if dependency choices are clear.
  - Tests: Mapper node/edge counts on synthetic two-cluster data, overlap
    connectivity, empty input, mapper hover/member counts, persistence
    diagonal range, infinite death handling, dimension legends, barcode
    endpoint accuracy, and deterministic sorting.
  - Notebook: Mapper graph with linked reference scatter, persistence diagram,
    and barcode for synthetic manifold/circle data.
