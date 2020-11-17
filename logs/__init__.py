#!/usr/bin/env python
# _*_ encoding: UTF-8 _*_

"""
@File   : __init__.py.py
@Time   : 2020/11/7 3:46
@Author : yd
@Version: 1.0
@ToDo    : 日志文件存放位置
"""


dic = {'name': '点击登录', 'method': 'click', 'locator': '//*[@id="loginform"]/div/div[6]/a','name1': '点击登录', 'method1': 'click', 'locator1': '//*[@id="loginform"]/div/div[6]/a'}
li = list(dic.values())
# print(dic.values())
# print(list(dic.values()))
print(li)
print(li[:-1])
