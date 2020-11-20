# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   result.py
@Time   :   2020-11-20 13:54
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   分析接口测试后生成Excel表格，并统计结果
"""
from comm import configs
from comm.configs import config
from comm.read_and_write_excel import Excel


class Result:
    def __init__(self):
        # 用于记录所有模块分组信息名称
        self.sumarry = {}
        # 统计分组信息
        self.groups = []

    def get_res(self, result_path):
        # 用于记录执行结果，逻辑为，只要分组中出现一个失败用例，则认为该分组执行失败，与flag联合使用。
        self.sumarry.clear()
        status = "FAIL"
        # 标识是否有失败
        flag = True
        # 统计测试用例集的用例总条数
        totalcount = 0
        # 统计所有用例中通过用例的条数数
        totalpass = 0

        excel = Excel()
        excel.open_excel(result_path)
        excel.set_sheet(excel.get_sheets()[0])
        lines = excel.read_lines()
        self.sumarry['runtype'] = lines[1][1]
        self.sumarry['title'] = lines[1][2]
        self.sumarry['starttime'] = configs.time_start
        self.sumarry['endtime'] = configs.time_end
        # 获取所有sheet页面
        for n in excel.get_sheets():
            # logger.info(n)
            # 从第一个页面开始解析
            excel.set_sheet(n)
            # 获取sheet的行数，用来遍历
            row = excel.rows
            # 设置从第二行开始读
            excel.r = 1

            # 遍历sheet里面所有用例
            lines = excel.read_lines()

            for i in range(1, row):
                line = lines[i]
                # logger.info(line)
                # 查找记录了分组信息的行
                # 如果第一列（分组信息）和第二列（类别或用例名）不同时为空,则不是用例，执行非用例的操作
                if not (line[0] == '' and line[1] == ''):
                    pass

                # 非用例行判断结束
                # 第一列信息和第二列信息均为空的行，即用例行，这时开始进行用例数、通过数、状态的统计。
                else:
                    # 判断执行结果列，如果为空，将flag置为false,视为该行有误，不纳入用例数量计算
                    if len(line) < 8 or line[7] == '':
                        flag = False
                    # 执行结果不为空，则将用例统计数自增
                    else:
                        totalcount = totalcount + 1
                        # logger.info(line)
                        # 如果通过，则通过数和总通过数均自增
                        if line[7] == "PASS":
                            totalpass += 1
                        else:
                            # 出现了用例执行结果不是PASS的情况，则视为当前分组执行失败。
                            flag = False
            # for循环结束

        # 所有用例执行概况
        # logger.info(totalpass)
        # 计算执行通过率
        if flag:
            status = "PASS"

        # 计算通过率
        try:
            p = int(totalpass * 10000 / totalcount)
            passrate = p / 100
        except Exception as e:
            passrate = 0.0

        # 用例总数
        self.sumarry["casecount"] = str(totalcount)
        # 通过率
        self.sumarry["passrate"] = str(passrate)
        self.sumarry['status'] = status
        # logger.info(self.sumarry)
        return self.sumarry

    def get_groups(self, result_path):
        # 用于记录执行结果，逻辑为，只要分组中出现一个失败用例，则认为该分组执行失败，与flag联合使用。
        self.groups.clear()
        # 每一个分组统计信息为列表
        groupinfo = []
        status = "FAIL"
        # 标识是否有失败
        flag = True

        # 统计每一个分组的用例总条数
        totalcount = 0
        # 统计分组用例中通过用例的条数数
        totalpass = 0

        excel = Excel()
        excel.open_excel(result_path)
        # 获取所有sheet页面
        for n in excel.get_sheets():
            # logger.info(n)
            # 从第一个页面开始解析
            excel.set_sheet(n)
            # 获取sheet的行数，用来遍历
            row = excel.rows
            # 设置从第二行开始读
            excel.r = 1

            # 标识一个分组是否统计完
            gflag = True

            # 遍历sheet里面所有用例
            lines = excel.read_lines()

            for i in range(1, row):
                # 查找记录了分组信息的行
                # 如果第一列（分组信息）
                line = lines[i]
                if not line[0] == '':
                    # 先保存上一步信息
                    # 如果不是sheet最开始，就保存上一个分组统计的全部信息
                    if not gflag:
                        if flag:
                            status = 'PASS'
                        else:
                            status = 'FAIL'
                        groupinfo.append(totalcount)
                        groupinfo.append(totalpass)
                        groupinfo.append(status)
                        self.groups.append(groupinfo)

                        # 重置下一个分组的统计信息
                        # 每一个分组统计信息为列表
                        groupinfo = []
                        status = "FAIL"
                        # 标识是否有失败
                        flag = True

                        # 统计每一个分组的用例总条数
                        totalcount = 0
                        # 统计分组用例中通过用例的条数数
                        totalpass = 0

                    # 保存分组名字
                    groupinfo.append(line[0])

                    # 表示当前分组未统计完
                    gflag = False
                # 第二列（类别或用例名）不同时为空,则不是用例，执行非用例的操作
                elif not line[1] == '':
                    # 不做统计
                    pass

                # 非用例行判断结束
                # 第一列信息和第二列信息均为空的行，即用例行，这时开始进行用例数、通过数、状态的统计。
                else:
                    # 判断执行结果列，如果为空，将flag置为false,视为该行有误，不纳入用例数量计算
                    if len(line) < 7 or line[7] == '':
                        flag = False
                    # 执行结果不为空，则将用例统计数自增
                    else:
                        totalcount = totalcount + 1
                        # logger.info(line)
                        # 如果通过，则通过数和总通过数均自增
                        if line[7] == "PASS":
                            totalpass += 1
                        else:
                            # 出现了用例执行结果不是PASS的情况，则视为当前分组执行失败。
                            flag = False

            # 当一个sheet统计完成后，保存上一次统计的结果
            if flag:
                status = 'FAIL'
            else:
                status = 'FAIL'

            if len(groupinfo) == 0:
                groupinfo.append('用例数据错误')
            groupinfo.append(totalcount)
            groupinfo.append(totalpass)
            groupinfo.append(status)
            self.groups.append(groupinfo)

            # 重置下一个分组的统计信息
            # 每一个分组统计信息为列表
            groupinfo = []
            status = "FAIL"
            # 标识是否有失败
            flag = True

            # 统计每一个分组的用例总条数
            totalcount = 0
            # 统计分组用例中通过用例的条数数
            totalpass = 0

        return self.groups


if __name__ == '__main__':
    res = Result()
    s = res.get_res('../data/case/result_HTTP接口用例.xls')
    print(s)
    r = res.get_groups('../data/case/result_HTTP接口用例.xls')
    print(r)