# ggplot2 Gap Analysis

Date: 2026-05-18

Baseline source: ggplot2 official reference index, version 4.0.3,
https://ggplot2.tidyverse.org/reference/index.html

Local baseline: `advanced-visual-grammar` branch, inspected through
`ggplotly.__all__`.

Local public surface:

| Category | Export count |
| --- | ---: |
| Total exports | 207 |
| Geoms | 74 |
| Stats | 27 |
| Scales | 46 |
| Positions | 10 |
| Coordinates | 5 |
| Facets | 2 |
| Themes | 9 |
| Guides | 2 |

## Scope

This compares ggplotly's public API to core ggplot2, not to extension packages
such as ggrepel, ggridges, ggforce, sf, patchwork, gganimate, ggalluvial, or
ggbeeswarm. ggplotly already includes several extension-like and Plotly-native
capabilities, so the missing work below is primarily about drop-in ggplot2
compatibility.

The analysis is export-level first. Some APIs may have partial behavior behind a
different name, but if ggplot2 code cannot be translated with the expected
function name and arguments, it is treated as a parity gap.

Priority:

- P0: drop-in compatibility blocker or naming/API mismatch.
- P1: common ggplot2 workflow missing or only partially covered.
- P2: useful parity, but less likely to block most chart ports.
- P3: R/S3/grid internals or superseded APIs; implement only if needed.

## Executive Summary

ggplotly covers the core "everyday chart" surface well: scatter, line, path,
bar, col, histogram, boxplot, violin, density, area, ribbon, tile, rect, text,
label, smooth, maps, sf-like maps, facets, positions, and many stats are
present. The advanced branch also adds capabilities beyond ggplot2, including
edge bundling, network geoms, alluvial/mosaic, ridgelines, interval geoms,
patterns, text paths, repel labels, beeswarm/quasirandom, transitions, and
multi-scale support.

The largest gaps versus ggplot2 are:

- Complete scale families. ggplot2 has broad symmetric color/fill, size,
  linewidth, alpha, shape, linetype, date/time, binned, gradient, brewer,
  distiller, fermenter, viridis, hue, grey, identity, and manual scale
  constructors. ggplotly has useful coverage but many names and variants are
  missing.
- Guide, theme, and element helpers. ggplotly exposes only `guide_legend()` and
  `guide_colorbar()`, only three element helpers, and does not expose ggplot2's
  theme state helpers.
- Facet/labeller parity. `facet_wrap()` and `facet_grid()` exist, but ggplot2's
  labeller and facet helper ecosystem is much larger.
- Annotation helpers. `annotate()` exists, but the `annotation_*()` family is
  mostly absent.
- A small set of core geoms/stats and aliases remain missing, including
  `geom_curve()`, `geom_spoke()`, `geom_polygon()`, `geom_blank()`,
  `geom_quantile()`, `geom_function()`, `stat_align()`, `stat_unique()`, and
  `stat_summary_hex()`.
- Coordinate parity needs `coord_trans()` and newer polar/radial behavior.

## P0: Compatibility And Naming

- [ ] Add a generated API parity test that imports the expected ggplot2 names
  and asserts aliases resolve to the intended implementation.
  - Include British/American aliases such as `colour` and `color`.
  - Include underscore aliases where ggplot2 has historical variants, for
    example `geom_bin_2d()` and `stat_bin_2d()` if ggplot2 exposes both forms.
  - Keep Python-callable argument names in ggplot2 style where possible:
    `na_rm`, `show_legend`, `binwidth`, `bins`, `breaks`, `labels`, `limits`,
    `position`, `stat`, `geom`, `linewidth`, and `lineend`.
  - For R names containing dots, consider accepting dotted keys through
    `**params` for generated/transpiled calls, but do not make normal Python
    calls rely on invalid identifiers.

- [ ] Audit all public constructors for accidental Pythonic renames.
  - High-risk areas: advanced geoms/stats recently added, position arguments,
    scale constructors, guide constructors, and map/geospatial helpers.
  - Each fix should preserve any existing Pythonic alias for compatibility, but
    the ggplot2-style spelling should be canonical in docs and examples.

## P1: Core Geoms Missing Or Partial

| ggplot2 API | Local status | Why it matters | Suggested implementation |
| --- | --- | --- | --- |
| `geom_blank()` | Missing | Used to train axes, reserve limits, and build plots incrementally. | Add a no-op geom that still participates in scale training. Test no trace output plus axis limits. |
| `geom_curve()` | Missing | Common for curved annotations and arrows. | Draw quadratic Bezier paths using `x`, `y`, `xend`, `yend`; support `curvature`, `angle`, `ncp`, `arrow`, `lineend`, `linewidth`. |
| `geom_spoke()` | Missing | Polar/vector field shorthand using `angle` and `radius`. | Convert angle/radius to segment endpoints, then delegate to segment drawing. |
| `geom_polygon()` | Missing | Core filled polygon layer; important for maps and custom shapes. | Group by `group`, draw closed filled `Scatter` traces. Respect `fill`, `colour`, `alpha`, `linewidth`. |
| `geom_quantile()` | Missing | ggplot2 pair for `stat_quantile()`. | Wrap `stat_quantile()` plus path drawing. Test multiple quantiles and grouping. |
| `geom_function()` | Missing | ggplot2 pair for `stat_function()`. | Add wrapper over `stat_function()` and line geom. |
| `geom_density_2d()` / `geom_density2d()` | Stat exists, public geom wrapper missing. | Common 2D density contour call. | Alias to contour-style rendering with `stat_density_2d()`. |
| `geom_density_2d_filled()` / `geom_density2d_filled()` | Stat exists, public geom wrapper missing. | Common filled 2D density call. | Alias to filled contour rendering with `stat_density_2d_filled()`. |
| `geom_bin_2d()` | `geom_bin2d()` exists; underscore form should be checked. | ggplot2 code often uses the underscore spelling. | Add alias if missing. |
| `geom_sf_text()` | Missing | Text labels on sf geometries are common in maps. | Compute representative points/centroids and draw geo-aware text. |
| `geom_sf_label()` | Missing | Label boxes on sf geometries are common in maps. | Same as `geom_sf_text()`, with label styling where Plotly supports it. |

Covered well enough already: `geom_point`, `geom_line`, `geom_path`,
`geom_segment`, `geom_rect`, `geom_tile`, `geom_raster`, `geom_text`,
`geom_label`, `geom_bar`, `geom_col`, `geom_histogram`, `geom_freqpoly`,
`geom_boxplot`, `geom_violin`, `geom_density`, `geom_area`, `geom_ribbon`,
`geom_smooth`, `geom_errorbar`, `geom_linerange`, `geom_pointrange`,
`geom_crossbar`, `geom_count`, `geom_contour`, `geom_contour_filled`,
`geom_hex`, `geom_map`, `geom_sf`, `geom_qq`, and `geom_qq_line`.

## P1: Core Stats Missing Or Partial

| ggplot2 API | Local status | Why it matters | Suggested implementation |
| --- | --- | --- | --- |
| `stat_align()` | Missing | ggplot2 uses it for aligned area/ribbon data. | Implement pure x-domain alignment/interpolation for area-like layers. |
| `stat_unique()` | Missing | Useful for de-duplicating plotted rows. | Return unique rows over mapped aesthetics. Test grouping and NA behavior. |
| `stat_summary_hex()` | Missing | Completes summary over hex bins. | Pair with existing `geom_hex()` and aggregate `z`/`weight` by hex bin. |
| `stat_contour_filled()` | Missing export | ggplot2 exposes it separately from `geom_contour_filled()`. | Export wrapper using existing filled contour computation. |
| `stat_bin_2d()` | `stat_bin2d()` exists; underscore alias likely missing. | Drop-in ggplot2 compatibility. | Add alias and import/export tests. |
| `stat_density2d()` | `stat_density_2d()` exists; compact alias likely missing. | ggplot2 has historical alias usage. | Add alias and import/export tests. |
| `stat_ydensity()` | Missing as public API | Underlies violin workflows and is a public ggplot2 stat. | Reuse violin density computation, expose stable computed columns. |
| `stat_sf()` | Missing as public API | ggplot2 exposes sf stat even though users often call `geom_sf()`. | Add no-op/simple-feature stat wrapper if `geom_sf()` already handles geometry. |

Covered well enough already: `stat_identity`, `stat_count`, `stat_bin`,
`stat_density`, `stat_ecdf`, `stat_function`, `stat_summary`,
`stat_summary_bin`, `stat_summary_2d`, `stat_sum`, `stat_ellipse`,
`stat_quantile`, `stat_qq`, `stat_qq_line`, `stat_smooth`, `stat_contour`,
`stat_bin_hex`, `stat_bindot`, `stat_density_2d`,
`stat_density_2d_filled`, `stat_halfeye`, `stat_dotsinterval`,
`stat_alluvium`, and `stat_mosaic`.

## P1: Scale Families

This is the biggest compatibility gap. The current package has 46 scale exports,
but ggplot2's scale surface is broad and highly systematic. Adding these in
families will produce the most compatibility per implementation hour.

### Color And Fill

- [ ] Complete continuous color/fill constructors.
  - Missing or partial names: `scale_colour_continuous()`,
    `scale_color_continuous()`, `scale_fill_continuous()`,
    `scale_colour_gradient2()`, `scale_color_gradient2()`,
    `scale_fill_gradient2()`, `scale_colour_gradientn()`,
    `scale_color_gradientn()`, `scale_fill_gradientn()`.
  - Implementation: share one color-scale implementation with wrappers for
    aesthetic and spelling.
  - Tests: limits, breaks, labels, midpoint, low/mid/high colors, NA color,
    legend title, and colorbar output.

- [ ] Complete binned and stepped color/fill constructors.
  - Missing or partial names: `scale_colour_steps()`, `scale_color_steps()`,
    `scale_fill_steps()`, `scale_colour_steps2()`, `scale_color_steps2()`,
    `scale_fill_steps2()`, `scale_colour_stepsn()`, `scale_color_stepsn()`,
    `scale_fill_stepsn()`.
  - Tests: bin count, boundary handling, guide type, and legend labels.

- [ ] Complete palette-based color/fill constructors.
  - Missing or partial names: `scale_colour_distiller()`,
    `scale_color_distiller()`, `scale_fill_distiller()`,
    `scale_colour_fermenter()`, `scale_color_fermenter()`,
    `scale_fill_fermenter()`, `scale_colour_viridis_c()`,
    `scale_color_viridis_c()`, `scale_colour_viridis_b()`,
    `scale_color_viridis_b()`, `scale_fill_viridis_b()`,
    `scale_colour_hue()`, `scale_color_hue()`, `scale_fill_hue()`,
    `scale_colour_grey()`, `scale_color_grey()`, `scale_fill_grey()`.
  - Tests: palette direction, discrete/continuous behavior, NA handling, and
    aliases.

- [ ] Complete discrete and identity color/fill aliases.
  - Missing or partial names: `scale_colour_discrete()`,
    `scale_color_discrete()`, `scale_fill_discrete()`.
  - Existing identity/manual/brewer names should be audited for both
    `colour` and `color` spellings.

### Size, Linewidth, Shape, Linetype, Alpha

- [ ] Add `scale_linewidth*()` family.
  - Names: `scale_linewidth()`, `scale_linewidth_continuous()`,
    `scale_linewidth_binned()`, `scale_linewidth_discrete()`,
    `scale_linewidth_identity()`, `scale_linewidth_manual()`.
  - Why: ggplot2 moved line width away from `size` for lines.
  - Tests: line traces use width, point size is unaffected, legends are sane.

- [ ] Complete `scale_size*()` family.
  - Missing or partial names: `scale_size_continuous()`,
    `scale_size_discrete()`, `scale_size_manual()`, `scale_size_area()`,
    `scale_size_binned()`, `scale_size_binned_area()`, `scale_radius()`,
    `scale_size_ordinal()`.
  - Tests: range scaling, zero-area behavior, legend labels, mapped numeric
    sizes remain visible.

- [ ] Complete `scale_shape*()` family.
  - Missing or partial names: `scale_shape()`, `scale_shape_discrete()`,
    `scale_shape_binned()`.
  - Existing: `scale_shape_manual()`, `scale_shape_identity()`.
  - Tests: categorical mapping to Plotly marker symbols, unknown symbols fail
    clearly.

- [ ] Complete linetype and alpha variants.
  - Missing or partial names: `scale_linetype()`, `scale_linetype_binned()`,
    `scale_alpha_binned()`.
  - Existing: linetype discrete/manual/identity and alpha
    continuous/discrete/manual/identity.

### Position And Date/Time Scales

- [ ] Complete x/y scale symmetry.
  - Missing or partial names: `scale_x_binned()`, `scale_y_binned()`,
    `scale_x_log2()`, `scale_y_log2()`, `scale_y_date()`,
    `scale_y_datetime()`, `scale_x_time()`, `scale_y_time()`.
  - Existing: x/y continuous/discrete/log10/reverse/sqrt and x date/datetime.
  - Tests: transformed axis values, tick labels, limits, reversed ranges, and
    date/datetime preservation in traces.

- [ ] Add generic manual/identity helpers where ggplot2 exposes them.
  - Names to check against ggplot2 docs before implementing:
    `scale_discrete_manual()`, `scale_continuous_identity()`,
    `scale_discrete_identity()`.
  - Use wrappers only if the behavior is materially compatible.

## P1: Coordinates

| ggplot2 API | Local status | Why it matters | Suggested implementation |
| --- | --- | --- | --- |
| `coord_trans()` | Missing | Common for coordinate-level transforms distinct from scale transforms. | Transform axes after stat computation; test smooth/bin differences vs scale transforms where possible. |
| `coord_radial()` | Missing | Newer ggplot2 radial coordinate surface; more flexible than classic polar. | Build on `coord_polar()`, add radial axis/inner radius/theta semantics as Plotly permits. |
| `coord_map()` / `coord_quickmap()` | Not exposed | Older map workflows may use them. | Lower priority if deprecated in current ggplot2; document as aliases/fallbacks if added. |

Covered already: `coord_cartesian`, `coord_fixed`, `coord_flip`,
`coord_polar`, and `coord_sf`.

## P1: Facets And Labellers

- [ ] Add `facet_null()`.
  - It should explicitly remove faceting and help code that programmatically
    chooses a facet object.

- [ ] Add `vars()` helper for ggplot2-style facet specifications.
  - Python can keep accepting strings/lists, but `vars()` improves translated
    ggplot2 code compatibility.

- [ ] Expand labeller API.
  - Existing: `label_value()`, `label_both()`.
  - Missing or partial: `labeller()`, `as_labeller()`, `label_context()`,
    `label_parsed()`, `label_bquote()`, `label_wrap_gen()`.
  - Tests: strip text for one variable, multiple variables, long labels,
    wrapped labels, and parsed/math-like labels where supported.

- [ ] Audit facet arguments against ggplot2.
  - `facet_wrap()`: `nrow`, `ncol`, `scales`, `shrink`, `labeller`, `as.table`,
    `switch`, `drop`, `dir`, `strip.position`, `axes`, `axis.labels`.
  - `facet_grid()`: `rows`, `cols`, `scales`, `space`, `shrink`, `labeller`,
    `as.table`, `switch`, `drop`, `margins`, `axes`, `axis.labels`.
  - Free scales and panel sizing need notebook visual review, not just unit
    tests.

## P1: Themes And Theme Elements

- [ ] Add missing complete themes and aliases.
  - Missing or partial: `theme_gray()`, `theme_grey()`, `theme_bw()`,
    `theme_light()`, `theme_linedraw()`, `theme_void()`, `theme_test()`.
  - Existing: default, ggplot2, minimal, classic, dark, custom, BBC, NYTimes.
  - Tests: background, grid, axis, legend, and text defaults in rendered
    layout.

- [ ] Add theme state helpers.
  - Missing: `theme_get()`, `theme_set()`, `theme_update()`,
    `theme_replace()`.
  - Implementation note: keep state explicit and test-isolated. If global state
    is introduced, provide reset helpers and avoid leaking state across tests.

- [ ] Add missing element helpers.
  - Missing or partial: `element_blank()`, `element_geom()`,
    `element_point()`, `element_polygon()`, `margin()`, `margin_part()`,
    `rel()`.
  - Existing: `element_text()`, `element_line()`, `element_rect()`.
  - Tests: blanking grid/axis text/legend title, relative font sizes, margins,
    and propagation into Plotly layout.

## P1: Guides And Legends

- [ ] Complete guide constructors.
  - Existing: `guide_legend()`, `guide_colorbar()`.
  - Missing or partial: `guide_axis()`, `guide_axis_logticks()`,
    `guide_axis_stack()`, `guide_bins()`, `guide_colorsteps()`,
    `guide_colourbar()`, `guide_coloursteps()`, `guide_none()`,
    `guide_custom()`.
  - Tests: guide suppression, colorbar vs legend selection, binned labels,
    axis guide label angle/dodging, and spelling aliases.

- [ ] Audit `guides()` behavior.
  - It should accept named aesthetics, `None`/`"none"` suppression, explicit
    guide objects, and both `color` and `colour`.

## P1: Annotation Helpers

- [ ] Add ggplot2 `annotation_*()` helpers.
  - Missing or partial: `annotation_custom()`, `annotation_logticks()`,
    `annotation_map()`, `annotation_raster()`, `annotation_borders()`.
  - Current: generic `annotate()` exists.
  - Tests: annotations do not train scales unless ggplot2 does, log ticks align
    with log axes, raster annotations preserve extents, map annotations respect
    geo/facet context.

- [ ] Add `borders()` if map examples rely on it.
  - This can wrap `map_data()` plus polygon/path geoms.

## P2: Layer, Build, And Convenience Utilities

- [ ] Add user-facing build/introspection helpers.
  - Only implement helpers where behavior makes sense in Python/Plotly.
  - Missing or partial: `ggplot_build()`, `layer_data()`,
    `get_layer_data()`, `ggplot_gtable()`, `ggplotGrob()`, `last_plot()`,
    `is_ggplot()`.
  - Plotly means some grid/gtable helpers may be compatibility shims rather
    than full ports.

- [ ] Add default-update helpers.
  - Missing: `update_geom_defaults()`, `update_stat_defaults()`.
  - Use carefully; global mutable defaults are a test isolation risk.

- [ ] Consider `qplot()` / `quickplot()` only if users request legacy parity.
  - ggplot2 keeps them for convenience/legacy use, but they are not central to
    modern grammar usage.

- [ ] Consider `autoplot()` and `fortify()` compatibility.
  - In R these rely heavily on S3 methods. In Python, prefer explicit adapters
    for pandas, GeoPandas, statsmodels, sklearn, networkx, and xarray rather
    than recreating R dispatch wholesale.

## P2: Datasets

Core ggplot2 datasets appear mostly covered:

- Present locally: `diamonds`, `economics`, `economics_long`, `faithfuld`,
  `luv_colours`, `midwest`, `mpg`, `msleep`, `presidential`, `seals`,
  `txhousing`.
- Extra local datasets: `iris`, `mtcars`, `commodity_prices`,
  `us_flights_nodes`, `us_flights_edges`.

Suggested checks:

- [ ] Add dataset availability tests for every ggplot2 dataset name.
- [ ] Verify column names and dtypes match ggplot2 closely enough for examples
  translated from R.

## P3: Deprioritized Or Conditional Parity

These should not lead the backlog unless a user has real code that needs them:

- R-specific NSE helpers such as `aes_string()`, `aes_()`, `aes_all()`, and
  `aes_at()` if they are deprecated/superseded in ggplot2.
- Grid/gtable internals where Plotly has no direct equivalent.
- Deprecated coordinate/map helpers unless current ggplot2 docs still present
  them and user code depends on them.
- Low-level guide/theme grob internals.

## Existing Capabilities Beyond ggplot2

ggplotly already exceeds core ggplot2 in several areas:

- Interactive Plotly rendering, range sliders, and range selectors.
- 3D geoms: `geom_point_3d()`, `geom_surface()`, `geom_wireframe()`.
- Financial geoms: `geom_candlestick()`, `geom_ohlc()`, `geom_waterfall()`.
- Time-series diagnostics: `geom_acf()`, `geom_pacf()`, `geom_stl()`.
- Uncertainty geoms: `geom_fanchart()`, `geom_slabinterval()`,
  `geom_dotsinterval()`, `stat_halfeye()`.
- Network and flow geoms: `geom_edgebundle()`, `geom_edge_link()`,
  `geom_node_point()`, `geom_node_text()`, `geom_sankey()`.
- Categorical structure: `geom_alluvium()`, `geom_stratum()`,
  `geom_mosaic()`.
- Advanced labels and paths: `geom_text_repel()`, `geom_label_repel()`,
  `geom_textpath()`, `geom_labelpath()`.
- Patterns: `geom_col_pattern()`, `geom_bar_pattern()`,
  `geom_tile_pattern()`.
- Animation helpers: `transition_time()`, `transition_states()`,
  `transition_reveal()`.

These are valuable, but they should not hide ggplot2 parity gaps. A user
expecting drop-in replacement behavior will care more about exact scale,
theme, guide, facet, and argument compatibility than about additional chart
families.

## Recommended Phases

### Phase 1: API Parity Harness

- Add a machine-readable expected ggplot2 API list grouped by category.
- Add import/export tests for aliases and constructor names.
- Add argument-name tests for high-use geoms, stats, scales, facets, themes,
  and guides.
- Do not change rendering behavior except for pure aliases and no-op wrappers.

### Phase 2: Scale Parity

- Implement missing color/fill constructors as shared wrappers first.
- Add size/linewidth/shape/linetype/alpha families next.
- Add x/y date/time/binned/log2 symmetry last.
- Add notebooks that compare discrete, continuous, binned, stepped, viridis,
  brewer, and gradient scales.

### Phase 3: Guides, Themes, Facets, Annotations

- Add guide aliases and missing guide constructors.
- Add complete theme and element helper families.
- Expand labellers and facet arguments.
- Add annotation helpers.
- Visual review should cover legends, colorbars, strips, long labels, and
  theme grids/backgrounds.

### Phase 4: Missing Core Geoms And Stats

- Add `geom_blank()`, `geom_polygon()`, `geom_curve()`, `geom_spoke()`,
  `geom_quantile()`, `geom_function()`, density2d geom aliases, sf text/label,
  `stat_align()`, `stat_unique()`, `stat_summary_hex()`, and stat aliases.
- Each should include focused unit tests and at least one gallery example when
  behavior is visual.

### Phase 5: Lower-Priority Utilities

- Add build/introspection helpers that map cleanly to Plotly.
- Add dataset dtype/column parity checks.
- Add legacy convenience APIs only when user code or examples require them.

## Verification Standard

For each parity batch:

- Run targeted pytest for the changed category.
- Run full pytest when touching shared scale, mapping, facet, coord, theme, or
  drawing code.
- Add or update a docs/gallery notebook for visual behavior.
- Render impacted notebooks to HTML.
- Capture chart PNGs with Node/NPM Playwright using its managed Chromium.
- Inspect each PNG against chart intent, not just existence or non-blankness.
