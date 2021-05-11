#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午4:25
# @Author  : Stardustsky
# @File    : m_reg.py
# @Software: PyCharm


def attack_vec_load(url, attack_type, vec):
    """
    特征向量读取
    :param url:
    :param attack_type:
    :return:
    """
    high_risk_vec = attack_type + "_high"
    medium_risk_vec = attack_type + "_medium"
    low_risk_vec = attack_type + "_low"
    common_vec, attack_vec = vec[0], vec[1]
    # print common_vec,attack_vec
    common_vec_num = high_vec_num = medium_vec_num = low_vec_num = 0
    for i in common_vec:
        if common_vec_num < 5:
            common_vec_num = common_vec_num + url.count(i)
    for j in attack_vec[high_risk_vec]:
        if common_vec_num < 5:
            high_vec_num += url.count(j)
    for k in attack_vec[medium_risk_vec]:
        if common_vec_num < 5:
            medium_vec_num += url.count(k)
    for x in attack_vec[low_risk_vec]:
        if common_vec_num < 5:
            low_vec_num += url.count(x)
    return [common_vec_num, high_vec_num, medium_vec_num, low_vec_num]

