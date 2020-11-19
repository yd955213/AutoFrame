# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   configs.py
@Time   :   2020-11-19 12:38
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   存放全局参数
"""
from comm.file_tools import FileTools
from global_abspath import get_abspath

config = FileTools(get_abspath('./config/config.properties')).read_config_text()
print('config = ', config)
