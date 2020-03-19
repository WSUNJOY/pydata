# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: CsvAction.py
@time: 2020/3/9 10:55 上午
@description: 
"""
import os
import csv
import datetime
import numpy as np
import pandas as pd
class CsvAction(object):
    def __init__(self):
        pass
    def writeCsv(self, *args):
        # name = str(datetime.datetime.now().strftime("%Y-%m-%d")) + '.csv'
        name = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))+'.csv'
        path = os.path.join(os.path.abspath('..'), 'data', name)
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            # writer.writerow(args)
            writer.writerows(args)

    def readCsv(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    def readDictCsv(self, path):
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(row['first_name'], row['last_name'])

class PdCsv(object):
    def __init__(self):
        pass
    def readcsv(self, path):
        self.df = pd.read_csv(path)
        return self.df
    def csvHead(self):
        return self.df.head()
    def csvInfo(self):
        return self.df.info()
    def duplicated(self):
        self.df.duplicated().value_counts()

if __name__ == '__main__':
    # c = CsvAction()
    # c.writeCsv(['a', 'b'])
    path = os.path.join(os.path.abspath('..'), 'data', '2020-03-11 23:46:26.csv')
    p = PdCsv()
    # print(p.readcsv(path).info())
    # print(p.readcsv(path).duplicated().value_counts())
