#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : zhihu.py
@Time   : 2020/11/8 14:31
@Author : yd
@Version: 1.0
@ToDo    : 模拟知乎登录
"""
from keywords.web import AutoWeb


class ZhiHu:

    def __init__(self):
        self.web = AutoWeb()
        self.web.start_browser()

    def login(self):
        self.web.visit_url('https://www.zhihu.com/signin')
        self.web.sleep(3)
        self.web.click('//div[text()="密码登录"]')
        self.web.input('//input[@name="username"]', '13524589524')
        self.web.sleep(1)
        self.web.input('//input[@name="password"]', '12345678')
        self.web.sleep(1)
        self.web.click('//button[text()="登录"]')
        self.web.sleep(1)

        # 知乎的验证码有多个验证方式，这里方式2无法实现
        # 1、普通数字英文验证
        # 2、点击图中倒立的字
        self.web.verify_recognition('//div[contains(text(), "//img[@alt="图形验证码"]")]')


if __name__ == '__main__':
     test = ZhiHu()
     test.login()
