#!/usr/bin/env python  
#-*- coding:utf-8 _*-  

""" 
@author: robert_li@riversecurity.com
@time: 2018/12/13
@description:
"""

from center import check_for_api
import json

class AiSqli():
    # read config file and init etc.
    def initialize(self):
        pass

    def predict(self, data):
        return check_for_api(json.dumps(data))

    def status(self, data):
        return 'AiSqli OK'

app = AiSqli()