# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: HtmlData.py
@time: 2020/3/3 11:08 下午
@description: 
"""
import requests
from bs4 import BeautifulSoup
import datetime
import os

class HtmlData(object):
    def __init__(self, url=None, headers=None):
        if isinstance(url, str):
            self.url = url
        if headers is None:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
            }
        else:
            if isinstance(headers, dict):
                self.headers = headers
            else:
                raise Exception("headers is not a dict")

    def getUrlSoup(self, url=None):
        if isinstance(url, str):
            self.url = url
        if self.url is None:
            raise Exception("url is None")
        html = requests.get(url=self.url, headers=self.headers)
        # name = str(
        #     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '.html'
        # path = os.path.join(os.path.abspath('..'), 'data', name)
        # with open(path, 'wb') as f:
        #     f.writelines(html)
        self.soup = BeautifulSoup(html.text.encode('utf-8'), 'lxml')
        return self.soup

    def getFileSoup(self, name):
        # name = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.xhtml'
        path = os.path.join(os.path.abspath('..'), 'data', name)
        # print(type(path))
        html = ''
        with open(path, 'r', encoding='utf-8') as f:
            reader = f.readlines()
            for i in reader:
                html += i
            f.close()
        self.soup = BeautifulSoup(html, 'lxml')
        return self.soup

    def getSoup(self, soup):
        print(soup.title.string)


if __name__ == '__main__':
    url = 'https://movie.douban.com/top250'
    h = HtmlData(url)
    # print(h.getUrlSoup())
    soup = h.getFileSoup('2020-03-09 14:19:56.html')
    h.getSoup(soup)