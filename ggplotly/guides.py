# guides.py


# # guides.py
# class Labs:
#     def __init__(self, **kwargs):
#         """
#         Initialize plot labels.

#         Parameters:
#             **kwargs: Label parameters (e.g., title, x, y).
#         """
#         self.labels = kwargs

#     def apply(self, fig):
#         """
#         Apply labels to the figure.

#         Parameters:
#             fig (Figure): Plotly figure object.
#         """
#         fig.update_layout(**self.labels)


class Labs:
    """
    Class to handle plot labels, such as title, subtitle, x-axis label, y-axis label, color legend title, and caption.
    """

    def __init__(
        self,
        title=None,
        subtitle=None,
        x=None,
        y=None,
        color=None,
        fill=None,
        caption=None,
    ):
        self.title = title
        self.subtitle = subtitle
        self.x = x
        self.y = y
        self.color = color  # Legend title for color aesthetic
        self.fill = fill  # Legend title for fill aesthetic
        self.caption = caption

    def apply(self, fig):
        """
        Apply the labels to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        layout_updates = {}

        if self.title is not None:
            # Combine title and subtitle into a single title object using HTML tags
            if self.subtitle is not None:
                title_text = f"{self.title}<br><sup>{self.subtitle}</sup>"
            else:
                title_text = self.title

            layout_updates["title"] = dict(
                text=title_text,
                x=0.5,  # Center the title
                xanchor="center",
                yanchor="top",
                font=dict(size=24),
            )

        if self.color is not None:
            layout_updates["legend_title_text"] = self.color

        if self.fill is not None:
            layout_updates["legend_title_text"] = self.fill

        if self.caption is not None:
            # Add caption as an annotation
            fig.add_annotation(
                text=self.caption,
                xref="paper",
                yref="paper",
                x=1,
                y=0,
                showarrow=False,
                xanchor="right",
                yanchor="bottom",
                font=dict(size=12),
            )

        # Apply the layout updates to the figure
        fig.update_layout(**layout_updates)

        # Update axis titles for all subplots (handles faceted plots)
        if self.x is not None:
            fig.update_xaxes(title_text=self.x)
        if self.y is not None:
            fig.update_yaxes(title_text=self.y)


# guides.py continued
def labs(**kwargs):
    """
    Create a Labs object to modify plot labels.

    Parameters:
        **kwargs: Label parameters (e.g., title, x, y).

    Returns:
        Labs: An instance of the Labs class.
    """
    return Labs(**kwargs)
