from matplotlib.figure import Figure


class FigureOptions:
    def __init__(
        self,
        title: str = None,
        title_padding: float = None,
        save_path: str = None,
        filename: str = None,
        tight_layout: bool = True,
        hide_axis: bool = False,
        show_plot: bool = False,
        seaborn_style: str = 'ticks',
        figure: Figure = None,
        super_title: str = None,
        hide_y_labels: bool = False,
        hide_x_labels: bool = False):

        self._title = title
        self._title_padding = title_padding
        self._save_path = save_path
        self._filename = filename
        self._tight_layout = tight_layout
        self._hide_axis = hide_axis
        self._show_plot = show_plot
        self._seaborn_style = seaborn_style
        self._figure = figure
        self._super_title = super_title
        self._hide_y_labels = hide_y_labels
        self._hide_x_labels = hide_x_labels

    @property
    def title(self) -> str:
        return self._title

    @property
    def title_padding(self) -> str:
        return self._title_padding

    @property
    def save_path(self) -> str:
        return self._save_path

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def tight_layout(self) -> bool:
        return self._tight_layout

    @property
    def hide_axis(self) -> bool:
        return self._hide_axis

    @property
    def show_plot(self) -> bool:
        return self._show_plot

    @property
    def seaborn_style(self) -> str:
        return self._seaborn_style

    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def super_title(self) -> str:
        return self._super_title

    @property
    def hide_y_labels(self) -> bool:
        return self._hide_y_labels

    @property
    def hide_x_labels(self) -> bool:
        return self._hide_x_labels