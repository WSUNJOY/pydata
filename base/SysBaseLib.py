# encoding: utf-8
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: SysBaseLib.py
@time: 2020/3/18 6:28 下午
@description: 
"""
import sys
import os

class SysBaseLib(object):
    def __init__(self):
        pass
    def getClassName(self):
        return self.__class__.__name__
    def getFrameName(self):
        return sys._getframe().f_code.co_name
    def getParentPath(self):
        return os.path.abspath('..')