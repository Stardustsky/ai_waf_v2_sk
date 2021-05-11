#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/6 下午4:25
# @Author  : Stardustsky
# @File    : m_reg.py
# @Software: PyCharm
import ctypes
import libinjection as lb
# libinjection = ctypes.CDLL('module/lib/libinjection_mac.so')
#
# def py_libinjection_sqli(sql):
#     """
#     #libinjection_sqli预测函数
#     :param sql:
#     :return:
#     """
#     sql_str = ctypes.c_char_p(sql)
#     sql_len = ctypes.c_int(len(sql))
#     sql_out = ctypes.create_string_buffer(256)
#     libinjection_sqli = libinjection.libinjection_sqli
#     libinjection_sqli.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]
#     isqli = libinjection_sqli(sql_str, sql_len, sql_out)
#     fingerprint = sql_out.value
#     # print "[+]sqli libinjection check over[+]"
#     return isqli
#
# def py_libinjection_xss(xss):
#     """
#     #ibinjection_xss预测函数
#     :param xss:
#     :return:
#     """
#     xss_str = ctypes.c_char_p(xss)
#     xss_len = ctypes.c_int(len(xss))
#     libinjection_xss = libinjection.libinjection_xss
#     libinjection_xss.argtypes = [ctypes.c_char_p, ctypes.c_int]
#     isxss = libinjection_xss(xss_str, xss_len)
#     # print "[+]xss libinjection check over[+]"
#     return isxss


def is_attack_type(uri, att_type):
    try:
        if att_type == "sqli":
            res = lb.is_sql_injection(uri)["is_sqli"]
            if res:
                return 1
            else:
                return 0
        elif att_type == "xss":
            res = lb.is_xss(uri)["is_xss"]
            if res:
                return 1
            else:
                return 0
        else:
            return -1
    except:
        return 0

# print is_attack_type("aaaa ","traversal")
