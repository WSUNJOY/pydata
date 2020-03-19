# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: movie250.py
@time: 2020/3/9 3:43 下午
@description: 
"""
import os
import sys
import datetime
import time
import csv
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter
import matplotlib
# %matplotlib inline

# matplotlib不会每次启动时都重新扫描所有的字体文件并创建字体索引列表，
# 因此在复制完字体文件之后，需要运行下面的语句以重新创建字体索引列表
from matplotlib.font_manager import _rebuild

from base.HtmlData import HtmlData
from base.WordCloudAction import WordCloudAtion

_rebuild()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 引入加载字体名
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['font.size'] = 20


class movieData(object):
    def __init__(self):
        self.url = "https://movie.douban.com/top250?start={}&filter="
        self.fieldnames = ['序号', '电影名称', '年份', '国家', '类型', '导演',
                           '主演', '评分', '评分人数', '短评', '链接']
        # self.fieldnames = ['序号', '电影名称', '年份', '国家', '类型', '导演主演',
        #                    '评分', '评分人数', '短评', '链接']
        csvName = str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.csv'
        self.csvPath = os.path.join(os.path.abspath('..'), 'data', csvName)

    def getMovies(self):
        f = open(self.csvPath, 'w')
        writer = csv.DictWriter(f, fieldnames=self.fieldnames)
        writer.writeheader()
        f.close()
        html = HtmlData()
        num = 0
        movie_url = []
        name = []
        store = []
        store_court = []
        intro = []
        director, starring = [], []
        year, country, type = [], [], []
        f = open(self.csvPath, 'a+')
        writer = csv.writer(f)
        for i in range(25):
            soup = html.getUrlSoup(self.url.format(i * 25))
            ol = soup.find('ol', class_="grid_view")
            for li in ol.find_all('li'):
                # print(li)
                hd = li.find('div', class_="hd")
                movie_url = hd.find('a').get('href')
                name = hd.find('span', class_="title").get_text()
                bd = li.find('div', class_='bd')
                info = bd.find('p').get_text().strip().split('\n')
                director_starring = info[0].strip()
                year, country, type = info[1].strip().split('\xa0/\xa0')

                # re maybe error
                try:
                    director, starring = (
                        re.match(r'导演: (.*)\xa0\xa0\xa0主演: (.*)', info[0],
                                 re.S)).groups()
                    year, country, type = (
                        re.match(r'(\d{4})\xa0/\xa0(.*)\xa0/\xa0(.*)',
                                 info[1].lstrip(), re.S)).groups()
                except Exception as e:
                    director = (re.match(r'导演: (.*)', info[0], re.S)).group(1)
                    starring = None

                star = bd.find('div', class_="star")
                store = star.find('span',
                                  class_="rating_num").get_text()
                store_court = (re.match(r'(\d*).*', star.find_all('span')[
                    3].get_text())).groups()[0]
                try:
                    intro = bd.find('span', class_="inq").get_text().strip()
                except Exception as e:
                    intro = None
                num += 1
                # movieInfo = [str(num), name, year, country, type,
                #              director_starring, store, store_court, intro,
                #              movie_url]
                movieInfo = [str(num), name, year, country, type,
                             director, starring, store, store_court, intro,
                             movie_url]
                print('_____________{}'.format(movieInfo))
                writer.writerow(movieInfo)
            time.sleep(3)
        f.close()

    def pdCsv(self, path=None):
        if path is None:
            path = os.path.join(os.path.abspath('..'), 'data',
                                '2020-03-16 11:47:54.csv')
        df = pd.read_csv(path)
        df.info()
        df.head()
        df.duplicated().value_counts()
        return df

    def countryData(self):
        df = self.pdCsv()
        country = df[u'国家'].str.split(' ').apply(pd.Series)
        all_country = country.apply(pd.value_counts).fillna('0')
        all_country.columns = ['area1', 'area2', 'area3', 'area4', 'area5',
                               'area6']
        all_country['area1'] = all_country['area1'].astype(int)
        all_country['area2'] = all_country['area2'].astype(int)
        all_country['area3'] = all_country['area3'].astype(int)
        all_country['area4'] = all_country['area4'].astype(int)
        all_country['area5'] = all_country['area5'].astype(int)
        all_country['area6'] = all_country['area6'].astype(int)
        all_country['all_counts'] = all_country['area1'] + all_country[
            'area2'] + \
                                    all_country['area3'] + all_country[
                                        'area4'] + \
                                    all_country['area5'] + all_country['area6']
        all_country.sort_values(['all_counts'], ascending=False)
        print(all_country.head())
        return all_country['all_counts']

    def typeData(self):
        df = self.pdCsv()
        tpye = df[u'类型'].str.split(' ').apply(pd.Series)
        all_type = tpye.apply(pd.value_counts).fillna('0')
        all_type['all_counts'] = 0
        for i in range(len(all_type.columns) - 1):
            all_type[all_type.columns[i]] = all_type[
                all_type.columns[i]].astype(int)
            all_type['all_counts'] += all_type[all_type.columns[i]]
        all_type.sort_values(['all_counts'], ascending=False)
        # print(all_type)
        # print(all_type['all_counts'])
        return all_type['all_counts']

    def typeData2(self):
        df = self.pdCsv()
        tpye = df[u'类型'].str.split(' ').apply(pd.Series)
        all_type = tpye.apply(pd.value_counts).unstack().dropna().reset_index()
        all_type.columns = ['level_0', 'level_1', 'counts']
        all_type_m = all_type.drop(['level_0'], axis=1).groupby('level_1').sum()
        all_type_m.sort_values(['counts'], ascending=False)
        print(all_type_m['counts'])
        return all_type_m['counts']

    def yearData(self):
        df = self.pdCsv()

        # way1
        year = df[u'年份'].value_counts()
        return year

        # way2
        # all_year = year.unstack().dropna().reset_index()
        # year = df[u'年份'].apply(pd.Series)
        # all_year = year.apply(pd.value_counts).unstack().dropna().reset_index()
        # all_year.columns = ['level_0', 'level_1', 'counts']
        # all_year_m = all_year.drop(['level_0'], axis=1).groupby('level_1').sum()
        # all_year_m.sort_values(['counts'], ascending=False)
        # return all_year_m['counts']

    def scoreData(self):
        df = self.pdCsv()
        score = df[u'评分'].value_counts()
        print(score)
        return score

    def directorData(self):
        df = self.pdCsv()
        director = df[u'导演'].str.strip('主演...').str.strip('主...').str.split(
            ' / ').apply(pd.Series)
        # director = df[u'导演'].str.split(' / ').apply(pd.Series)
        all_director = director.apply(pd.value_counts).fillna('0')
        all_director['all_counts'] = 0
        for i in range(len(all_director.columns) - 1):
            all_director[all_director.columns[i]] = all_director[
                all_director.columns[i]].astype(int)
            all_director['all_counts'] += all_director[all_director.columns[i]]
        all_director.sort_values(['all_counts'], ascending=False)
        print(all_director['all_counts'].head(20))
        return all_director['all_counts']

    def directorChart(self):
        picName = os.path.join(os.path.abspath('..'), 'MatPic',
                               self.__class__.__name__,
                               sys._getframe().f_code.co_name)
        director = self.directorData()[self.directorData() > 1]
        movie_director = pd.DataFrame({'数量': director}).sort_values(by='数量',
                                                                    ascending=False)
        movie_director.plot(kind='bar', figsize=(20, 10))
        plt.xlabel(u'电影导演')
        plt.ylabel(u'数量')
        plt.title(u'电影导演数量图')
        plt.savefig(picName)
        plt.show()

    def yearChart(self):
        picName = os.path.join(os.path.abspath('..'), 'MatPic',
                               self.__class__.__name__,
                               sys._getframe().f_code.co_name)
        year = self.yearData()
        movie_year = pd.DataFrame({'数量': year}).sort_values(by='数量',
                                                            ascending=False)
        movie_year.plot(kind='bar', figsize=(10, 6))
        plt.xlabel(u'电影年份')
        plt.ylabel(u'数量')
        plt.title(u'电影年份数量图')
        plt.savefig(picName)
        plt.show()

    def typeChart(self):
        picName = os.path.join(os.path.abspath('..'), 'MatPic',
                               self.__class__.__name__,
                               sys._getframe().f_code.co_name)
        typeCounts = self.typeData2()
        movie_type = pd.DataFrame({'数量': typeCounts}).sort_values(by='数量',
                                                                  ascending=False)
        movie_type.plot(kind='bar', figsize=(10, 6))
        plt.xlabel(u'电影类型')
        plt.ylabel(u'数量')
        plt.title(u'电影类型数量图')
        plt.savefig(picName)
        plt.show()

    def countryChart(self):
        picName = os.path.join(os.path.abspath('..'), 'MatPic',
                               self.__class__.__name__,
                               sys._getframe().f_code.co_name)
        country = self.countryData()
        movie_country = pd.DataFrame({'数量': country}).sort_values(by='数量',
                                                                  ascending=False)
        movie_country.plot(kind='bar', figsize=(10, 6))
        plt.xlabel(u'国家')
        plt.ylabel(u'数量')
        plt.title(u'电影国家数量图')
        plt.savefig(picName)
        plt.show()

    def scoreIndexSubChart(self):
        picName = os.path.join(os.path.abspath('..'), 'MatPic',
                               self.__class__.__name__,
                               sys._getframe().f_code.co_name)
        print(picName)
        df = self.pdCsv()
        xlabel = u'评分'
        ylabel = u'排名'
        xSlabel = u'评分'
        ySlabel = u'出现次数'
        x = df[xlabel]
        print(x)
        y = df[u'序号']
        plt.figure(figsize=(20, 8))
        plt.subplot(1, 2, 1)
        plt.scatter(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # 修改y轴为倒序
        plt.gca().invert_yaxis()

        # 集中趋势的直方图
        plt.subplot(1, 2, 2)
        plt.hist(x, bins=15)
        plt.xlabel(xSlabel)
        plt.ylabel(ySlabel)

        plt.savefig(picName)
        plt.show()

    def scorePeopleSubChart(self):
        picName = os.path.join(os.path.abspath('..'), 'MatPic',
                               self.__class__.__name__,
                               sys._getframe().f_code.co_name)
        df = self.pdCsv()
        xlabel = u'评分人数'
        ylabel = u'排名'
        xSlabel = u'评分人数'
        ySlabel = u'出现次数'
        x = df[xlabel]
        # set_printoptions(suppress=True)
        print(x)
        y = df[u'序号']
        plt.figure(figsize=(30, 8))
        plt.subplot(1, 2, 1)
        plt.scatter(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # 修改y轴为倒序
        plt.gca().invert_yaxis()

        # 集中趋势的直方图
        plt.subplot(1, 2, 2)
        plt.hist(x, bins=25)
        plt.xlabel(xSlabel)
        plt.ylabel(ySlabel)
        plt.savefig(picName)
        plt.show()

    def commentWordCloud(self):
        df = self.pdCsv()
        wl = WordCloudAtion()
        imageName = 'commentWC.jpg'
        comment = df[u'短评'].to_string()
        wl.wordCloudImage(word=comment, imageName=imageName)

    def typeAndCountryWordCloud(self):
        df = self.pdCsv()
        wl = WordCloudAtion()
        imageName = 'type&countryWC.jpg'
        bg = os.path.join(os.path.abspath('..'), 'source', 'pic', 'cloud.png')
        comment = df[u'国家'].to_string() + df[u'类型'].to_string()
        wl.wordCloudImage(word=comment, imageName=imageName, bg=bg)

    def actorAnddirectorWordCloud(self):
        df = self.pdCsv()
        wl = WordCloudAtion()
        imageName = 'actor&directorWC.jpg'
        bg = os.path.join(os.path.abspath('..'), 'source', 'pic', 'head.jpeg')
        comment = df[u'导演'].to_string() + df[u'主演'].dropna().to_string()
        wl.wordCloudImage(word=comment, imageName=imageName, bg=bg)


if __name__ == '__main__':
    m = movieData()
    # m.getMovies()
    # m.typeData()
    # m.typeData2()
    # m.yearData()
    # m.directorData()
    # m.scoreData()
    m.scoreIndexSubChart()
    m.scorePeopleSubChart()
    m.typeChart()
    m.countryChart()
    m.directorChart()
    m.commentWordCloud()
    m.typeAndCountryWordCloud()
    m.actorAnddirectorWordCloud()