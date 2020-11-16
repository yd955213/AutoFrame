# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   global_path.py
@Time   :   2020-11-12 9:32
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :  获取项目路径，该文件只能放在项目的根路径下
"""
import os


def get_abspath(path):
    """
    合成绝对路径:输入文件名或者相对路径，路径错误返回None
    """
    if os.path.exists(path):
        return os.path.abspath(path)
    else:
        path = os.path.abspath(os.path.dirname(__file__) + os.sep + path)
        if os.path.exists(path):
            return path
        else:
            return None
