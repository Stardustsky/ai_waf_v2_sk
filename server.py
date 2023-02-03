#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午4:25
# @Author  : Stardustsky
# @File    : m_reg.py
# @Software: PyCharm
import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import urllib
from center import check_for_api


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        pack = self.get_query_argument("payload")
        # pack = self.request.body
        json_pack = urllib.unquote(pack)
        # print json_pack
        try:
            res = check_for_api(json_pack)
            self.write(res)
        except Exception as e:
            self.write(e)


    def post(self):
        # pack = self.get_query_argument("payload")
        pack = self.request.body
        json_pack = urllib.unquote(pack)
        try:
            res = check_for_api(json_pack)
            self.write(res)
        except Exception as e:
            self.write(e)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/svm_waf/', IndexHandler),
        ]

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False,
            "login_url": "/svm_waf/"
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    port = 9999
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()
    # http_server.bind(port)
    # http_server.start(0)
    # tornado.ioloop.IOLoop.instance().start()