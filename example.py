# coding: UTF-8
import numpy as np
from dv_plt import dv_time_series, plt, dv_line_chart, RED, add_colorbar_below
from dv_map import dv_map
from datetime import datetime
from matplotlib import gridspec
from DV.dv_plt import get_DV_Font


x1 = [1, 2, 3, 4, 5, 6, 7]
y1 = [6, 7, 6, 8, 4, 5, 9]
x2 = [3, 4, 5, 6, 7, 8, 9]
y2 = [2, 5, 3, None, 5, 8, 3]
x3 = [datetime(2015, 3, 1, e) for e in x1]
x4 = [datetime(2015, 3, 4, e) for e in x2]

def test0():
    '''
    4图画在一张 等比例
    '''
    fig = plt.figure(figsize=(6.8, 6))  # 图像大小

    p = dv_line_chart(fig, subplot=221)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图1'
    p.xlabel = u'X轴'
    p.ylabel = u'Y轴'
    p.grid(True)
    p.draw()

    p = dv_line_chart(fig, subplot=222)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图2'
    p.xlabel = u'X轴'
    p.draw()

    p = dv_line_chart(fig, subplot=223)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图3'
    p.xlabel = u'X轴'
    p.ylabel = u'Y轴'
    p.draw()

    p = dv_time_series(fig, subplot=224)
    p.easyplot(x3, y1, RED, u'甲')
#     p.title = u'图4'
    p.xlabel = u'X轴'

    # 调整间距
    fig.subplots_adjust(bottom=0.08, top=0.8,  # 下， 上
                        left=0.07, right=0.87,  # 左， 右
                        wspace=0.26, hspace=0.25)  # 列间距（width方向）， 行间距（height方向）
    # 总标题
    fig.suptitle("Title centered above all subplots", fontproperties=get_DV_Font(), size=9)
    p.savefig('4in1_0.png')

def test1():
    '''
    4图画在一张 自定比例
    '''
    fig = plt.figure(figsize=(6.8, 6))  # 图像大小
    gs = gridspec.GridSpec(2, 2,  # 两行两列
                           width_ratios=[1, 2],  # 两列比例 1：2
                           height_ratios=[4, 1]  # 两行比例 4：1
                          )

    ax1 = plt.subplot(gs[0])  # 2行 2列  第1张
    p = dv_line_chart(fig, ax1)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图1'
    p.xlabel = u'X轴'
    p.ylabel = u'Y轴'
    p.draw()

    ax2 = plt.subplot(gs[1])
    p = dv_line_chart(fig, ax2)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图2'
    p.xlabel = u'X轴'
    p.draw()

    ax3 = plt.subplot(gs[2])
    p = dv_line_chart(fig, ax3)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图3'
    p.xlabel = u'X轴'
    p.ylabel = u'Y轴'
    p.draw()

    ax4 = plt.subplot(gs[3])
    p = dv_time_series(fig, ax4)
    p.easyplot(x3, y1, RED, u'甲')
#     p.title = u'图4'
    p.xlabel = u'X轴'

    # 调整间距
    fig.subplots_adjust(bottom=0.08, top=0.935,  # 下， 上
                        left=0.07, right=0.87,  # 左， 右
                        wspace=0.26, hspace=0.25)  # 列间距（width方向）， 行间距（height方向）
    # 总标题
    fig.suptitle("Title centered above all subplots", fontproperties=get_DV_Font(), size=9)
    p.savefig('4in1.png')


def test2():
    '''
    # 3图画在一张 2行 
    第1行2张
    第2行1张
    '''
    fig = plt.figure(figsize=(6.8, 6))  # 图像大小
    p = dv_line_chart(fig, subplot=221)  # 221：2行 2列 的第1张
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图1'
    p.xlabel = u'X轴'
    p.ylabel = u'Y轴'
    p.draw()

    p = dv_line_chart(fig, subplot=222)
    p.easyplot(x1, y1, 'c', u'w')
    p.easyplot(x2, y2, 'b', u'a')
#     p.show_leg = False
#     p.title = u'图2'
    p.xlabel = u'X轴'
    p.draw()

    p = dv_time_series(fig, subplot=212)  # 212：2行 1列 的第2张
    p.easyplot(x3, y1, RED, u'甲')
#     p.title = u'图4'
    p.xlabel = u'X轴'

    # 调整间距
    fig.subplots_adjust(bottom=0.08, top=0.935, left=0.07, right=0.87,
                        wspace=0.26, hspace=0.25)
    # 总标题
    fig.suptitle("Title centered above all subplots", fontproperties=p.font, size=9)
    p.savefig('3in1.png')

def test3():
    """
    上下2张图， 比例3：1
    """
    # 全球-----------------------

    lats, lons = np.mgrid[70 :0 :-6, 50 : 150: 6]
    values = np.random.random_integers(0., 10000., lats.shape)


    fig = plt.figure(figsize=(5, 6))  # 图像大小
    gs = gridspec.GridSpec(2, 1,  # 两行一列
                           height_ratios=[3, 1]  # 两行比例 3：1
                          )
    # 中国
    ax1 = plt.subplot(gs[0])
    p = dv_map(fig, ax1)
    p.colorbar_fmt = "%d"
    p.show_countries = False
    p.show_china = True
    p.show_china_province = True
    p.show_line_of_latlon = False
#     p.show_inside_china = True
#     p.setArea(u"中国省界", ["Beijing"])
#     p.show_colorbar = False
#     p.projection = "aea"
    p.colorbar_bounds = range(0, 10001, 1000)
    p.easyplot(lats, lons, values, ptype='contourf', vmin=0, vmax=10000)
#     p.title = u'中国区域分布图'
    p.draw()

    ax2 = plt.subplot(gs[1])
    p = dv_time_series(fig, ax2)
    p.easyplot(x3, y1, 'r', u'甲')
#     p.title = u'图4'
    p.xlabel = u'X轴'
    p.fontsize_tick = 8
    # 调整间距
    fig.subplots_adjust(bottom=0.1, top=0.96, left=0.07, right=0.87,
                        hspace=0.15)

    # 总标题
    fig.suptitle("Title centered above all subplots", fontproperties=p.font, size=9)
    p.savefig('2in1.png')


def test3_wp():
    """
    上下2张图， 比例3：1
    """
    # 全球-----------------------

    lats, lons = np.mgrid[70 :0 :-6, 50 : 150: 6]
    values = np.random.random_integers(0., 10000., lats.shape)


    fig = plt.figure(figsize=(5, 6))  # 图像大小
    gs = gridspec.GridSpec(2, 1,  # 两行一列
                           height_ratios=[3, 0.5]  # 两行比例 3：1
                          )
    # 中国
    ax1 = plt.subplot(gs[0])
    p = dv_map(fig, ax1)
    p.colorbar_fmt = "%d"

    p.show_colorbar = False
    p.show_countries = False
    p.show_china = True
    p.show_china_province = True
    p.show_line_of_latlon = False
#     p.show_inside_china = True
#     p.setArea(u"中国省界", ["Beijing"])
#     p.show_colorbar = False
#     p.projection = "aea"
    p.colorbar_bounds = range(0, 10001, 1000)
    p.easyplot(lats, lons, values, ptype='contourf', vmin=0, vmax=10000)
#     p.title = u'中国区域分布图'
    p.draw()

    ax2 = plt.subplot(gs[1])
    plt.sca(ax2)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.grid(False)
    ax2.set_ylabel(False)
    ax2.set_xticks([])
    ax2.set_yticks([])

    hist, bins = np.histogram(values, bins=80)
#     print bins
    hist = hist / (values.size * 1.0)
    center = (bins[:-1] + bins[1:]) / 2
    width = (bins[1] - bins[0])
#     plt.grid(b, which, axis)

    plt.bar(center, hist, align='center', width=width, color=None, alpha=0.5, edgecolor='b')
    add_colorbar_below(fig, 0.1, 1 - 0.1, 0.075, 0, 10000)

    # 总标题
    fig.suptitle("Title centered above all subplots", fontproperties=p.font, size=9)
    p.savefig('2in1.png')

def north_south():

    lats, lons = None, None
    values = None

    fig = plt.figure(figsize=(9, 5))  # 图像大小
    # 北极
    p = dv_map(fig, subplot=121)
    p.show_colorbar = False
    p.show_north = True
    p.show_bg_color = True
    p.easyplot(lats, lons, values, ptype='contourf', vmin=0, vmax=10000)

    p.draw()

    # 南极
    p = dv_map(fig, subplot=122)
    p.show_colorbar = False
    p.show_south = True
    p.show_bg_color = True
    p.easyplot(lats, lons, values, ptype='contourf', vmin=0, vmax=10000)

    fig.subplots_adjust(bottom=0.09, top=0.97, left=0.04, right=0.96,
                        wspace=0.06)
    fig.suptitle("North Pole & South Pole", fontproperties=p.font, size=9.5)

    # add colorbar below
    add_colorbar_below(fig, 0.3, 1 - 0.3, 0.07, 0, 100)
    p.savefig('ns.png')

def north_south_poles():

    lats, lons = None, None
    values = None

    fig = plt.figure(figsize=(9, 5))  # 图像大小
    # 北极
    p = dv_map(fig, subplot=121)
    p.show_colorbar = False
    p.show_north_pole = True
    p.show_bg_color = True
    p.easyplot(lats, lons, values, ptype='contourf', vmin=0, vmax=10000)

    p.draw()

    # 南极
    p = dv_map(fig, subplot=122)
    p.show_colorbar = False
    p.show_south_pole = True
    p.show_bg_color = True
    p.easyplot(lats, lons, values, ptype='contourf', vmin=0, vmax=10000)

    fig.subplots_adjust(bottom=0.1, top=0.97, left=0.06, right=0.94,
                        wspace=0.12)
    fig.suptitle("North Pole & South Pole", fontproperties=p.font, size=9.5)

    # add colorbar below
    add_colorbar_below(fig, 0.3, 1 - 0.3, 0.07, 0, 100)
    p.savefig('poles.png')

if __name__ == '__main__':
    # example
#     north_south()
    test3_wp()
