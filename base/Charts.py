# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: Charts.py
@time: 2020/3/9 10:37 上午
@description: 
"""
import os
import matplotlib.pyplot as plt
import matplotlib
# %matplotlib inline

#matplotlib不会每次启动时都重新扫描所有的字体文件并创建字体索引列表，
# 因此在复制完字体文件之后，需要运行下面的语句以重新创建字体索引列表
from matplotlib.font_manager import _rebuild
_rebuild()
plt.rcParams['font.sans-serif'] = ['SimHei']     # 引入加载字体名
plt.rcParams['axes.unicode_minus'] = False      # 解决保存图像是负号'-'显示为方块的问题
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.size'] = 20

class Charts(object):
    def __init__(self):
        pass
    def movies(self, x, y, xlabel, ylabel, xSlabel, ySlabel, title1=None, title2=None):
        plt.figure(figsize=(20, 5))
        plt.subplot(1, 2, 1)
        ax.set_title(title1)
        plt.scatter(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # 修改y轴为倒序
        plt.gca().invert_yaxis()

        # 集中趋势的直方图
        plt.subplot(1, 2, 2)
        plt.hist(x, bins=14)
        ax.set_title(title2)
        plt.xlabel(xSlabel)
        plt.ylabel(ySlabel)
        plt.show()

if __name__ == '__main__':
    print(os.getcwd())