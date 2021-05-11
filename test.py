#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 下午3:46
# @Author  : Stardustsky
# @File    : center.py
# @Software: PyCharm
from sklearn.externals import joblib
import numpy
clf = joblib.load("module/lib/sk_svm_traversal.model")
print clf.predict_proba(numpy.array([[1, 0, 1]]))