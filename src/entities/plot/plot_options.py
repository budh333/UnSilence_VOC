from entities.plot.label_options import LabelOptions
from entities.plot.legend_options import LegendOptions
from enums.font_weight import FontWeight
from entities.plot.figure_options import FigureOptions
from enums.plots.line_style import LineStyle
from typing import Tuple
from matplotlib.axes import Axes


class PlotOptions:
    def __init__(
            self,
            ax: Axes = None,
            figure_options: FigureOptions = FigureOptions(),
            legend_options: LegendOptions = LegendOptions(show_legend=True),
            ylim: float = None,
            xlim: float = None,
            color: str = None,
            linestyle: LineStyle = LineStyle.Solid,
            alpha: float = None,
            label: str = None,
            line_width: float = 1,
            fill: bool = False,
            yticks_count: int = None,
            ylabel_options: LabelOptions = LabelOptions(),
            space_y_labels_vertically: bool = False,
            xticks_count: int = None,
            xlabel_options: LabelOptions = LabelOptions(),
            space_x_labels_vertically: bool = False,
            clear_figure: bool = False):

        self._ax = ax

        self._figure_options = figure_options
        self._legend_options = legend_options

        self._ylim = ylim
        self._xlim = xlim
        self._color = color
        self._linestyle = linestyle
        self._alpha = alpha
        self._label = label
        self._line_width = line_width
        self._fill = fill

        self._yticks_count = yticks_count
        self._ylabel_options = ylabel_options
        self._space_y_labels_vertically = space_y_labels_vertically

        self._xticks_count = xticks_count
        self._xlabel_options = xlabel_options
        self._space_x_labels_vertically = space_x_labels_vertically

        self._clear_figure = clear_figure

    @property
    def ax(self) -> Axes:
        return self._ax

    @property
    def ylim(self) -> Tuple[float, float]:
        return self._ylim

    @property
    def xlim(self) -> Tuple[float, float]:
        return self._xlim

    @property
    def color(self) -> str:
        return self._color

    @property
    def linestyle(self) -> LineStyle:
        return self._linestyle

    @property
    def alpha(self) -> float:
        return self._alpha

    @property
    def label(self) -> str:
        return self._label

    @property
    def line_width(self) -> float:
        return self._line_width

    @property
    def fill(self) -> bool:
        return self._fill

    @property
    def figure_options(self) -> FigureOptions:
        return self._figure_options

    @property
    def legend_options(self) -> LegendOptions:
        return self._legend_options

    @property
    def yticks_count(self) -> int:
        return self._yticks_count

    @property
    def ylabel_options(self) -> LabelOptions:
        return self._ylabel_options

    @property
    def space_y_labels_vertically(self) -> bool:
        return self._space_y_labels_vertically

    @property
    def xticks_count(self) -> int:
        return self._xticks_count

    @property
    def xlabel_options(self) -> LabelOptions:
        return self._xlabel_options

    @property
    def space_x_labels_vertically(self) -> bool:
        return self._space_x_labels_vertically

    @property
    def clear_figure(self) -> bool:
        return self._clear_figure
