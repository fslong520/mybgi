#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 字符串的一些操作 '

__author__ = 'fslong'

import pickle


def transformStr(strings, stringsMethod):
    if strings == '':
        return False
    else:
        strResult = ''
        if stringsMethod == '':
            return False
        elif stringsMethod == 'str':
            strings=strings.encode('utf-8')
            strResult = strings.decode('utf-8')
            return strResult
        elif stringsMethod == 'bytes':
            try:
                strResult = strings.encode('utf-8')
                return strResult
            except:
                return False

        elif stringsMethod == 'picking':
            try:
                strResult = pickle.dumps(strings)
                return strResult
            except:
                return False
        elif stringsMethod == 'unpicking':
            strResult = pickle.loads(strings)
            return strResult
        else:
            return False


if __name__ == "__main__":
    print(transformStr(transformStr('测试','bytes'), 'str'))
