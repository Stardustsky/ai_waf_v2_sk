#!/usr/bin/env python
# encoding: utf-8
# from threading import Thread
# from multiprocessing import Pool, Manager
from sklearn import preprocessing
import json
import re
import urllib
import ConfigParser


def data_normalize(data, type="normalize"):
    """
    @数据预处理（独热码、正则化等处理），使数据缩放到单位范数
    :param data:
    :param type:
    :return:
    """
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


def config_parser(file):
    cf = ConfigParser.ConfigParser()
    cf.read(file)
    return cf


def log_parser(score_dict):
    """
    日志处理函数
    :param score_dict:
    :return:
    """
    for i in score_dict.keys():
        if score_dict[i][0] == 0:
            print("\033[1;32;0m [+]%s attack test:\033[0m") % i, score_dict[i]
        elif score_dict[i][0] == 1:
            print("\033[1;31;0m [+]%s attack test:\033[0m")% i, score_dict[i]


def initialize(type):
    regex_list = list()
    rules = json.load(open("module/reg_veclize/%s.json" % type))['filters']['filter']
    for i in rules:
        if i['status'] == "live":
            regex_list.append(re.compile(urllib.unquote(i['rule']), flags=re.I))
    return regex_list


def load_vec():
    """
    特征向量内容读取
    :param rule_type:
    :return:
    """
    attack_vec = dict()
    cf = ConfigParser.ConfigParser()
    cf.read("module/reg_index/vul.vec")
    common_vec = cf.get("common", "vec").split(",")
    attack_vec["sqli_high"] = cf.get("sqli_high", "vec").split(",")
    attack_vec["sqli_medium"] = cf.get("sqli_medium", "vec").split(",")
    attack_vec["sqli_low"] = cf.get("sqli_low", "vec").split(",")
    attack_vec["xss_high"] = cf.get("xss_high", "vec").split(",")
    attack_vec["xss_medium"] = cf.get("xss_medium", "vec").split(",")
    attack_vec["xss_low"] = cf.get("xss_low", "vec").split(",")
    attack_vec["rce_high"] = cf.get("rce_high", "vec").split(",")
    attack_vec["rce_medium"] = cf.get("rce_medium", "vec").split(",")
    attack_vec["rce_low"] = cf.get("rce_low", "vec").split(",")
    attack_vec["traversal_high"] = cf.get("traversal_high", "vec").split(",")
    attack_vec["traversal_medium"] = cf.get("traversal_medium", "vec").split(",")
    attack_vec["traversal_low"] = cf.get("traversal_low", "vec").split(",")
    attack_vec["php_rce_high"] = cf.get("php_rce_high", "vec").split(",")
    attack_vec["php_rce_medium"] = cf.get("php_rce_medium", "vec").split(",")
    attack_vec["php_rce_low"] = cf.get("php_rce_medium", "vec").split(",")
    attack_vec["java_rce_high"] = cf.get("php_rce_high", "vec").split(",")
    attack_vec["java_rce_medium"] = cf.get("php_rce_medium", "vec").split(",")
    attack_vec["java_rce_low"] = cf.get("php_rce_low", "vec").split(",")
    return common_vec, attack_vec


def filter_score(score):
    attck_oc = {"attack_type":"none"}
    safe_oc = {"attack_type":"none"}
    attack_value = 0
    try:
        for key, value in score.items():
            # print value
            if value[1][1] > value[1][0]:
                if value[1][1] > attack_value:
                    attack_value = value[1][1]
                    attck_oc["attack_type"] = key
                    attck_oc["probability"] = value[1].tolist()
                    attck_oc["attack_vec"] = value[-1]
                    attck_oc["libinjection"] = value[-2]
            else:
                safe_oc["probability"] = value[1].tolist()
                safe_oc["attack_vec"] = value[-1]
                safe_oc["libinjection"] = value[-2]
        if attack_value > 0:
            return attck_oc
        else:
            return safe_oc
    except Exception:
        print "Filter score error."
