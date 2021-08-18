from matplotlib.legend_handler import HandlerBase

from matplotlib.lines import Line2D
import matplotlib.text as mtext

class GroupingHandler(HandlerBase):
    def create_artists(self, legend, orig_handle, x0, y0, width, height, fontsize, trans):

        title = mtext.Text(x0,y0, text=orig_handle.group_name, fontsize=fontsize)
        fast_line = Line2D([130,165], [(height/2), (height/2)], linestyle='solid', color=orig_handle.color, linewidth=5)
        fast_title = mtext.Text(175,0, text='fast', fontsize=fontsize-1)
        slow_line = Line2D([220,255], [(height/2), (height/2)], linestyle='dashed', color=orig_handle.color, linewidth=5)
        slow_title = mtext.Text(265,0, text='slow', fontsize=fontsize-1)

        return [title, fast_line, fast_title, slow_line, slow_title]
