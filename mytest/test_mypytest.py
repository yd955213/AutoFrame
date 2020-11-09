#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : test_mypytest.py
@Time   : 2020/11/9 6:40
@Author : yd
@Version: 1.0
@ToDo    : 
"""
import pytest


class TestMyTest:

    def test_1(self):
        print('pass1')

    def test_2(self):
        print('pass2')

    def test_3(self):
        print('pass3')

    def test_4(self):
        print('pass4')

    def test_5(self):
        print(int('a'))


if __name__ == '__main__':
    pytest.main(["-s", "test_mypytest.py"])



