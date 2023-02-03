#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 下午3:46
# @Author  : Stardustsky
# @File    : center.py
# @Software: PyCharm
import time
from module.m_weighting import controller_center
from tool.common import *
from module.m_urlparser import json_parser
from module.svm.svmutil import svm_load_model
from sklearn.externals import joblib
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# 攻击字段定义
_multi_score_args = dict()
_multi_score_cookie = dict()
_multi_score_body = dict()
_multi_score_referer = dict()
_multi_score_ua = dict()
_multi_score_host = dict()
_multi_score_uri = dict()

# 模型加载
CLF_PHP_RCE = joblib.load("module/lib/sk_svm_php_rce.model")
CLF_RCE = joblib.load("module/lib/sk_svm_rce.model")
CLF_SQLI = joblib.load("module/lib/sk_svm_sqli.model")
CLF_XSS = joblib.load("module/lib/sk_svm_xss.model")
CLF_TRAVERSAL = joblib.load("module/lib/sk_svm_traversal.model")
CLF_JAVA_RCE = joblib.load("module/lib/sk_svm_java_rce.model")
CLF_DICT = {"sqli": CLF_SQLI, "xss": CLF_XSS, "traversal": CLF_TRAVERSAL, "php_rce": CLF_PHP_RCE, "rce": CLF_RCE,"java_rce": CLF_JAVA_RCE}

# 判断容忍度
RATIO_DICT = {"sqli": 1.0, "xss": 1.0, "traversal": 1.0, "rce": 1.0, "php_rce": 1.0, "java_rce": 1.0}

# 启用攻击类型
OPEN_ATTACK_TYPE = ["xss", "sqli", "traversal", "php_rce", "rce", "java_rce"]

# 攻击向量加载
VEC = load_vec()

RGE_ATTACK_DICT = {
    "sqli": initialize('sqli'),
    "xss": initialize('xss'),
    "rce": initialize('rce'),
    "traversal": initialize('traversal'),
    "php_rce": initialize('php_rce'),
    "java_rce": initialize('java_rce')
}


def check_for_api(data):
    """
    :param data: 传入的json数据
    :return: 返回攻击判别结果
    """
    all_attack_score = dict()
    filter_attack_score = dict()
    # start = time.time()
    json_data = json_parser(data)
    print json_data
    # end = time.time()
    # print "Json渲染耗时:%s"%(end - start)
    for position in json_data:
        for key in OPEN_ATTACK_TYPE:
            controller_center(json_data[position],
                              key,
                              RATIO_DICT[key],
                              eval('_multi_score_' + position),
                              CLF_DICT[key],
                              RGE_ATTACK_DICT[key],
                              VEC,
                              position)
        for attack_type in OPEN_ATTACK_TYPE:
            filter_attack_score[attack_type] = eval("_multi_score_" + position)[attack_type]
        all_attack_score[position] = filter_score(filter_attack_score)
    print filter_attack_score
    return all_attack_score
    # return json.dumps(all_attack_score)


# print check_for_api('{"cookie":"------WebKitFormBoundarym2JpXGKs37B2pv41%5cx0D%5cx0AContent-Disposition: form-data; name=%5cx22csrfmiddlewaretoken%5cx22%5cx0D%5cx0A%5cx0D%5cx0AaRWVpnu2twngMHzsYNdFGMyz8S83Vz0r%5cx0D%5cx0A------WebKitFormBoundarym2JpXGKs37B2pv41%5cx0D%5cx0AContent-Disposition: form-data; name=%5cx22name%5cx22%5cx0D%5cx0A%5cx0D%5cx0A%5cx0D%5cx0A------WebKitFormBoundarym2JpXGKs37B2pv41%5cx0D%5cx0AContent-Disposition: form-data; name=%5cx22title%5cx22%5cx0D%5cx0A%5cx0D%5cx0A%5cx0D%5cx0A------WebKitFormBoundarym2JpXGKs37B2pv41%5cx0D%5cx0AContent-Disposition: form-data; name=%5cx22email%5cx22%5cx0D%5cx0A%5cx0D%5cx0A%5cx0D%5cx0A------WebKitFormBoundarym2JpXGKs37B2pv41%5cx0D%5cx0AContent-Disposition: form-data; name=%5cx22file%5cx22; filename=%5cx2217.16.1 System_Reliability_Design_Doc   SphinxWork_Products Wiki.pdf.zip%5cx22%5cx0D%5cx0AContent-Type: application/zip%5cx0D%5cx0A%5cx0D%5cx0A%PDF-1.4%5cx0A% %5cx0A1 0 obj%5cx0A<</Creator (Mozilla/5.0 %5cx5C(Macintosh; Intel Mac OS X 10_13_2%5cx5C) AppleWebKit/537.36 %5cx5C(KHTML, like Gecko%5cx5C) Chrome/74.0.3729.131 Safari/537.36)%5cx0A/Producer (Skia/PDF m74)%5cx0A/CreationDate (D:20190510071842+00%\'00%5c\')%5cx0A/ModDate (D:20190510071842+00\'00\')>>%5cx0Aendobj%5cx0A3 0 obj%5cx0A<</ca 1%5cx0A/BM /Normal>>%5cx0Aendobj%5cx0A65 0 obj%5cx0A<</CA .2%5cx0A/ca .2%5cx0A/LC 0%5cx0A/LJ 0%5cx0A/LW 1%5cx0A/ML 4%5cx0A/SA true%5cx0A/BM /Normal>>%5cx0Aendobj%5cx0A68 0 obj%5cx0A<</Type /Anno"}')
# print check_for_api('{"cookie":"/_vti_bin/owssvr.dll?ul=1&act=4&build=4518&strmver=4&capreq=0\'and\'456890\'=\'456890\'-- "}')
# print check_for_api('{"uri":"https://tensorwall-web-service.tensorsecurity.cn/vulnerabilities/sqli/?id=1%27 and 1%3D1&Submit=Submit"}')
# st = time.time()
# obj = open("black_payload.txt", "r")
# fp_obj = open("tp_payload.txt", "r+")
# files = obj.readlines()
# fp = list()
# fp_payload = list()
# # import urllibx
# for line in files:
#     line = urllib.quote(line)
#     payload = "{\"uri\":\"%s\"}"%line
#     res = check_for_api(payload)
#     # print type(res)
#     print res['uri']['attack_type']
#     if res['uri']['attack_type'] != "none":
#         fp.append(res['uri'])
#         fp_payload.append(payload)
#         out = urllib.unquote(line).strip()+"\n"
#         fp_obj.writelines(out)
# print fp
# print len(fp)
# end = time.time()
# print "Time cost %s" % (end - st)