# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   type_judgment.py
@Time   :   2020-11-17 9:46
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   一些常见的数据类型判断
"""


def is_dict(value):
    """
    判断是否为字典或者json
    """
    if type(value).__name__ == 'dict':
        return True
    else:
        return False


def is_string(value):
    """
    判断是否为字符串
    """
    if type(value).__name__ == 'str':
        return True
    else:
        return False


def is_int(value):
    """
    判断是否为字典
    """
    if type(value).__name__ == 'int':
        return True
    else:
        return False


def is_float(value):
    """
    判断是否为字典
    """
    if type(value).__name__ == 'float':
        return True
    else:
        return False


def is_list(value):
    """
    判断是否为字典
    """
    if type(value).__name__ == 'list':
        return True
    else:
        return False


def is_Null(value):
    """
    判断数据类型是否为空
    """
    if value is None or value.__len__ == 0:
        return True
    else:
        return False
