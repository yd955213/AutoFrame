#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : qqmaillogin.py
@Time   : 2020/11/7 21:18
@Author : yd
@Version: 1.0
@ToDo    : 自动化完成qq邮箱登录
"""
from keywords.web import AutoWeb


class QqMail:

    def __init__(self):
        self.web = AutoWeb()
        self.web.start_browser()

    def login(self):
        self.web.visit_url('https://mail.qq.com')
        self.web.sleep(3)
        self.web.into_iframe('//*[@id="login_frame"]')
        # 点击账号密码登录
        self.web.click('//*[@id="switcher_plogin"]')
        # 输入用户名
        self.web.input('//*[@id="u"]', '888888')
        # 输入密码
        self.web.input('//*[@id="p"]', '1234567')
        # 点击登录
        self.web.click('//*[@id="login_button"]')

        self.web.into_iframe('//*[@id="tcaptcha_iframe"]')
        self.web.slide_url(slide_background_locator='//img[@id="slideBg"]',
                           slide_block_locator='//img[@id="slideBlock"]')


if __name__ == '__main__':
    test = QqMail()
    test.login()
