#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : __init__.py.py
@Time   : 2020/11/7 3:48
@Author : yd
@Version: 1.0
@ToDo    : 一些测试脚本
"""
dic = {'name': '打开登录页', 'method': 'visit_url', 'url': 'http://testingedu.com.cn:8000/index.php/Home/user/login.html'}
print(dic.values())
li = list(dic.values())
print(li)
print(li[2:])