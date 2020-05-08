# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: GetPath.py
@time: 2020/5/6 6:40 下午
@description: 
"""

__all__ = ['GetPath']

from pathlib import Path

class GetPath(object):

    def project_path(self):
        return Path.cwd().parent

    def data_path(self):
        return self.project_path().joinpath('data')

if __name__ == '__main__':
    p = GetPath()
    print(p.data_path())