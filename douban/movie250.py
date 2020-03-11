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
import datetime
import time
import csv
import re

from base.HtmlData import HtmlData
from base.CsvAction import CsvAction
from base.Charts import Charts


class movieData(object):
    def __init__(self):
        self.url = "https://movie.douban.com/top250?start={}&filter="
        self.fieldnames = ['序号', '电影名称', '年份', '国家', '类型', '导演主演', '评分', '评分人数',
                           '短评', '链接']
        csvName = str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.csv'
        self.csvPath = os.path.join(os.path.abspath('..'), 'data', csvName)
        f = open(self.csvPath, 'w')
        writer = csv.DictWriter(f, fieldnames=self.fieldnames)
        writer.writeheader()
        f.close()

    def getMovies(self):
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
                # director, starring = (re.match(r'导演: (.*)\xa0\xa0\xa0(.*)', info[0], re.S)).groups()
                # year, country, type = (
                #     re.match(r'(\d{4})\xa0/\xa0(.*)\xa0/\xa0(.*)',
                #              info[1].lstrip(), re.S)).groups()

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
                movieInfo = [str(num), name, year, country, type,
                             director_starring, store, store_court, intro,
                             movie_url]
                print('_____________{}'.format(movieInfo))
                writer.writerow(movieInfo)
            time.sleep(3)
        f.close()

    # def write2csv(self, *args):
    #     csvData = CsvAction()
    #     if args is not None:
    #         csvData.writeCsv(args)
    #     else:
    #         raise Exception("nothing to write")


if __name__ == '__main__':
    m = movieData()
    m.getMovies()
