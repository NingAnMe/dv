# -*- coding: utf-8 -*-
"""
@Time    : 2018/6/29 14:33
@Author  : AnNing
"""
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

import numpy as np
from scipy import stats
import matplotlib as mpl

mpl.use("Agg")  # 必须加这个字段，否则引用 pyplot 服务器会报错，服务器上面没有 TK

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, LinearLocator
from matplotlib.font_manager import FontProperties
from matplotlib import colors
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches


def get_ds_font(font_name="OpenSans-Regular.ttf"):
    """
    载入字体
    "OpenSans-Regular.ttf"
    "simhei.ttf"
    "微软雅黑.ttf"
    """
    self_path = os.path.split(os.path.realpath(__file__))[0]
    font0 = FontProperties()
    font_path = os.path.join(self_path, "FNT", font_name)
    if os.path.isfile(font_path):
        font0.set_file(font_path)
        return font0
    return None


FONT0 = get_ds_font()
FONT1 = get_ds_font()
FONT_MONO = get_ds_font("DroidSansMono.ttf")


class PlotAx(object):
    """
    格式化 matplotlib.axis 常用方法
    """
    def __init__(self):
        self.font = FONT0  # 字体

        self.x_label_font_size = 11
        self.y_label_font_size = 11

        self.tick_font_size = 11

        self.annotate_font_size = 11
        self.annotate_font_color = '#000000'

    def format_ax(self, ax, **kwargs):
        """
        ax = ax

        font = FONT0  # 字体

        x_label = None  # X 轴标签
        y_label = None  # Y 轴标签
        x_label_font_size = 11  # X 轴标签字体
        y_label_font_size = 11  # Y 轴标签字体

        x_major_count = None  # X 轴主刻度数量
        x_minor_count = None  # Y 轴主刻度数量
        y_major_count = None  # X 轴次刻度数量
        y_minor_count = None  # Y 轴次刻度数量

        x_axis_min = None  # X 轴最小值
        x_axis_max = None  # X 轴最大值
        y_axis_min = None  # Y 轴最小值
        y_axis_max = None  # Y 轴最大值

        tick_font_size = 11  # 刻度文字字体大小

        annotate = None  # 注释
        annotate_font_size = 11  # 注释字体大小
        annotate_font_color = '#000000'

        :param ax:
        :param kwargs: (dict)
        :return:
        """
        # 设置字体
        if 'font' in kwargs:
            self.font = kwargs.get('font')

        # 设置 label
        if 'x_label' in kwargs:
            x_label = kwargs.get('x_label')
            if 'x_label_font_size' in kwargs:
                x_label_font_size = kwargs.get('x_label_font_size')
            else:
                x_label_font_size = self.x_label_font_size
            ax.set_xlabel(x_label, fontsize=x_label_font_size, fontproperties=self.font)
        if 'y_label' in kwargs:
            y_label = kwargs.get('y_label')
            if 'y_label_font_size' in kwargs:
                y_label_font_size = kwargs.get('y_label_font_size')
            else:
                y_label_font_size = self.y_label_font_size
            ax.set_ylabel(y_label, fontsize=y_label_font_size, fontproperties=self.font)

        # 设置 x y 轴的范围
        if 'x_axis_min' in kwargs and 'x_axis_max' in kwargs:
            x_axis_min = kwargs.get('x_axis_min')
            x_axis_max = kwargs.get('x_axis_max')
            ax.set_xlim(x_axis_min, x_axis_max)

            # 如果是长时间序列图，设置长时间序列x轴日期坐标
            if kwargs.get('timeseries') is not None:
                self.set_timeseries_x_locator(ax, x_axis_min, x_axis_max)

        if 'y_axis_min' in kwargs and 'y_axis_max' in kwargs:
            y_axis_min = kwargs.get('y_axis_min')
            y_axis_max = kwargs.get('y_axis_max')
            ax.set_ylim(y_axis_min, y_axis_max)

        # 设置大刻度的数量
        if 'x_major_count' in kwargs:
            x_major_count = kwargs.get('x_major_count')
            ax.xaxis.set_major_locator(LinearLocator(x_major_count))
        if 'y_major_count' in kwargs:
            y_major_count = kwargs.get('y_major_count')
            ax.yaxis.set_major_locator(LinearLocator(y_major_count))

        # 设置小刻度的数量
        if 'x_minor_count' in kwargs:
            x_minor_count = kwargs.get('x_minor_count')
            x_major_count = len(ax.xaxis.get_majorticklocs())
            ax.xaxis.set_minor_locator(LinearLocator((x_major_count - 1) * (x_minor_count + 1) + 1))
        if 'y_minor_count' in kwargs:
            y_minor_count = kwargs.get('y_minor_count')
            y_major_count = len(ax.yaxis.get_majorticklocs())
            ax.yaxis.set_minor_locator(LinearLocator((y_major_count - 1) * (y_minor_count + 1) + 1))

        # 设置图片注释文字
        if 'annotate' in kwargs:
            annotate = kwargs.get('annotate')
            if 'annotate_font_size' in kwargs:
                annotate_font_size = kwargs.get('annotate_font_size')
            else:
                annotate_font_size = self.annotate_font_size
            if 'annotate_font_color' in kwargs:
                annotate_font_color = kwargs.get('annotate_font_color')
            else:
                annotate_font_color = self.annotate_font_color
            for k in annotate:
                add_annotate(ax, annotate[k], k, fontsize=annotate_font_size,
                             color=annotate_font_color)

    @classmethod
    def plot_time_series(cls, ax, data_x, data_y, marker=None, marker_size=None,
                         marker_facecolor=None, marker_edgecolor=None, marker_edgewidth=None,
                         color=None, alpha=None, line_width=None, label=None, zorder=None):
        """
        :param ax:
        :param data_x:
        :param data_y:
        :param marker:
        :param marker_size:
        :param marker_facecolor:
        :param marker_edgecolor:
        :param marker_edgewidth:
        :param color:
        :param alpha:
        :param line_width:
        :param label:
        :param zorder:
        :return:
        """
        if marker is None:
            marker = 'o'
        if marker_size is None:
            marker_size = 6
        if marker_edgecolor is None:
            marker_edgecolor = 'b'
        if marker_edgewidth is None:
            marker_edgewidth = 0.3
        if color is None:
            color = 'b'
        if alpha is None:
            alpha = 1.0
        if label is None:
            label = 'Daily'
        if zorder is None:
            zorder = 100

        ax.plot(data_x, data_y, marker, ms=marker_size, lw=line_width, c=color,
                markerfacecolor=marker_facecolor, markeredgecolor=marker_edgecolor,
                mew=marker_edgewidth, alpha=alpha, label=label, zorder=zorder)

    @classmethod
    def plot_zero_line(cls, ax, x_axis_min=None, x_axis_max=None, line_color=None, line_width=None):
        """
        绘制 y = 0 线
        :param ax:
        :param line_color:
        :param line_width:
        :param x_axis_min:
        :param x_axis_max:
        :return:
        """
        if line_color is None:
            line_color = '#808080'
        if line_width is None:
            line_width = 1.0

        if x_axis_min is not None and x_axis_max is not None:
            ax.plot([x_axis_min, x_axis_max], [0, 0], color=line_color, linewidth=line_width)

    @classmethod
    def plot_background_fill(cls, ax, x=None, y1=None, y2=None, color=None, alpha=None,
                             zorder=None):
        """
        :param ax:
        :param x:
        :param y1:
        :param y2:
        :param color:
        :param alpha:
        :param zorder:
        :return:
        """
        if color is None:
            color = 'r'
        if alpha is None:
            alpha = 1.0
        if zorder is None:
            zorder = 100
        ax.fill_between(x, y1, y2, facecolor=color, edgecolor=color, alpha=alpha, zorder=zorder,
                        interpolate=True)

    @classmethod
    def set_timeseries_x_locator(cls, ax, xlim_min, xlim_max):
        """
        :param ax:
        :param xlim_min: datetime 数据
        :param xlim_max: datetime 数据
        :return:
        """
        day_range = (xlim_max - xlim_min).days
        if day_range <= 6:
            return
        if day_range <= 60:
            days = mdates.DayLocator(interval=(day_range / 6))
            ax.xaxis.set_major_locator(days)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        else:
            month_range = day_range / 30
            if month_range <= 12.:
                months = mdates.MonthLocator()  # every month
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
            elif month_range <= 24.:
                months = mdates.MonthLocator(interval=2)
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
            elif month_range <= 48.:
                months = mdates.MonthLocator(interval=4)
                ax.xaxis.set_major_locator(months)
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
            else:
                years = mdates.YearLocator()
                ax.xaxis.set_major_locator(years)
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

            if month_range <= 48:
                PlotAx.add_year_xaxis(ax, xlim_min, xlim_max)

    @classmethod
    def add_year_xaxis(cls, ax, xlim_min, xlim_max):
        """
        add year xaxis
        :param ax:
        :param xlim_min:
        :param xlim_max:
        :return:
        """
        if xlim_min.year == xlim_max.year:
            ax.set_xlabel(xlim_min.year, fontsize=11, fontproperties=FONT_MONO)
            return
        newax = ax.twiny()
        newax.set_frame_on(True)
        newax.grid(False)
        newax.patch.set_visible(False)
        newax.xaxis.set_ticks_position("bottom")
        newax.xaxis.set_label_position("bottom")
        newax.set_xlim(xlim_min, xlim_max)
        newax.xaxis.set_major_locator(mdates.YearLocator())
        newax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        newax.spines["bottom"].set_position(("outward", 20))
        newax.spines["bottom"].set_linewidth(0.6)

        newax.tick_params(which="both", direction="in")
        set_tick_font(newax)
        newax.xaxis.set_tick_params(length=5)


class FormatAx(object):
    """
    OCC 绘图使用，不再维护
    """
    def __init__(self, ax):
        self.ax = ax

        self.font = FONT0  # 字体

        self.x_label = None  # X 轴标签
        self.y_label = None  # Y 轴标签
        self.x_label_font_size = 11  # X 轴标签字体
        self.y_label_font_size = 11  # Y 轴标签字体

        self.x_major_count = None
        self.x_minor_count = None
        self.y_major_count = None
        self.y_minor_count = None

        self.x_axis_min = None
        self.x_axis_max = None
        self.y_axis_min = None
        self.y_axis_max = None

        self.tick_font_size = 11

        self.annotate = None
        self.annotate_font_size = 11

    def set_tick(self, font_size=None):
        if font_size:
            self.tick_font_size = font_size

    def set_x_label(self, label=None, font_size=None):
        if label:
            self.x_label = label
        if font_size:
            self.x_label_font_size = font_size

    def set_y_label(self, label=None, font_size=None):
        if label:
            self.y_label = label
        if font_size:
            self.y_label_font_size = font_size

    def set_x_major_count(self, major_count):
        self.x_major_count = major_count

    def set_y_major_count(self, major_count):
        self.y_major_count = major_count

    def set_x_minor_count(self, minor_count):
        self.x_minor_count = minor_count

    def set_y_minor_count(self, minor_count):
        self.y_minor_count = minor_count

    def set_x_axis_range(self, axis_min=None, axis_max=None):
        self.x_axis_min = axis_min
        self.x_axis_max = axis_max

    def set_y_axis_range(self, axis_min=None, axis_max=None):
        self.y_axis_min = axis_min
        self.y_axis_max = axis_max

    def set_annotate(self, annotate=None, annotate_font_size=None):
        if annotate:
            self.annotate = annotate
        if annotate_font_size:
            self.annotate_font_size = annotate_font_size

    def set_ax(self):
        """

            update by anning 20180905
            此方法不再进行维护，使用 format_ax 方法。
        :return:
        """
        # 设置 label
        if self.x_label:
            self.ax.set_xlabel(self.x_label, fontsize=self.x_label_font_size,
                               fontproperties=self.font)
        if self.y_label:
            self.ax.set_ylabel(self.y_label, fontsize=self.y_label_font_size,
                               fontproperties=self.font)
        # 设置大刻度和小刻度的数量
        if self.x_major_count is not None and self.x_axis_min is not None \
                and self.x_axis_max is not None:
            self.ax.xaxis.set_major_locator(
                MultipleLocator((self.x_axis_max - self.x_axis_min) / self.x_major_count))
        if self.y_major_count is not None and self.y_axis_min is not None \
                and self.y_axis_max is not None:
            self.ax.yaxis.set_major_locator(
                MultipleLocator((self.y_axis_max - self.y_axis_min) / self.y_major_count))
        if self.x_minor_count is not None:
            x_ticklocs = self.ax.xaxis.get_ticklocs()
            self.ax.xaxis.set_minor_locator(
                MultipleLocator((x_ticklocs[1] - x_ticklocs[0]) / self.x_minor_count))
        if self.y_minor_count is not None:
            y_ticklocs = self.ax.yaxis.get_ticklocs()
            self.ax.yaxis.set_minor_locator(
                MultipleLocator((y_ticklocs[1] - y_ticklocs[0]) / self.y_minor_count))
        # 设置刻度文字的大小
        if self.tick_font_size is not None:
            set_tick_font(self.ax, scale_size=self.tick_font_size)
        # 设置 x y 轴的范围
        if self.x_axis_min is not None and self.x_axis_max is not None:
            self.ax.set_xlim(self.x_axis_min, self.x_axis_max)
        if self.y_axis_min is not None and self.y_axis_max is not None:
            self.ax.set_ylim(self.y_axis_min, self.y_axis_max)
        # 设置图片注释文字
        if self.annotate is not None:
            for k in self.annotate:
                add_annotate(self.ax, self.annotate[k], k, fontsize=self.annotate_font_size)


class Scatter(FormatAx):
    """
    绘制相对详细图
    """
    def __init__(self, ax):
        super(Scatter, self).__init__(ax)
        self.scatter_size = 1
        self.scatter_alpha = 0.8  # 透明度
        self.scatter_marker = "o"  # 形状
        self.scatter_color = "b"  # 颜色
        self.scatter_label = 'label'  # 标签

        self.zero_line_width = 1.0
        self.zero_line_color = '#808080'

        self.background_x = None
        self.background_y1 = None
        self.background_y2 = None
        self.background_fill_color = '#f63240'
        self.background_fill_alpha = 0.1
        self.background_fill_zorder = 80

        self.plot_result = None

    def set_zero_line(self, zero_line=True, width=None, color=None):
        if zero_line is not None:
            self.zero_line = zero_line
        if width is not None:
            self.zero_line_width = width
        if color is not None:
            self.zero_line_color = color

    def set_background_fill(self, background_fill=True, x=None, y1=None, y2=None, color=None,
                      alpha=None, zorder=None):
        if background_fill is not None:
            self.background_fill = background_fill
        if x is not None:
            self.background_x = x
        if y1 is not None:
            self.background_y1 = y1
        if y2 is not None:
            self.background_y2 = y2
        if color is not None:
            self.background_fill_color = color
        if alpha is not None:
            self.background_fill_alpha = alpha
        if zorder is not None:
            self.background_fill_zorder = zorder

    def set_scatter(self, size=None, alpha=None, marker=None, color=None, label=None):
        if size is not None:
            self.scatter_size = size
        if alpha is not None:
            self.scatter_alpha = alpha
        if marker is not None:
            self.scatter_marker = marker
        if color is not None:
            self.scatter_color = color
        if label is not None:
            self.scatter_label = label

    def plot_scatter(self, data_x=None, data_y=None, kde=False):
        if not kde:
            self.ax.scatter(data_x, data_y, s=self.scatter_size, marker=self.scatter_marker,
                       c=self.scatter_color, lw=0, alpha=self.scatter_alpha)
        else:
            data_x = data_x.reshape(-1)
            data_y = data_y.reshape(-1)
            xy = np.vstack((data_x, data_y))
            kde = stats.gaussian_kde(xy)
            z = kde(xy)
            # z = z / z.sum()
            norm = colors.Normalize()
            norm.autoscale(z)
            self.plot_result = self.ax.scatter(data_x, data_y, c=z, s=self.scatter_size,
                                               marker=self.scatter_marker, lw=0,
                                               alpha=self.scatter_alpha, cmap=plt.get_cmap('jet'),
                                               norm=norm)

        self.set_ax()

    def plot_zero_line(self):
        self.ax.plot([self.x_axis_min, self.x_axis_max],
                     [0, 0],
                     color=self.zero_line_color,
                     linewidth=self.zero_line_width, )

    def plot_background_fill(self):
        self.ax.fill_between(self.background_x,
                             self.background_y1,
                             self.background_y2,
                             facecolor=self.background_fill_color,
                             edgecolor=self.background_fill_color,
                             alpha=self.background_fill_alpha,
                             zorder=self.background_fill_zorder,
                             interpolate=True)


class Histogram(FormatAx):
    """
    绘制直方图
    """
    def __init__(self, ax):
        super(Histogram, self).__init__(ax)

        self.histogram_alpha = 1
        self.histogram_color = "Blue"
        self.histogram_bins_count = 100
        self.histogram_label = "Label"
        self.histogram_label_font_size = 10

    def set_histogram(self, **kwargs):
        """
        :return:
        """
        if 'alpha' in kwargs:
            self.histogram_alpha = kwargs['alpha']
        if 'color' in kwargs:
            self.histogram_color = kwargs['color']
        if 'bins_count' in kwargs:
            self.histogram_bins_count = kwargs['bins_count']
        if 'label' in kwargs:
            self.histogram_label = kwargs['label']
        if 'label_font_size' in kwargs:
            self.histogram_label_font_size = kwargs['label_font_size']

    def plot_histogram(self, data):
        if self.x_axis_min is not None and self.x_axis_max is not None:
            x_range = (self.x_axis_min, self.x_axis_max)
        else:
            x_range = None
        self.ax.hist(data,
                     bins=self.histogram_bins_count,
                     range=x_range, histtype="bar",
                     color=self.histogram_color,
                     label=self.histogram_label,
                     alpha=self.histogram_alpha)
        self.ax.legend(prop={"size": self.histogram_label_font_size})
        self.set_ax()


def set_tick_font(ax, scale_size=11, color="#000000"):
    """
    设定刻度的字体
    """
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontproperties(FONT0)
        tick.label1.set_fontsize(scale_size)
        tick.label1.set_color(color)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontproperties(FONT0)
        tick.label1.set_fontsize(scale_size)
        tick.label1.set_color(color)


def add_label(ax, label, local, fontsize=11, fontproperties=FONT_MONO):
    """
    添加子图的标签
    :param fontproperties:
    :param fontsize:
    :param ax:
    :param label:
    :param local:
    :return:
    """
    if label is None:
        return
    if local == "xlabel":
        ax.set_xlabel(label, fontsize=fontsize, fontproperties=fontproperties)
    elif local == "ylabel":
        ax.set_ylabel(label, fontsize=fontsize, fontproperties=fontproperties)


def add_annotate(ax, strlist, local, color="#000000", fontsize=11):
    """
    添加上方注释文字
    loc must be "left_top" or "right_top"
    or "left_bottom" or "right_bottom"
    格式 ["annotate1", "annotate2"]
    """
    if strlist is None:
        return
    xticklocs = ax.xaxis.get_ticklocs()
    yticklocs = ax.yaxis.get_ticklocs()

    x_step = (xticklocs[1] - xticklocs[0])
    x_toedge = x_step / 6.
    y_toedge = (yticklocs[1] - yticklocs[0]) / 6.

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    if local == "left_top":
        ax.text(xlim[0] + x_toedge, ylim[1] - y_toedge,
                "\n".join(strlist), ha="left", va="top", color=color,
                fontsize=fontsize, fontproperties=FONT_MONO)

    elif local == "right_top":
        ax.text(xlim[1] - x_toedge, ylim[1] - y_toedge,
                "\n".join(strlist), ha="right", va="top", color=color,
                fontsize=fontsize, fontproperties=FONT_MONO)

    elif local == "left_bottom":
        ax.text(xlim[0] + x_toedge, ylim[0] + y_toedge,
                "\n".join(strlist), ha="left", va="bottom", color=color,
                fontsize=fontsize, fontproperties=FONT_MONO)
    elif local == "right_bottom":
        ax.text(xlim[1] - x_toedge, ylim[0] + y_toedge,
                "\n".join(strlist), ha="right", va="bottom", color=color,
                fontsize=fontsize, fontproperties=FONT_MONO)
    else:
        return


def set_timeseries_x_locator(ax, xlim_min, xlim_max):
    day_range = (xlim_max - xlim_min).days
    if day_range <= 6:
        return
    if day_range <= 60:
        days = mdates.DayLocator(interval=(day_range / 6))
        ax.xaxis.set_major_locator(days)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    else:
        month_range = day_range / 30
        if month_range <= 12.:
            months = mdates.MonthLocator()  # every month
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        elif month_range <= 24.:
            months = mdates.MonthLocator(interval=2)
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        elif month_range <= 48.:
            months = mdates.MonthLocator(interval=4)
            ax.xaxis.set_major_locator(months)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        else:
            years = mdates.YearLocator()
            ax.xaxis.set_major_locator(years)
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

        if month_range <= 48:
            add_year_xaxis(ax, xlim_min, xlim_max)


def add_year_xaxis(ax, xlim_min, xlim_max):
    """
    add year xaxis
    """
    if xlim_min.year == xlim_max.year:
        ax.set_xlabel(xlim_min.year, fontsize=11, fontproperties=FONT_MONO)
        return
    newax = ax.twiny()
    newax.set_frame_on(True)
    newax.grid(False)
    newax.patch.set_visible(False)
    newax.xaxis.set_ticks_position("bottom")
    newax.xaxis.set_label_position("bottom")
    newax.set_xlim(xlim_min, xlim_max)
    newax.xaxis.set_major_locator(mdates.YearLocator())
    newax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    newax.spines["bottom"].set_position(("outward", 20))
    newax.spines["bottom"].set_linewidth(0.6)

    newax.tick_params(which="both", direction="in")
    set_tick_font(newax)
    newax.xaxis.set_tick_params(length=5)


def day_data_write(title, data, outFile):
    """
    title: 标题
    data： 数据体
    outFile:输出文件
    """

    allLines = []
    DICT_D = {}
    FilePath = os.path.dirname(outFile)
    if not os.path.exists(FilePath):
        os.makedirs(FilePath)

    if os.path.isfile(outFile) and os.path.getsize(outFile) != 0:
        fp = open(outFile, "r")
        fp.readline()
        Lines = fp.readlines()
        fp.close()
        # 使用字典特性，保证时间唯一，读取数据
        for Line in Lines:
            DICT_D[Line[:8]] = Line[8:]
        # 添加或更改数据
        Line = data
        DICT_D[Line[:8]] = Line[8:]
        # 按照时间排序

        newLines = sorted(DICT_D.iteritems(), key=lambda d: d[0], reverse=False)
        for i in xrange(len(newLines)):
            allLines.append(str(newLines[i][0]) + str(newLines[i][1]))
        fp = open(outFile, "w")
        fp.write(title)
        fp.writelines(allLines)
        fp.close()
    else:
        fp = open(outFile, "w")
        fp.write(title)
        fp.writelines(data)
        fp.close()


def get_cabr_data(cbar_file):
    """
    读取日的 CABR 文件，返回 np.array
    :param cbar_file:
    :return:
    """
    try:
        names = ("date", "count", "slope", "s_std", "intercept", "i_std", "rsquared", "r_std")
        formats = ("object", "i4", "f4", "f4", "f4", "f4", "f4", "f4")
        data = np.loadtxt(cbar_file,
                          converters={0: lambda x: datetime.strptime(x, "%Y%m%d")},
                          dtype={"names": names,
                                 "formats": formats},
                          skiprows=1, ndmin=1)
    except IndexError:
        names = ("date", "count", "slope", "intercept", "rsquared")
        formats = ("object", "i4", "f4", "f4", "f4")
        data = np.loadtxt(cbar_file,
                          converters={0: lambda x: datetime.strptime(x, "%Y%m%d")},
                          dtype={"names": names,
                                 "formats": formats},
                          skiprows=1, ndmin=1)

    return data


def get_bias_data(md_file):
    """
    读取日的 MD 文件，返回 np.array
    :param md_file:
    :return:
    """
    try:
        names = ("date", "bias", "bias_std", "md", "md_std")
        formats = ("object", "f4", "f4", "f4", "f4")
        data = np.loadtxt(md_file,
                          converters={0: lambda x: datetime.strptime(x, "%Y%m%d")},
                          dtype={"names": names,
                                 "formats": formats},
                          skiprows=1, ndmin=1)
    except IndexError:
        names = ("date", "bias", "md")
        formats = ("object", "f4", "f4")
        data = np.loadtxt(md_file,
                          converters={0: lambda x: datetime.strptime(x, "%Y%m%d")},
                          dtype={"names": names,
                                 "formats": formats},
                          skiprows=1, ndmin=1)
    return data


def bias_information(x, y, boundary=None, bias_range=1):
    """
    # 过滤 range%10 范围的值，计算偏差信息
    # MeanBias( <= 10 % Range) = MD±Std @ MT
    # MeanBias( > 10 % Range) = MD±Std @ MT
    :param bias_range:
    :param x:
    :param y:
    :param boundary:
    :return: MD Std MT 偏差均值 偏差 std 样本均值
    """
    bias_info = {}

    if boundary is None:
        return bias_info
    # 计算偏差
    delta = x - y

    # 筛选大于界限值的数据
    idx_greater = np.where(x > boundary)
    delta_greater = delta[idx_greater]
    x_greater = x[idx_greater]
    # 筛选小于界限值的数据
    idx_lower = np.where(x <= boundary)
    delta_lower = delta[idx_lower]
    x_lower = x[idx_lower]

    # 计算偏差均值，偏差 std 和 样本均值
    md_greater = delta_greater.mean()  # 偏差均值
    std_greater = delta_greater.std()  # 偏差 std
    mt_greater = x_greater.mean()  # 样本均值

    md_lower = delta_lower.mean()
    std_lower = delta_lower.std()
    mt_lower = x_lower.mean()

    # 格式化数据
    info_lower = "MeanBias(<={:d}%Range)={:.4f}±{:.4f}@{:.4f}".format(
        int(bias_range * 100), md_lower, std_lower, mt_lower)
    info_greater = "MeanBias(>{:d}%Range) ={:.4f}±{:.4f}@{:.4f}".format(
        int(bias_range * 100), md_greater, std_greater, mt_greater)

    bias_info = {"md_greater": md_greater, "std_greater": std_greater,
                 "mt_greater": mt_greater,
                 "md_lower": md_lower, "std_lower": std_lower,
                 "mt_lower": mt_lower,
                 "info_lower": info_lower, "info_greater": info_greater}

    return bias_info


def get_month_avg_std(date_day, value_day):
    """
    由日数据生成月平均数据
    :param date_day: (list) [datetime 实例]
    :param value_day: (list)
    :return: (date_month, avg_month, std_month)
    """
    date_month = []
    avg_month = []
    std_month = []

    date_day = np.array(date_day)
    value_day = np.array(value_day)

    ymd_start = np.nanmin(date_day)  # 第一天日期
    ymd_end = np.nanmax(date_day)  # 最后一天日期
    month_date_start = ymd_start - relativedelta(
        days=(ymd_start.day - 1))  # 第一个月第一天日期

    while month_date_start <= ymd_end:
        # 当月最后一天日期
        month_date_end = month_date_start + relativedelta(months=1) - relativedelta(days=1)

        # 查找当月所有数据
        month_idx = np.logical_and(date_day >= month_date_start, date_day <= month_date_end)
        value_month = value_day[month_idx]

        avg = np.nanmean(value_month)
        std = np.nanstd(value_month)
        date_month = np.append(date_month, month_date_start + relativedelta(days=14))
        avg_month = np.append(avg_month, avg)
        std_month = np.append(std_month, std)

        month_date_start = month_date_start + relativedelta(months=1)
    return date_month, avg_month, std_month


if __name__ == "__main__":
    t_base_map = Basemap()
    t_m_patches = mpatches
