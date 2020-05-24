#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@version: 1.0
@author: sunjoy
@software: PyCharm
@file: app.py
@time: 2020/5/18 7:02 下午
@description: 
"""

import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web


def index(request):
    return web.Response(body='<h1>Awesome</h1>',
                        headers={'content-type': 'text/html'})


# @asyncio.coroutine
# def init(loop):
#     app = web.Application(loop=loop)
#     app.router.add_route('GET', '/', index)
#     srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
#     logging.info('server started at http://127.0.0.1:9000')
#     return srv

# --------new way line---------
async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

# --------new way line---------
# def init():
#     app = web.Application()
#     app.router.add_route('GET', '/', index)
#     logging.info('server started at http://127.0.0.1:9000')
#     web.run_app(app, host='127.0.0.1', port=9000)
#
# if __name__ == '__main__':
#     init()
