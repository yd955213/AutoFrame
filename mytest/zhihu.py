#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : zhihu.py
@Time   : 2020/11/8 14:31
@Author : yd
@Version: 1.0
@ToDo    : 模拟知乎登录
"""
# from keywords.web import AutoWeb
# from keywords.web import AutoWeb
import sys

from global_path import get_global_path


class ZhiHu:

    def __init__(self):
        # self.web = AutoWeb()
        # self.web.start_browser()
        pass

    # def login(self):
        # self.web.visit_url('https://www.zhihu.com/signin')
        # self.web.sleep(3)
        # self.web.click('//div[text()="密码登录"]')
        # self.web.input('//input[@name="username"]', '13524589524')
        # self.web.sleep(1)
        # self.web.input('//input[@name="password"]', '12345678')
        # self.web.sleep(1)
        # self.web.click('//button[text()="登录"]')
        # self.web.sleep(1)
        #
        # # 知乎的验证码有多个验证方式，这里方式2无法实现
        # # 1、普通数字英文验证
        # # 2、点击图中倒立的字
        # self.web.verify_recognition('//div[contains(text(), "//img[@alt="图形验证码"]")]')
    def haha(self):
        print("哈哈")


if __name__ == '__main__':
     # # test = ZhiHu()
     # # test.login()
     # dic = [{'name': '打开登录页', 'method': 'visit_url',
     #         'url': 'http://testingedu.com.cn:8000/index.php/Home/user/login.html'},
     #        {'name': '输入用户名', 'method': 'input', 'locator': '//*[@id="username"]', 'value': 13800138006},
     #        {'name': '输入密码', 'method': 'input', 'locator': '//*[@id="password"]', 'value': 123456},
     #        {'name': '输入验证码', 'method': 'input', 'locator': '//*[@id="verify_code"]', 'value': 111111},
     #        {'name': '点击登录', 'method': 'click', 'locator': '//*[@id="loginform"]/div/div[6]/a'}]
     # dic = {'name': '打开登录页', 'method': 'visit_url', 'url': 'http://testingedu.com.cn:8000/index.php/Home/user/login.html'}
     # li = list(dic.values())[2:]
     # print(li)
     # # print(list(li))
     # # print(list(li)[2:])
     # # print(list(li)[:-2])
     # print(dic.get('name'))
     # print(get_global_path('zhihu.py'))
     # print(get_global_path('\\zhihu.py'))
     #
     # print(get_global_path('/zhihu.py'))
     # print(get_global_path('./zhihu.py'))
     # print(get_global_path('mytest/zhihu.py'))
     # print(assert 3 is None)
     # print(sys.platform)
     test = ZhiHu()

     print(getattr(test, 'haha'))