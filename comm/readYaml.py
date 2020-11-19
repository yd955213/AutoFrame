# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   readYaml.py
@Time   :   2020-11-10 13:54
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   读取yaml格式文件
"""
import yaml

from global_abspath import get_abspath


class ReadCasesYaml:
    """
    读取用例
    """
    def read(self, path="data/case/cases.yml"):
        with open(get_abspath(path), encoding='utf8') as f:
            return yaml.safe_load(f)


if __name__ == '__main__':
    print(ReadCasesYaml().read('../data/case/cases.yml'))
