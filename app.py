#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 下午2:57
# @Author  : Stardustsky
# @File    : falcon-server.py
# @Software: PyCharm
import falcon
from center import check_for_api

class ThingsResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = "request error."

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200  # This is the default status
        payload = req.bounded_stream.read()
	#print payload
        res = check_for_api(payload)
        resp.body = str(res)

app = application = falcon.API()

ai_sqli = ThingsResource()

app.add_route('/ai_waf', ai_sqli)
