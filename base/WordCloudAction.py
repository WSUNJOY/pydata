# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: WordCloudAction.py
@time: 2020/3/18 10:41 下午
@description: 
"""
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import jieba
import os


class WordCloudAtion(object):
    def __init__(self):
        pass

    def wordjieba(self, word):
        word_jieba = jieba.cut(word)
        wl = " ".join(word_jieba)
        return wl

    def wordCloudImage(self, word, imageName=None, bg=None):
        if bg is None:
            bgImagePath = os.path.join(os.path.abspath('..'), 'source', 'pic',
                                     'douban.png')
        else:
            bgImagePath = bg
        if imageName is None:
            wordImagePath = os.path.join(os.path.abspath('..'), 'MatPic',
                                         'movieData',
                                         'wordImage.png')
        else:
            wordImagePath = os.path.join(os.path.abspath('..'), 'MatPic',
                                         'movieData',
                                         imageName)
        fontPath = os.path.join(os.path.abspath('..'), 'source', 'font',
                                'SimHei.ttf')
        bgImage = np.array(Image.open(bgImagePath))
        font = fontPath

        wl = self.wordjieba(word)
        sw = set(STOPWORDS)
        sw.add("xx")
        wordcloud = WordCloud(scale=4,
                              font_path=font,
                              mask=bgImage,
                              stopwords=sw,
                              background_color='white',
                              max_words=100,
                              max_font_size=60,
                              random_state=20).generate(wl)
        image_colors = ImageColorGenerator(bgImage)
        wordcloud.recolor(color_func=image_colors)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        wordcloud.to_file(wordImagePath)


if __name__ == '__main__':
    wd = WordCloudAtion()
    wd.wordCloudImage(word='None')
