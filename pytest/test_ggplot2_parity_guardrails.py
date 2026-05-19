"""Static guardrails for ggplot2-compatible public API parity."""

import inspect

import pytest

import ggplotly


PUBLIC_API_BASELINE = (
    "Coord",
    "Facet",
    "Layer",
    "aes",
    "after_stat",
    "annotate",
    "coord_cartesian",
    "coord_fixed",
    "coord_flip",
    "coord_polar",
    "coord_sf",
    "data",
    "dup_axis",
    "element_line",
    "element_rect",
    "element_text",
    "facet_grid",
    "facet_wrap",
    "geom_abline",
    "geom_acf",
    "geom_alluvium",
    "geom_area",
    "geom_bar",
    "geom_bar_pattern",
    "geom_beeswarm",
    "geom_bin2d",
    "geom_bin_2d",
    "geom_boxplot",
    "geom_candlestick",
    "geom_col",
    "geom_col_pattern",
    "geom_contour",
    "geom_contour_filled",
    "geom_count",
    "geom_crossbar",
    "geom_density",
    "geom_density2d",
    "geom_density2d_filled",
    "geom_density_2d",
    "geom_density_2d_filled",
    "geom_density_ridges",
    "geom_dotplot",
    "geom_dotsinterval",
    "geom_edge_link",
    "geom_edgebundle",
    "geom_errorbar",
    "geom_errorbarh",
    "geom_fanchart",
    "geom_freqpoly",
    "geom_hex",
    "geom_histogram",
    "geom_hline",
    "geom_jitter",
    "geom_label",
    "geom_label_repel",
    "geom_labelpath",
    "geom_line",
    "geom_linerange",
    "geom_lines",
    "geom_map",
    "geom_mosaic",
    "geom_node_point",
    "geom_node_text",
    "geom_norm",
    "geom_ohlc",
    "geom_pacf",
    "geom_path",
    "geom_point",
    "geom_point_3d",
    "geom_pointrange",
    "geom_qq",
    "geom_qq_line",
    "geom_quasirandom",
    "geom_range",
    "geom_raster",
    "geom_rect",
    "geom_ribbon",
    "geom_rug",
    "geom_sankey",
    "geom_searoute",
    "geom_segment",
    "geom_sf",
    "geom_slabinterval",
    "geom_smooth",
    "geom_step",
    "geom_stl",
    "geom_stratum",
    "geom_surface",
    "geom_text",
    "geom_text_repel",
    "geom_textpath",
    "geom_tile",
    "geom_tile_pattern",
    "geom_violin",
    "geom_vline",
    "geom_waterfall",
    "geom_wireframe",
    "ggplot",
    "ggsave",
    "ggsize",
    "ggtitle",
    "graph_layout",
    "guide_colorbar",
    "guide_colourbar",
    "guide_legend",
    "guides",
    "label_both",
    "label_value",
    "labs",
    "layer",
    "lims",
    "map_data",
    "new_scale_color",
    "new_scale_colour",
    "new_scale_fill",
    "position_beeswarm",
    "position_dodge",
    "position_dodge2",
    "position_fill",
    "position_identity",
    "position_jitter",
    "position_jitterdodge",
    "position_nudge",
    "position_quasirandom",
    "position_stack",
    "scale_alpha",
    "scale_alpha_continuous",
    "scale_alpha_discrete",
    "scale_alpha_identity",
    "scale_alpha_manual",
    "scale_color_binned",
    "scale_color_brewer",
    "scale_color_gradient",
    "scale_color_identity",
    "scale_color_manual",
    "scale_color_viridis_d",
    "scale_colour_binned",
    "scale_colour_brewer",
    "scale_colour_gradient",
    "scale_colour_identity",
    "scale_colour_manual",
    "scale_colour_viridis_d",
    "scale_fill_binned",
    "scale_fill_brewer",
    "scale_fill_gradient",
    "scale_fill_identity",
    "scale_fill_manual",
    "scale_fill_viridis_c",
    "scale_fill_viridis_d",
    "scale_linetype_discrete",
    "scale_linetype_identity",
    "scale_linetype_manual",
    "scale_pattern_manual",
    "scale_shape_identity",
    "scale_shape_manual",
    "scale_size",
    "scale_size_identity",
    "scale_x_continuous",
    "scale_x_date",
    "scale_x_datetime",
    "scale_x_discrete",
    "scale_x_log10",
    "scale_x_rangeselector",
    "scale_x_rangeslider",
    "scale_x_reverse",
    "scale_x_sqrt",
    "scale_y_continuous",
    "scale_y_discrete",
    "scale_y_log10",
    "scale_y_reverse",
    "scale_y_sqrt",
    "sec_axis",
    "stat_alluvium",
    "stat_bin",
    "stat_bin2d",
    "stat_bin_2d",
    "stat_bin_hex",
    "stat_bindot",
    "stat_contour",
    "stat_contour_filled",
    "stat_count",
    "stat_density",
    "stat_density2d",
    "stat_density_2d",
    "stat_density_2d_filled",
    "stat_dotsinterval",
    "stat_ecdf",
    "stat_ellipse",
    "stat_fanchart",
    "stat_function",
    "stat_halfeye",
    "stat_identity",
    "stat_mosaic",
    "stat_qq",
    "stat_qq_line",
    "stat_quantile",
    "stat_sf",
    "stat_smooth",
    "stat_stl",
    "stat_sum",
    "stat_summary",
    "stat_summary_2d",
    "stat_summary_bin",
    "theme",
    "theme_bbc",
    "theme_classic",
    "theme_custom",
    "theme_dark",
    "theme_default",
    "theme_ggplot2",
    "theme_minimal",
    "theme_nytimes",
    "transition_reveal",
    "transition_states",
    "transition_time",
    "xlim",
    "ylim",
)


KNOWN_GGPLOT2_GAPS = (
    "annotation_borders",
    "annotation_custom",
    "annotation_logticks",
    "annotation_map",
    "annotation_raster",
    "as_labeller",
    "autoplot",
    "borders",
    "coord_map",
    "coord_quickmap",
    "coord_radial",
    "coord_trans",
    "element_blank",
    "element_geom",
    "element_point",
    "element_polygon",
    "facet_null",
    "fortify",
    "geom_blank",
    "geom_curve",
    "geom_function",
    "geom_polygon",
    "geom_quantile",
    "geom_sf_label",
    "geom_sf_text",
    "geom_spoke",
    "get_layer_data",
    "ggplotGrob",
    "ggplot_build",
    "ggplot_gtable",
    "guide_axis",
    "guide_axis_logticks",
    "guide_axis_stack",
    "guide_bins",
    "guide_colorsteps",
    "guide_coloursteps",
    "guide_custom",
    "guide_none",
    "is_ggplot",
    "label_bquote",
    "label_context",
    "label_parsed",
    "label_wrap_gen",
    "labeller",
    "last_plot",
    "layer_data",
    "margin",
    "margin_part",
    "qplot",
    "quickplot",
    "rel",
    "scale_alpha_binned",
    "scale_color_continuous",
    "scale_color_discrete",
    "scale_color_distiller",
    "scale_color_fermenter",
    "scale_color_gradient2",
    "scale_color_gradientn",
    "scale_color_grey",
    "scale_color_hue",
    "scale_color_steps",
    "scale_color_steps2",
    "scale_color_stepsn",
    "scale_color_viridis_b",
    "scale_color_viridis_c",
    "scale_colour_continuous",
    "scale_colour_discrete",
    "scale_colour_distiller",
    "scale_colour_fermenter",
    "scale_colour_gradient2",
    "scale_colour_gradientn",
    "scale_colour_grey",
    "scale_colour_hue",
    "scale_colour_steps",
    "scale_colour_steps2",
    "scale_colour_stepsn",
    "scale_colour_viridis_b",
    "scale_colour_viridis_c",
    "scale_continuous_identity",
    "scale_discrete_identity",
    "scale_discrete_manual",
    "scale_fill_continuous",
    "scale_fill_discrete",
    "scale_fill_distiller",
    "scale_fill_fermenter",
    "scale_fill_gradient2",
    "scale_fill_gradientn",
    "scale_fill_grey",
    "scale_fill_hue",
    "scale_fill_steps",
    "scale_fill_steps2",
    "scale_fill_stepsn",
    "scale_fill_viridis_b",
    "scale_linetype",
    "scale_linetype_binned",
    "scale_linewidth",
    "scale_linewidth_binned",
    "scale_linewidth_continuous",
    "scale_linewidth_discrete",
    "scale_linewidth_identity",
    "scale_linewidth_manual",
    "scale_radius",
    "scale_shape",
    "scale_shape_binned",
    "scale_shape_discrete",
    "scale_size_area",
    "scale_size_binned",
    "scale_size_binned_area",
    "scale_size_continuous",
    "scale_size_discrete",
    "scale_size_manual",
    "scale_size_ordinal",
    "scale_x_binned",
    "scale_x_log2",
    "scale_x_time",
    "scale_y_binned",
    "scale_y_date",
    "scale_y_datetime",
    "scale_y_log2",
    "scale_y_time",
    "stat_align",
    "stat_summary_hex",
    "stat_unique",
    "stat_ydensity",
    "theme_bw",
    "theme_get",
    "theme_gray",
    "theme_grey",
    "theme_light",
    "theme_linedraw",
    "theme_replace",
    "theme_set",
    "theme_test",
    "theme_update",
    "theme_void",
    "update_geom_defaults",
    "update_stat_defaults",
    "vars",
)


DIRECT_ALIAS_PAIRS = (
    ("geom_bin_2d", "geom_bin2d"),
    ("geom_density2d", "geom_density_2d"),
    ("geom_density2d_filled", "geom_density_2d_filled"),
    ("guide_colourbar", "guide_colorbar"),
    ("scale_colour_manual", "scale_color_manual"),
    ("scale_colour_gradient", "scale_color_gradient"),
    ("scale_colour_brewer", "scale_color_brewer"),
    ("stat_bin_2d", "stat_bin2d"),
    ("stat_density2d", "stat_density_2d"),
)


COMPATIBLE_ALIAS_CASES = (
    ("new_scale_colour", "new_scale_color", {}, ("aesthetic",)),
    (
        "scale_colour_viridis_d",
        "scale_color_viridis_d",
        {"direction": -1, "name": "group"},
        ("aesthetic", "palette", "option", "name"),
    ),
    (
        "scale_colour_identity",
        "scale_color_identity",
        {"guide": "legend", "name": "group"},
        ("aesthetic", "guide", "name"),
    ),
    (
        "scale_colour_binned",
        "scale_color_binned",
        {"low": "#000000", "high": "#ffffff", "n_breaks": 4, "name": "group"},
        ("aesthetic", "low", "high", "n_breaks", "name", "guide"),
    ),
)


HIGH_USE_SIGNATURE_PARAMS = (
    ("geom_histogram", ("bins", "binwidth", "boundary", "center")),
    ("geom_density", ("bw", "adjust", "kernel", "n", "trim")),
    ("geom_boxplot", ("outlier_colour", "notch", "varwidth", "coef", "width")),
    ("stat_bin", ("bins", "binwidth", "breaks", "closed", "pad", "na_rm")),
    ("stat_density", ("bw", "adjust", "kernel", "n", "trim", "na_rm")),
    ("stat_smooth", ("method", "span", "se", "level", "degree")),
    (
        "scale_x_continuous",
        ("limits", "breaks", "labels", "expand", "trans", "sec_axis"),
    ),
    ("facet_wrap", ("ncol", "nrow", "scales", "dir", "labeller", "drop")),
    ("facet_grid", ("rows", "cols", "scales", "space", "labeller", "margins")),
    ("guide_legend", ("title", "direction", "nrow", "ncol", "reverse")),
    ("guide_colorbar", ("title", "direction", "barwidth", "barheight", "reverse")),
    ("coord_cartesian", ("xlim", "ylim", "expand", "clip")),
)


CONSTRUCTOR_SMOKE_CASES = (
    ("geom_point", {"na_rm": True, "show_legend": False, "colour": "red"}),
    ("geom_point", {"na.rm": True, "show.legend": False}),
    ("geom_line", {"linewidth": 2, "linetype": "dash", "lineend": "round"}),
    ("geom_bar", {"stat": "identity", "position": "dodge", "width": 0.5}),
    ("geom_col", {"position": "stack", "width": 0.6}),
    ("geom_histogram", {"bins": 8, "binwidth": 0.5, "boundary": 0}),
    ("geom_density", {"bw": "nrd0", "adjust": 1.2, "kernel": "gaussian", "trim": True}),
    ("geom_boxplot", {"outlier_colour": "red", "notch": True, "varwidth": True}),
    ("geom_smooth", {"method": "lm", "se": False, "level": 0.9}),
    ("stat_bin", {"bins": 8, "binwidth": 0.5, "closed": "left", "pad": True}),
    ("stat_density", {"bw": "nrd0", "adjust": 1.1, "trim": True, "na_rm": True}),
    ("stat_smooth", {"method": "lm", "se": False, "level": 0.9}),
    ("scale_x_continuous", {"limits": (0, 10), "breaks": [0, 5, 10], "labels": ["a", "b", "c"]}),
    ("scale_color_manual", {"values": {"A": "red"}, "name": "group", "breaks": ["A"], "labels": ["Alpha"]}),
    ("scale_colour_manual", {"values": {"A": "red"}, "name": "group", "breaks": ["A"], "labels": ["Alpha"]}),
    ("facet_wrap", {"facet_var": "group", "ncol": 2, "scales": "free_x", "drop": False}),
    ("facet_grid", {"rows": "row", "cols": "col", "scales": "free", "margins": True}),
    ("guide_legend", {"title": "Group", "direction": "horizontal", "reverse": True}),
    ("guide_colorbar", {"title": "Value", "direction": "horizontal", "reverse": True}),
    ("coord_cartesian", {"xlim": (0, 1), "ylim": (0, 2), "expand": False, "clip": "off"}),
    ("theme", {"legend_position": "bottom", "axis_title": {"size": 12}}),
)


def _missing_exports(expected, actual):
    return tuple(name for name in expected if name not in actual)


def _unexpected_implemented_gaps(gaps, exports):
    return tuple(name for name in gaps if name in exports)


def _state(obj, attrs):
    return tuple((attr, getattr(obj, attr)) for attr in attrs)


def test_manifest_constants_are_unique_and_stable():
    assert PUBLIC_API_BASELINE == tuple(sorted(PUBLIC_API_BASELINE))
    assert len(PUBLIC_API_BASELINE) == len(set(PUBLIC_API_BASELINE))
    assert KNOWN_GGPLOT2_GAPS == tuple(sorted(KNOWN_GGPLOT2_GAPS))
    assert len(KNOWN_GGPLOT2_GAPS) == len(set(KNOWN_GGPLOT2_GAPS))
    assert not set(PUBLIC_API_BASELINE).intersection(KNOWN_GGPLOT2_GAPS)


def test_public_api_baseline_is_still_available():
    current_exports = set(ggplotly.__all__)
    missing_exports = _missing_exports(PUBLIC_API_BASELINE, current_exports)
    missing_attributes = tuple(
        name for name in PUBLIC_API_BASELINE if not hasattr(ggplotly, name)
    )

    assert not missing_exports, f"Public exports were removed: {missing_exports}"
    assert not missing_attributes, f"Exported names missing as attributes: {missing_attributes}"


def test_known_ggplot2_gaps_remain_explicit_until_implemented():
    implemented = _unexpected_implemented_gaps(KNOWN_GGPLOT2_GAPS, set(ggplotly.__all__))

    assert not implemented, (
        "These ggplot2 gaps now exist in the public API. Move them out of "
        f"KNOWN_GGPLOT2_GAPS and into the supported API manifest: {implemented}"
    )


@pytest.mark.parametrize(("alias_name", "canonical_name"), DIRECT_ALIAS_PAIRS)
def test_direct_aliases_resolve_to_same_object(alias_name, canonical_name):
    assert getattr(ggplotly, alias_name) is getattr(ggplotly, canonical_name)


@pytest.mark.parametrize(
    ("alias_name", "canonical_name", "kwargs", "state_attrs"),
    COMPATIBLE_ALIAS_CASES,
)
def test_compatible_aliases_construct_equivalent_specs(
    alias_name,
    canonical_name,
    kwargs,
    state_attrs,
):
    alias_constructor = getattr(ggplotly, alias_name)
    canonical_constructor = getattr(ggplotly, canonical_name)

    alias_instance = alias_constructor(**kwargs)
    canonical_instance = canonical_constructor(**kwargs)

    assert isinstance(alias_instance, canonical_instance.__class__)
    assert _state(alias_instance, state_attrs) == _state(canonical_instance, state_attrs)


@pytest.mark.parametrize(("name", "expected_params"), HIGH_USE_SIGNATURE_PARAMS)
def test_high_use_signatures_expose_ggplot2_style_parameters(name, expected_params):
    signature_params = inspect.signature(getattr(ggplotly, name)).parameters
    missing = tuple(param for param in expected_params if param not in signature_params)

    assert not missing, f"{name} is missing ggplot2-style parameters: {missing}"


@pytest.mark.parametrize(("name", "kwargs"), CONSTRUCTOR_SMOKE_CASES)
def test_high_use_constructors_accept_ggplot2_style_arguments(name, kwargs):
    constructor = getattr(ggplotly, name)

    assert constructor(**kwargs) is not None


def test_geom_common_aliases_are_normalized_to_canonical_params():
    geom = ggplotly.geom_point(
        **{
            "na.rm": True,
            "show.legend": False,
            "colour": "red",
            "linewidth": 3,
        }
    )

    assert geom.params["na_rm"] is True
    assert geom.params["show_legend"] is False
    assert geom.params["showlegend"] is False
    assert geom.params["color"] == "red"
    assert geom.params["size"] == 3


def test_color_takes_precedence_over_colour_for_geoms():
    geom = ggplotly.geom_point(color="blue", colour="red")

    assert geom.params["color"] == "blue"
