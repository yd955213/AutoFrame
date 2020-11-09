#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : test_mypytest.py
@Time   : 2020/11/9 6:40
@Author : yd
@Version: 1.0
@ToDo    : 
"""
import os

import pytest


class TestMyTest:

    def setup_class(self):
        """
        测试类级别的setup
        整个测试类执行前执行一次
        :return:
        """
        print('类执行')

    def teardown_class(self):
        """
        测试类级别的teardown
        整个测试类执行后执行一次
        :return:
        """
        print("类结束")

    def teardown(self):

        """
        测试类级别的teardown
        在每一个测试用例执行前都会执行一次
        :return:
        """
        print('关闭')

    def setup(self):
        """
        测试函数级别的setup
        在每一个测试用例执行前都会执行一次
        :return:
        """
        print('初始化')

    def teardown(self):

        """
        测试函数级别的teardown
        在每一个测试用例执行后都会执行一次
        :return:
        """
        print('关闭')

    # 只在某个用例前设置前置条件或者后置条件

    @pytest.fixture()
    def before_1(self):
        """
        @pytest.fixture() 优先于函数级别的setup，别函数级别的teardown后执行
        :return:
        """
        print('某个函数开始只执行一次')

    @pytest.fixture()
    def after_1(self):
        """
        @pytest.fixture() 优先于函数级别的setup，别函数级别的teardown后执行
        :return:
        """
        print('某个函数关闭只执行一次')

    def test_1(self, before_1):
        print('pass1')

    def test_2(self):
        print('pass2')

    def test_3(self):
        print('pass3')

    def test_4(self):
        print('pass4')

    def test_5(self):
        print('pass5')


if __name__ == '__main__':
    # 使用allur 需要用
    pytest.main(["-s", "test_mypytest.py", "--alluredir", "./temp"])
    # 执行命令行，生成allure测试报告
    os.system('allure generate ./temp -o ./report --clean')



