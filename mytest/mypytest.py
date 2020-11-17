# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   mypytest.py
@Time   :   2020-11-10 13:27
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   pytest 参数化
"""
import os

import pytest


def add(a, b): return a + b


pra = [
    (1, 2, 3),
    (2, 2, 5),
    (3, 3, 6),
    (1, "1", None),
    (0, 0, 0),
]


@pytest.mark.parametrize('li', pra)
def test_add(li):
    """
    参数化测试用例
    """
    z = add(li[0], li[1])
    assert z == li[2]


if __name__ == '__main__':
    pytest.main(["-s", "mypytest.py", "--alluredir", "./temp"])
    # os.system('allure generate ./temp -o ./report --clean')