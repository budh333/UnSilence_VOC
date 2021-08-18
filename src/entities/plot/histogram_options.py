class HistogramOptions:
    def __init__(
            self,
            bars_padding: float = 0.2,
            plot_values_above_bars: bool = False,
            values_above_bars_rotation: int = 0):

        if bars_padding >= 1 or bars_padding < 0:
            raise Exception('bars_padding must be between 0 and 1')

        self._bars_padding = bars_padding
        self._plot_values_above_bars = plot_values_above_bars
        self._values_above_bars_rotation = values_above_bars_rotation

    @property
    def bars_padding(self) -> float:
        return self._bars_padding

    @property
    def plot_values_above_bars(self) -> bool:
        return self._plot_values_above_bars

    @property
    def values_above_bars_rotation(self) -> int:
        return self._values_above_bars_rotation
