# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   test_fixture.py
@Time   :   2020-11-12 14:27
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import pytest


# @pytest.fixture(scope='function', params=None, autouse=None, ids=None, name=None)
# def test():
#     print('fixture初始化参数列表')
# @pytest.fixture
# def login():
#     print('输入账号、密码登陆')
#
#
# @pytest.fixture
# def login2():
#     print('---输入账号、密码登陆---')
#
#
# @pytest.fixture(autouse=True)
# def login3():
#     print("-----auto-------")
#
#
# def test_s1(login):
#     print("用例 1：登录之后其它动作 111")
#
#
# def test_s3(login2, login):
#     print("用例 2：不需要登录，操作 222")
#
#
# def test_s2():
#     print("用例 2：不需要登录，操作 222")
#
#
# # 不是test开头，加了装饰器也不会执行fixture
# @pytest.mark.usefixtures("login2")
# def loginss():
#     print(123)
#
# #
# # if __name__ == '__main__':
# #     pytest.main(['-s', 'test_fixture.py::test_s3'])


@pytest.fixture(scope="session")
def open():
    # 会话前置操作setup
    print("===打开浏览器===")
    test = "测试变量是否返回"
    yield test
    # 会话后置操作teardown
    print("==关闭浏览器==")


@pytest.fixture
def login(open):
    # 方法级别前置操作setup
    print(f"输入账号，密码先登录{open}")
    name = "==我是账号=="
    pwd = "==我是密码=="
    age = "==我是年龄=="
    # 返回变量
    yield name, pwd, age
    # 方法级别后置操作teardown
    print("登录成功")


def test_s1(login):
    print("==用例1==")
    # 返回的是一个元组
    print(login)
    # 分别赋值给不同变量
    name, pwd, age = login
    print(name, pwd, age)
    assert "账号" in name
    assert "密码" in pwd
    assert "年龄" in age


def test_s2(login):
    print("==用例2==")
    print(login)
