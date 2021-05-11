#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午4:04
# @Author  : Stardustsky
# @File    : m_weighting.py
# @Software: PyCharm

from module.m_ml import attack_identify,str2vec
from module.m_regex import attack_vec_load
from sklearn import preprocessing
from module.m_libinjection import is_attack_type
import numpy
import time


def controller_center(para, attack_type, ratio, _multi_score, clf, regexes, vec, positon="url"):
    """
    :param para:
    :param attack_type:
    :param ratio:
    :param _multi_score:
    :param clf:
    :param regexes:
    :param vec:
    :param positon:
    :return:
    """
    # 获取正则匹配向量化结果
    reg_vec_list = attack_vec_load(para, attack_type, vec)
    # 获取libinjection匹配后结果
    libinjection_res = is_attack_type(para, attack_type)
    # 获取攻击特征串匹配后结果
    ml_vec_list = str2vec(para, regexes)
    vec_list = ml_vec_list + reg_vec_list
    vec_list.append(libinjection_res)
    # 调整vec_list用于模型预测
    vec_list = data_normalize(numpy.array(vec_list).reshape(1, len(vec_list)))
    attack_score = attack_identify(vec_list, clf)[0]
    # print attack_score
    if attack_score[1] > attack_score[0]:
        _multi_score[attack_type] = [1, attack_score, ml_vec_list, libinjection_res, reg_vec_list]
    else:
        _multi_score[attack_type] = [0, attack_score, ml_vec_list, libinjection_res, reg_vec_list]


def data_normalize(data, type="normalize"):
    """
    数据预处理函数
    :param data:
    :param type:
    :return:
    """
    # data=numpy.array(data,dtype=numpy.float64)
    if type == "minmax":
        normalized = preprocessing.MinMaxScaler().fit_transform(data)
    elif type == "normalize":
        normalized = preprocessing.normalize(data)
    elif type == "scale":
        normalized = preprocessing.scale(data)
    elif type == "onehot":
        enc = preprocessing.OneHotEncoder()
        normalized = enc.fit_transform(data).toarray()
    else:
        return data
    return normalized