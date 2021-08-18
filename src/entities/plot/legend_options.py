from entities.plot.legend_title_options import LegendTitleOptions
from enums.plot_legend_position import PlotLegendPosition
from typing import List


class LegendOptions:
    def __init__(
            self,
            show_legend: bool,
            legend_colors: List[str] = None,
            legend_labels: List[str] = None,
            legend_position: PlotLegendPosition = PlotLegendPosition.Automatic,
            legend_title_options: LegendTitleOptions = None,
            marker_scale: int = None):
        self._show_legend = show_legend
        self._legend_colors: List[str] = legend_colors
        self._legend_labels: List[str] = legend_labels
        self._legend_position = legend_position
        self._legend_title_options = legend_title_options
        self._marker_scale = marker_scale

    @property
    def show_legend(self) -> bool:
        return self._show_legend

    @property
    def legend_colors(self) -> List[str]:
        return self._legend_colors

    @property
    def legend_labels(self) -> List[str]:
        return self._legend_labels

    @property
    def legend_position(self) -> PlotLegendPosition:
        return self._legend_position

    @property
    def legend_title_options(self) -> LegendTitleOptions:
        return self._legend_title_options

    @property
    def marker_scale(self) -> int:
        return self._marker_scale