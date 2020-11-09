#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : test_mypytest1.py
@Time   : 2020/11/10 6:06
@Author : yd
@Version: 1.0
@ToDo    : 
"""
import os

import pytest

from mytest.webtest import POTest


class TestPo:

    def setup_class(self):
        print("类执行")
        self.po_test = POTest()

    def teardown_class(self):
        print("类结束")
        self.po_test.quit()

    def test_login(self):
        print("login")
        self.po_test.long_in_ok()

    def test_logout(self):
        print("logout")
        self.po_test.logout()


if __name__ == '__main__':
    # 使用allure 需要自行下载安装allure
    pytest.main(["-s", "test_mypytest1.py", "--alluredir", "./temp"])
    # 执行命令行，生成allure测试报告
    os.system('allure generate ./temp -o ./report --clean')
