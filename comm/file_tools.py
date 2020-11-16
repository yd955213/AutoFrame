# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   file_tools.py
@Time   :   2020-11-16 15:10
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :  一些对于文件的操作
"""
import json

# from comm.logger import logger
from global_path import get_abspath


class FileTools:

    def __init__(self, file_name):
        self.data_txt = []
        self.file_path = get_abspath(file_name)

    def read_config_text(self, mode='r', encoding='utf8'):
        # 清空列表
        config = {}
        with open(file=self.file_path, mode=mode, encoding=encoding) as f1:
            data_lines = f1.readlines()
            for st in data_lines:
                st = st.replace('\n', '').replace(' ', '')
                st = st.encode('utf-8').decode('utf-8-sig')
                if not st.startswith("#"):
                    if st.find("#") > 0:
                        st = st[0:st.find("#")]
                        if st.find('='):
                            try:
                                index = st.find('=')
                                config[st[0: index]] = st[index + 1:len(st)]
                            except:
                                pass
                                # logger.warn('配置文件格式错误，请检查：' + str(s))
                                # logger.exception(e)
        return config


if __name__ == '__main__':
    file = FileTools(get_abspath('./config/config.properties'))
    data = file.read_config_text()
    print(data)
