# # !/uer/bin/env python
# # -*- coding: utf-8 -*-
# """
# @File   :   test_mypytest3.py
# @Time   :   2020-11-11 15:50
# @Author :   yang_dang
# @Contact    :   664720125@qq.com
# @Version    :   1.0
# @Description   :
# """
# import pytest
#
#
# def add(a, b):
#     try:
#         z = a + b
#     except:
#         z =None
#     return z
#
#
# class Test_Case:
#     li = [
#         (1, 2, 3),
#         (0, 2, 3),
#         (1, -1, 0),
#         (11, 12, 23),
#         (1, 2, None),
#         (1, '2', None),
#         (1, '2', 3),
#     ]
#
#     @pytest.mark.xfail(raises=TypeError)
#     @pytest.mark.parametrize('param', li)
#     def test_add(self, param):
#         z = add(param[0], param[1])
#         assert z == param[2], "判断%s, %s 的和是否为%s?" % (param[0], param[1], param[2])
#
#
# if __name__ == '__main__':
#     # pytest.main(["-A", "test_mypytest3.py"])
#     # pytest.main(["-rfs" "mytest/test_mypytest3.py"])

# @pytest.fixture()
# def user():
#     print("获取用户名")
#     a = "yygirl"
#     assert a == "yygirl123"
#     return a
#
#
# def test_1(user):
#     assert user == "yygirl"
import pytest


@pytest.mark.weibo
def test_weibo():
    print("测试微博")


@pytest.mark.toutiao
def test_toutiao():
    print("测试头条")


@pytest.mark.toutiao
def test_toutiao1():
    print("再次测试头条")


@pytest.mark.xinlang
class TestClass:
    def test_method(self):
        print("测试新浪")


def testnoMark():
    print("没有标记测试")


if __name__ == '__main__':
    pytest.main(['-s', '-m xinlang', 'test_mypytest3.py'])
