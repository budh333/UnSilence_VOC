from matplotlib.figure import Figure
import pandas as pd
from utils.math_utils import get_square, is_square
from entities.plot.histogram_options import HistogramOptions
from entities.plot.label_options import LabelOptions
from entities.plot.figure_options import FigureOptions
from enums.plot_legend_position import PlotLegendPosition
from entities.plot.legend_options import LegendOptions
from entities.plot.plot_options import PlotOptions
import sys
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
from services.data_service import DataService
from typing import Dict, List
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import cm, plot
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from collections import Counter


plt.rcParams["figure.figsize"] = (15, 10)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'cm'


class PlotService:
    def __init__(
            self,
            data_service: DataService):
        sns.set()
        sns.set(font_scale=2)  # crazy big
        # sns.set_style("ticks")

        self._data_service = data_service

    def create_plot(self, plot_options: PlotOptions = None) -> Axes:
        if plot_options is not None and plot_options.ax is not None:
            return plot_options.ax

        if plot_options is not None and plot_options.figure_options is not None:
            sns.set_style(plot_options.figure_options.seaborn_style)
        else:
            sns.set_style('ticks')

        fig = plt.figure()

        fig.canvas.start_event_loop(sys.float_info.min) # workaround for Exception in Tkinter callback

        ax = fig.add_subplot(1, 1, 1)
        return ax

    def create_plots(self, plots_count: int, share_x_coords: bool = False, share_y_coords: bool = False) -> List[Axes]:
        sns.set_style('ticks')

        rows_count = plots_count
        columns_count = 1
        if is_square(plots_count):
            square_count = get_square(plots_count)
            rows_count = square_count
            columns_count = square_count

        fig, all_axs = plt.subplots(rows_count, columns_count, sharex=share_x_coords, sharey=share_y_coords)
        axs = [x for col_axs in all_axs for x in col_axs]

        return fig, axs

    def plot_histogram(
            self,
            values: list,
            plot_options: PlotOptions,
            number_of_bins: int = None):
        ax = self.create_plot(plot_options)

        if number_of_bins is None:
            number_of_bins = len(set(values))

        if plot_options.xlim is None:
            start_x, end_x = min(values), max(values)
        else:
            start_x, end_x = plot_options.xlim

        distance_bin = (end_x - start_x) / number_of_bins

        bins = np.arange(start_x, end_x, distance_bin)

        ax.hist(values, bins=bins, edgecolor='none')

        self._add_properties(ax, plot_options)
        return ax

    def autolabel_heights(self, ax, rects, rotation: int = 0):
        """Attach a text label above each bar in *rects*, displaying its height."""
        y_offset = 3 if rotation == 0 else 10
        for rect in rects:
            height = rect.get_height()
            if height == 0:
                continue

            ax.annotate(
                '{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, y_offset),  # 3 points vertical offset
                textcoords="offset points",
                ha='center',
                va='bottom',
                rotation=rotation)

    def plot_counters_histogram(
            self,
            counter_labels: List[str],
            counters: List[Counter],
            plot_options: PlotOptions,
            histogram_options: HistogramOptions,
            counter_colors: List[str] = None):

        ax = self.create_plot(plot_options)

        unique_labels = list(
            sorted(set([label for x in counters for label in x.keys()])))

        values = []
        for counter in counters:
            values.append([(counter[label] if label in counter.keys() else 0)
                           for label in unique_labels])

        total_width = 1 - histogram_options.bars_padding  # the width of the bars
        dim = len(counters)
        dimw = total_width / dim

        x = np.arange(len(unique_labels))  # the label locations

        if counter_colors is None:
            counter_colors = cm.rainbow(np.linspace(0, 1, dim))

        rects = []
        for i, counter_values in enumerate(values):
            rects.append(
                ax.bar(x + (i * dimw), counter_values, dimw, label=counter_labels[i], color=counter_colors[i]))

        xticks = x + (total_width - dimw) / 2
        xtick_labels = unique_labels
        if plot_options.xticks_count is not None:

            indices = np.round(np.linspace(
                0, len(xticks) - 1, plot_options.xticks_count)).astype(int)
            leftover_ticks = [xticks[idx] for idx in indices]
            xtick_labels = [unique_labels[idx] for idx in indices]

            xticks = leftover_ticks

        ax.set_xticks(xticks)
        labels = ax.set_xticklabels(
            xtick_labels, rotation=plot_options.x_labels_rotation_angle)

        if plot_options.space_x_labels_vertically:
            for i, label in enumerate(labels):
                label.set_y(label.get_position()[1] - (i % 2) * 0.075)

        if histogram_options.plot_values_above_bars:
            for rect in rects:
                self.autolabel_heights(
                    ax, rect, rotation=histogram_options.values_above_bars_rotation)

        x1, x2, y1, y2 = ax.axis()
        ax.axis((x1, x2, y1, y2 + 5))

        self._add_properties(ax, plot_options)

        return ax

    def plot_distribution(
            self,
            counts,
            plot_options: PlotOptions):
        ax = self.create_plot(plot_options)

        counts_list = counts
        if isinstance(counts, dict):
            for k, v in counts.items():
                for _ in range(v):
                    counts_list.append(k)

        ax = sns.kdeplot(
            data=counts_list,
            color=plot_options.color,
            fill=plot_options.fill,
            linestyle=plot_options.linestyle.value,
            label=plot_options.label,
            legend=plot_options.legend_options.show_legend,
            linewidth=plot_options.line_width,
            alpha=plot_options.alpha,
            ax=ax)

        self._add_properties(ax, plot_options)

        return ax

    def plot_line_variance(
            self,
            pd_dataframe: pd.DataFrame,
            x: str,
            y: str,
            plot_options: PlotOptions):

        ax = self.create_plot(plot_options)

        ax = sns.lineplot(
            data=pd_dataframe,
            x=x,
            y=y,
            label=plot_options.label,
            ax=ax,
            markersize=14,
            color=plot_options.color,
            linestyle=plot_options.linestyle.value,
            ci=95)

        self._add_properties(ax, plot_options)

        return ax

    def plot_scatter(
            self,
            x_values: list,
            y_values: list,
            plot_options: PlotOptions):
        ax = self.create_plot(plot_options)
        ax.scatter(x_values, y_values, color=plot_options.color)
        self._add_properties(ax, plot_options)
        return ax

    def plot_overlapping_bars(
            self,
            numbers_per_type: List[List[int]],
            bar_titles: List[str],
            plot_options: PlotOptions,
            colors: List[str] = None):

        ax = self.create_plot(plot_options)

        unique_numbers = set([item for v in numbers_per_type for item in v])
        counters_per_type = {
            bar_titles[i]: Counter(v)
            for i, v in enumerate(numbers_per_type)
        }

        normalized_counters_per_type = {
            type_name: Counter({
                n: (float(v)/sum(unnormalized_counter.values())) * 100
                for n, v in unnormalized_counter.items()
            })
            for type_name, unnormalized_counter in counters_per_type.items()
        }

        argmaxes = {}
        for i, number in enumerate(unique_numbers):
            occs = np.array([x[number]
                             for _, x in normalized_counters_per_type.items()])
            arg_sort = np.argsort(np.argsort(occs, kind='heapsort'))
            sorted_occs = sorted(occs)

            a = np.zeros(len(occs))
            for i, index in enumerate(arg_sort):
                if index == 0:
                    a[i] = 0
                else:
                    a[i] = sorted_occs[index-1]

            argmaxes[number] = a

        for i, counter_values in enumerate(normalized_counters_per_type.values()):
            x = list(sorted(counter_values.keys()))

            y = np.array([counter_values[key] for key in x])
            p = np.array([argmaxes[a][i] for a in x])
            norm_y = y - p

            ax.bar(x, norm_y, width=x[1]-x[0], color=colors[i], bottom=p)

        self._add_properties(ax, plot_options)

        return ax

    def plot_labels(
            self,
            labels_options: List[LabelOptions],
            plot_options: PlotOptions):
        ax = self.create_plot(plot_options)

        for label_options in labels_options:
            label_color = label_options.text_color if label_options.text_color is not None else plot_options.color

            ax.annotate(
                label_options.text,
                xy=(label_options.x, label_options.y),
                xytext=(0, 0),
                textcoords='offset points',
                color=label_color,
                weight=label_options.font_weight.value,
                fontsize=label_options.font_size)

        self._add_properties(ax, plot_options)
        return ax

    def plot_arrow(
            self,
            x: float,
            y: float,
            dx: float,
            dy: float,
            plot_options: PlotOptions):
        ax = self.create_plot(plot_options)

        ax.annotate("", xy=(x+dx, y+dy), xytext=(x, y),
                    arrowprops=dict(arrowstyle="-|>", color=plot_options.color),
                    bbox=dict(pad=7, facecolor="none", edgecolor="none"))

        self._add_properties(ax, plot_options)
        return ax

    def plot_confusion_matrix(
            self,
            true_values: list,
            predicted_values: list,
            plot_options: PlotOptions,
            labels: List[str] = None,
            normalize: bool = False):
        ax = self.create_plot(plot_options)

        cm = confusion_matrix(true_values, predicted_values, labels)

        vmin = cm.min()
        vmax = cm.max()
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            vmin = 0
            vmax = 1

        sns_heatmap = sns.heatmap(
            cm,
            ax=ax,
            vmin=vmin,
            vmax=vmax,
            cmap='RdYlGn_r',
            square=True)

        ax.set_xlabel('Predicted values')  # , labelpad=20)
        ax.set_ylabel('True values')

        if labels is not None:
            ax.set_ylim(0, len(labels) + 0.5)
            ax.set_ylim(0, len(labels) + 0.5)

            sns_heatmap.set_yticklabels(labels, rotation=0)
            sns_heatmap.set_xticklabels(
                labels, rotation=45, horizontalalignment='right')

        self._add_properties(ax, plot_options)
        return ax

    def plot_heatmap(
            self,
            values: np.array,
            plot_options: PlotOptions,
            labels: List[str] = None,
            vmin: float = None,
            vmax: float = None,
            show_colorbar: bool = True):
        ax = self.create_plot(plot_options)

        if vmin is None:
            vmin = np.min(values)

        if vmax is None:
            vmax = np.max(values)

        sns_heatmap = sns.heatmap(
            values,
            ax=ax,
            vmin=vmin,
            vmax=vmax,
            cmap='Greens',
            square=True,
            cbar=show_colorbar)
        if labels is not None:
            ax.set_ylim(0, len(labels) + 0.5)
            ax.set_ylim(0, len(labels) + 0.5)

            sns_heatmap.set_yticklabels(labels, rotation=0)
            sns_heatmap.set_xticklabels(
                labels, rotation=45, horizontalalignment='right')

        self._add_properties(ax, plot_options)
        return ax

    def plot_lines(
        self,
        x_values: List[float],
        y_values: List[List[float]],
        plot_options: PlotOptions,
        labels: List[str] = None):
        ax = self.create_plot(plot_options)

        if labels is not None:
            for value_list, label in zip(y_values, labels):
                ax.plot(x_values, value_list, label=label)
        else:
            label = plot_options.label
            ax.plot(x_values, y_values, label=label)

        self._add_properties(ax, plot_options)
        return ax

    def show_plot(self):
        plt.show()

    def set_plot_properties(
            self,
            ax: Axes,
            figure_options: FigureOptions,
            legend_options: LegendOptions = None):

        if figure_options.tight_layout:
            plt.tight_layout()

        if figure_options.hide_axis:
            ax.axis('off')

        if figure_options.hide_x_labels:
            ax.axes.xaxis.set_visible(False)

        if figure_options.hide_y_labels:
            ax.axes.yaxis.set_visible(False)

        if legend_options is not None:
            self.show_legend(ax, legend_options)

        if figure_options.super_title is not None and figure_options.figure is not None:
            figure_options.figure.suptitle(figure_options.super_title)

        if figure_options.title is not None:
            ax.set_title(figure_options.title, pad=figure_options.title_padding,
                         fontdict={'fontweight': 'bold'})


    def plot_confidence_lines(
        self,
        x_values: List[float],
        y_values: List[List[float]],
        plot_options: PlotOptions,
        labels: List[str] = None):
        ax = self.create_plot(plot_options)

        # if labels is not None:
        #     for value_list, label in zip(y_values, labels):
        #         ax.plot(x_values, value_list, label=label)
        # else:
        # label = plot_options.label
        # ax.plot(x_values, y_values, label=label)
        sns.lineplot(x_values, y_values)

        self._add_properties(ax, plot_options)
        return ax


    def show_legend(
            self,
            ax: Axes,
            legend_options: LegendOptions):

        if legend_options is None or not legend_options.show_legend:
            return

        bbox_to_anchor = None
        legend_location = None
        lg_obj = None

        if legend_options.legend_position == PlotLegendPosition.Outside:
            bbox_to_anchor = (1.04, 1)
            legend_location = "upper left"
        elif (legend_options.legend_position != PlotLegendPosition.Outside and
              legend_options.legend_position != PlotLegendPosition.Automatic):
            legend_location = legend_options.legend_position.value

        if legend_options.legend_colors is not None and len(legend_options.legend_colors) > 0:
            legend_lines = self._create_legend_lines(
                legend_options.legend_colors)
            if legend_options.legend_labels is not None and len(legend_options.legend_labels) > 0:
                lg_obj = ax.legend(legend_lines, legend_options.legend_labels,
                          bbox_to_anchor=bbox_to_anchor, loc=legend_location)
            else:
                lg_obj = ax.legend(legend_lines, bbox_to_anchor=bbox_to_anchor,
                          loc=legend_location)
        elif legend_options.legend_title_options is not None:
            sub_title_pairs = legend_options.legend_title_options.get_sub_titles()
            if sub_title_pairs is not None:
                handles, labels = ax.get_legend_handles_labels()
                for position_id, text in sub_title_pairs:
                    handles.insert(position_id, text)
                    labels.insert(position_id, '')

                lg_obj = ax.legend(handles, labels, handler_map={str: legend_options.legend_title_options},handlelength=10, markerscale=100)
        else:
            lg_obj = ax.legend()

        if lg_obj is not None and legend_options.marker_scale is not None:
            leg_lines = lg_obj.get_lines()
            plt.setp(leg_lines, linewidth=legend_options.marker_scale)

    def save_plot(self, save_path: str, filename: str, figure: Figure = None):
        self._data_service.save_figure(save_path, filename, fig=figure)

    def _create_legend_lines(
            self,
            legend_colors: List[str]) -> List[Artist]:
        lines = [Line2D([0], [0], color=color, lw=4)
                 for color in legend_colors]
        return lines

    def _add_properties(
            self,
            ax: Axes,
            plot_options: PlotOptions):

        self.show_legend(ax, plot_options.legend_options)
        self._set_labels(ax, plot_options)
        self._set_plot_limits(ax, plot_options)
        self.set_plot_properties(ax, plot_options.figure_options)

        if plot_options.figure_options is None:
            return

        if plot_options.figure_options.save_path is not None and plot_options.figure_options.filename is not None:
            self.save_plot(plot_options.figure_options.save_path,
                           plot_options.figure_options.filename)
        elif plot_options.figure_options.show_plot:
            self.show_plot()

        if plot_options.clear_figure:
            plt.clf()

    def _set_labels(self, ax: Axes, plot_options: PlotOptions):
        if plot_options.ylabel_options.text is not None:
            ax.set_ylabel(
                plot_options.ylabel_options.text,
                fontweight=plot_options.ylabel_options.font_weight.value)

        if plot_options.xlabel_options.text is not None:
            ax.set_xlabel(
                plot_options.xlabel_options.text,
                fontweight=plot_options.xlabel_options.font_weight.value)

    def _set_plot_limits(self, ax: Axes, plot_options: PlotOptions):
        if plot_options.ylim is not None:
            ax.set_ylim(plot_options.ylim[0], plot_options.ylim[1])

        if plot_options.xlim is not None:
            ax.set_xlim(plot_options.xlim[0], plot_options.xlim[1])
