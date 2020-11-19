# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   interface_case.py
@Time   :   2020-11-19 10:38
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import traceback

from comm.configs import config
from comm.read_and_write_excel import Excel, MyColor
from keywords.key_word_http import KeyWordHttp


class InterfaceCase:

    def __init__(self, file_path):
        self.file_path = file_path
        self.excel = Excel()
        self.http = KeyWordHttp(self.excel)

    def run(self):
        self.excel.open_excel(self.file_path)
        sheet_name = self.excel.get_sheets()
        for sheet in sheet_name:
            # 设置当前读取的sheet页面
            self.excel.set_sheet(sheet)
            for i in range(self.excel.rows):
                cell_list = self.excel.read_line()
                # print(cell_li)
                self.http.excel_write_row = i
                self.__run_case(cell_list)
        self.excel.save()

    def __run_case(self, cell_list):
        # 第一列，第二列不执行
        if len(cell_list[int(config.get('teem'))]) > 0 or len(cell_list[int(config.get('caseName'))]) > 0:
            return
        # print('cell_list =', cell_list)
        try:
            func = getattr(self.http, cell_list[int(config.get('keyWord'))])
            li = cell_list[int(config.get('requestParamStart')): int(config.get('requestParamEnd')) + 1]
            # print('li =', li)
            func(*li)
        except:
            self.excel.write(self.http.excel_write_row, config.get('status'), 'Fail', MyColor.RED)
            self.excel.write(self.http.excel_write_row, config.get('result'), '暂不支持该关键字，请检查')
            self.excel.write(self.http.excel_write_row, config.get('remark'), 'traceback.format_exc()')
            print(traceback.format_exc())

