from typing import Dict, List, Tuple
import matplotlib.text as mtext


class LegendTitleOptions(object):
    def __init__(self,  text_props=None, sub_titles: Dict[int, str]=None):
        self.text_props = text_props or { 'fontsize': 11 }
        self._sub_titles = sub_titles
        super(LegendTitleOptions, self).__init__()

    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        title = mtext.Text(x0, y0, orig_handle, usetex=False, **self.text_props)
        handlebox.add_artist(title)
        return title

    def add_subtitle(self, position_idx: int, text: str):
        assert position_idx > 0
        self._sub_titles[position_idx] = text

    def get_sub_titles(self) -> List[Tuple[int, str]]:
        if self._sub_titles is None:
            return []

        sub_title_tuples = list(self._sub_titles.items())
        sub_title_tuples.sort(key=lambda x: x[0])
        return sub_title_tuples
