#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : summery_report.py
@Time   : 2020/11/21 11:24
@Author : yd
@Version: 1.0
@ToDo    :  对执行后的用例结果进行汇总分析
"""
from comm import configs
from comm.configs import config
from comm.read_and_write_excel import Excel
from global_abspath import get_abspath


class SummeryReport:
    
    def __init__(self, file_path):
        # 汇总信息：report_title, tester, developer, case_version, case_count, pass_rate, start_time, end_time
        self.summery_info = {}
        
        # 分组信息: group_name, group_case_count, pass_count, status
        self.group_info = []
        self.excel = Excel()
        self.excel.open_excel(get_abspath(file_path))
        self.sheets = self.excel.get_sheets()
    
    def get_summery_info(self, ):
        """
        获取用例信息
        :param file_path: 用例文件路径
        :return:
        """
        # 重新赋值
        self.summery_info.clear()
        self.summery_info['report_title'] = config.get('reportTitle')
        self.summery_info['tester'] = config.get('tester')
        self.summery_info['developer'] = config.get('developer')
        self.summery_info['case_version'] = config.get('case_version')
        self.summery_info['case_count'] = ''
        self.summery_info['pass_rate'] = ''
        self.summery_info['start_time'] = configs.time_start
        self.summery_info['end_time'] = configs.time_end
        
        case_pass_count = 0
        case_fail_count = 0
        case_block_count = 0
        for sheet in self.sheets:
            self.excel.set_sheet(sheet)
            lines = self.excel.read_lines()
            for line in lines:
                # 过滤写分组信息和用例名称的列
                if not (line[int(config.get('teem'))] == '' and line[int(config.get('caseName'))] == ''):
                    pass
                # 是一个可执行的测试用例
                elif not line[int(config.get('keyWord'))] == '':
                    
                    if line[int(config.get('status'))].upper() == 'FAIL':
                        case_fail_count += 1
                    elif line[int(config.get('status'))].upper() == 'PASS':
                        case_pass_count += 1
                    else:
                        case_block_count += 1
        
        case_count = case_fail_count + case_pass_count + case_block_count
        
        try:
            pass_rate = (int((case_pass_count * 10000) / case_count)) / 100
        except Exception as e:
            pass_rate = 0.0
        
        self.summery_info['case_count'] = case_count
        self.summery_info['pass_rate'] = pass_rate
        self.summery_info['case_fail_count'] = case_fail_count
        self.summery_info['case_pass_count'] = case_pass_count
        self.summery_info['case_block_count'] = case_block_count
        return self.summery_info
        
    def get_group_info(self):
        """
        获取分组信息
        :param file_path:
        :return:
        """
        self.group_info.clear()
        case_count = 0
        pass_count = 0
        group_smale = {}
        sign = False
        group_name = ''
        for sheet in self.sheets:
            self.excel.set_sheet(sheet)
            lines = self.excel.read_lines()
            group_smale.clear()
            for i in range(1, len(lines)):
                line = lines[i]
                if line[int(config.get('teem'))] == '' and line[int(config.get('caseName'))] == '':
                    if not line[int(config.get('keyWord'))] == '':
                        if line[int(config.get('status'))].upper() == 'PASS':
                            pass_count += 1
                        else:
                            sign = True
                        case_count += 1
                elif not line[int(config.get('teem'))] == '':
                    if i == 1:
                        group_name = line[int(config.get('teem'))]
                        pass
                    else:
                        # 分组
                        if sign:
                            status = 'FAIL'
                            sign = False
                        else:
                            status = 'PASS'
                        
                        group_smale['group_name'] = group_name
                        group_smale['case_count'] = case_count
                        group_smale['pass_count'] = pass_count
                        group_smale['fail_count'] = case_count - pass_count
                        group_smale['status'] = status
                        self.group_info.append(group_smale)
                        case_count = 0
                        pass_count = 0
                        group_smale = {}
                        sign = False
                        group_name = line[int(config.get('teem'))]
            # 完成一个sheet时，保存分组信息
            if sign:
                status = 'FAIL'
                sign = False
            else:
                status = 'PASS'

            group_smale['group_name'] = group_name
            group_smale['case_count'] = case_count
            group_smale['pass_count'] = pass_count
            group_smale['fail_count'] = case_count - pass_count
            group_smale['status'] = status
            self.group_info.append(group_smale)
            case_count = 0
            pass_count = 0
            group_smale = {}
            sign = False
        return self.group_info
        
        
if __name__ == '__main__':
    test = SummeryReport('D:\搜狗高速下载\不杀毒\HTTP接口用例.xls')
    print(test.get_summery_info())
    print(test.get_group_info())
    