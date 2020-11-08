#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : jingdong.py
@Time   : 2020/11/8 0:33
@Author : yd
@Version: 1.0
@ToDo    : 京东自动登录
"""
from keywords.web import AutoWeb


class JingD:

    def __init__(self):
        self.web = AutoWeb()
        self.web.start_browser()

    def login(self):
        self.web.visit_url('https://passport.jd.com/new/login.aspx')
        #
        self.web.sleep(3)
        # self.web.into_iframe('//*[@id="login_frame"]')
        # 点击账号密码登录
        self.web.click('//*[@id="content"]/div[2]/div[1]/div/div[3]/a')
        # 输入用户名
        self.web.input('//*[@id="loginname"]', '888888')
        # 输入密码
        self.web.input('//*[@id="nloginpwd"]', '1234567')
        # 点击登录
        self.web.click('//*[@id="loginsubmit"]')

        # self.web.into_iframe('//*[@id="tcaptcha_iframe"]')
        self.web.slide_base64(slide_block_locator='//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img',
                       slide_background_locator='//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img')


if __name__ == '__main__':
    test = JingD()
    test.login()