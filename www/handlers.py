#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: handlers.py
@time: 2020/6/2 5:35 下午
@description: 
"""


'''url handlers'''

import re, time, json, logging, hashlib, base64, asyncio

from www.coroweb import get, post
from www.models import User, Comment, Blog, next_id

@get('/test')
async def test(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'user': users
    }

@get('/')
def index(request):
    summary = 'abc'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Python', summary=summary, created_at=time.time()-4800)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }