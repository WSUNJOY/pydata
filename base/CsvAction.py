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


if __name__ == '__main__':
    c = CsvAction()
    c.writeCsv(['a', 'b'])
