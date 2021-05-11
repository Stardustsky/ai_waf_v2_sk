#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午4:25
# @Author  : Stardustsky
# @File    : m_reg.py
# @Software: PyCharm

import numpy
import time
from module.svm.svmutil import svm_predict


def attack_identify(vec, clf,return_type="probability"):
    """
    攻击识别模块
    :param para:
    :param attack_type:
    :param return_type:
    :return:
    """
    # start = time.time()
    # para = str2vec(para, regexs)
    # end = time.time()
    # print "向量化耗时:%s"%(end - start)
    if return_type == "judge":
        return clf.predict(vec)
    if return_type == "probability":
        # start = time.time()
        return clf.predict_proba(vec)
        # end = time.time()
        # print "预测耗时:%s"%(end - start)
    # if res[0] == 0:
    #     return [1.0, 0.0]
    # else:
    #     return [0.0, 1.0]


def str2vec(data, regexes):
    """
    字符串转向量
    :param data:
    :param regexes:
    :return:
    """
    vec_url = veclize(data, regexes)
    # print vec_url
    # vec_url = numpy.array(vec_url)
    # return vec_url.reshape(1, len(vec_url))
    return vec_url


def veclize(data, regexes):
    vec_url = list()
    try:
        for regex in regexes:
            if regex.search(data):
                vec_url.append(1)
            else:
                vec_url.append(0)
        return vec_url
    except:
        print("Veclize error occur")
