# -*- coding: utf-8 -*-
"""
@Time    : 2018/6/29 14:33
@Author  : AnNing
"""
import os
from math import floor, ceil
from datetime import datetime

import numpy as np
from scipy import stats
import matplotlib as mpl

mpl.use("Agg")  # 必须加这个字段，否则引用 pyplot 服务器会报错，服务器上面没有 TK

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from matplotlib.font_manager import FontProperties
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches


def get_ds_font(fontName="OpenSans-Regular.ttf"):
    """
    载入字体
    "OpenSans-Regular.ttf"
    "simhei.ttf"
    "微软雅黑.ttf"
    """
    selfpath = os.path.split(os.path.realpath(__file__))[0]
    font0 = FontProperties()
    font_path = os.path.join(selfpath, "FNT", fontName)
    if os.path.isfile(font_path):
        font0.set_file(font_path)
        return font0
    return None


FONT0 = get_ds_font()
FONT1 = get_ds_font()
FONT_MONO = get_ds_font("DroidSansMono.ttf")


class PlotAx(object):
    """
    """
    def __init__(self, ax):
        self.ax = ax

        self.font = FONT0

        self.x_label = None
        self.y_label = None
        self.x_label_font_size = 11
        self.y_label_font_size = 11

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
        # 设置 label
        if self.x_label:
            self.ax.set_xlabel(self.x_label, fontsize=self.x_label_font_size,
                               fontproperties=self.font)
        if self.y_label:
            self.ax.set_ylabel(self.y_label, fontsize=self.y_label_font_size,
                               fontproperties=self.font)
        # 设置大刻度和小刻度的数量
        if self.x_major_count and self.x_axis_min and self.x_axis_max:
            self.ax.xaxis.set_major_locator(
                MultipleLocator((self.x_axis_max - self.x_axis_min) / self.x_major_count))
        if self.y_major_count and self.y_axis_min and self.y_axis_max:
            self.ax.yaxis.set_major_locator(
                MultipleLocator((self.y_axis_max - self.y_axis_min) / self.y_major_count))
        if self.x_minor_count:
            x_ticklocs = self.ax.xaxis.get_ticklocs()
            self.ax.xaxis.set_minor_locator(
                MultipleLocator((x_ticklocs[1] - x_ticklocs[0]) / self.x_minor_count))
        if self.y_minor_count:
            y_ticklocs = self.ax.yaxis.get_ticklocs()
            self.ax.yaxis.set_minor_locator(
                MultipleLocator((y_ticklocs[1] - y_ticklocs[0]) / self.y_minor_count))
        # 设置刻度文字的大小
        if self.tick_font_size:
            set_tick_font(self.ax, scale_size=self.tick_font_size)
        # 设置 x y 轴的范围
        if self.x_axis_min and self.x_axis_max:
            self.ax.set_xlim(self.x_axis_min, self.x_axis_max)
        if self.y_axis_min and self.y_axis_max:
            self.ax.set_ylim(self.y_axis_min, self.y_axis_max)
        # 设置图片注释文字
        if self.annotate:
            for k in self.annotate:
                add_annotate(self.ax, self.annotate[k], k, fontsize=self.annotate_font_size)


class Histogram(PlotAx):
    """
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


def add_title(titledict):
    """
    添加大标题和xy轴名称
    """
    tt = plt.title(titledict["title"], fontsize=11, fontproperties=FONT0)
    tt.set_y(1.01)  # set gap space below title and subplot
    if "xlabel" in titledict.keys() and titledict["xlabel"] != "":
        plt.xlabel(titledict["xlabel"], fontsize=11, fontproperties=FONT0)
    if "ylabel" in titledict.keys() and titledict["ylabel"] != "":
        plt.ylabel(titledict["ylabel"], fontsize=11, fontproperties=FONT0)


def add_label(ax, label, local, fontsize=11, fontproperties=FONT0):
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


def get_bar_data(xx, delta, Tmin, Tmax, step):
    T_seg = []
    mean_seg = []
    std_seg = []
    sampleNums = []
    for i in np.arange(Tmin, Tmax, step):
        idx = np.where(np.logical_and(xx >= i, xx < (i + step)))[0]

        if idx.size > 0:
            DTb_block = delta[idx]
        else:
            continue

        mean1 = np.mean(DTb_block)
        std1 = np.std(DTb_block)

        idx1 = np.where((abs(DTb_block - mean1) < std1))[0]  # 去掉偏差大于std的点
        if idx1.size > 0:
            DTb_block = DTb_block[idx1]
            mean_seg.append(np.mean(DTb_block))
            std_seg.append(np.std(DTb_block))
            sampleNums.append(len(DTb_block))
        else:
            mean_seg.append(0)
            std_seg.append(0)
            sampleNums.append(0)
        T_seg.append(i + step / 2.)

    return np.array(T_seg), np.array(mean_seg), np.array(std_seg), np.array(
        sampleNums)


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


def set_x_locator(ax, xlim_min, xlim_max):
    day_range = (xlim_max - xlim_min).days
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
        ax.set_xlabel(xlim_min.year, fontsize=11, fontproperties=FONT0)
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


if __name__ == "__main__":
    pass
