#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/7 下午4:23
# @Author  : Stardustsky
# @File    : m_urlparser.py
# @Software: PyCharm

import urlparse
import HTMLParser
import json
import re


re_html_hex_10 = re.compile("&#[0-9]{2,5};")
re_html_hex_16 = re.compile("&#x[0-9a-z]{2,4};")
re_js_unicode = re.compile("\\u00[0-9a-z]{2,4}")


def parser_url(url):
    """
    url处理模块
    :param url:
    :return:
    """
    para = urlparse.urlparse(url).query.lower()
    para = urlparse.unquote(para)
    para = complex_decode(para)
    return para


def parser_other(data):
    """
    其它字段处理模块
    :param data:
    :return:
    """
    data = urlparse.unquote(data).lower()
    data = complex_decode(data)
    return data


def json_parser(data):
    data = json.loads(data, object_hook=_decode_dict)
    for i in data.keys():
        if i == "url":
            data[i] = parser_url(data[i])
        else:
            data[i] = parser_other(data[i])
    return data


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def complex_decode(data):
    h = HTMLParser.HTMLParser()
    try:
        # 提供html实体化编码解码
        if re_html_hex_10.findall(data) or re_html_hex_16.findall(data):
            data = h.unescape(data)
        # 提供js unicode解码
        if re_js_unicode.findall(data):
            data = data.decode("unicode-escape")
        return data
    except:
        return data

