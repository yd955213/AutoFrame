# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   httpPo.py
@Time   :   2020-11-17 11:05
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   使用关联完成http PO模式用例
"""
import inspect
import traceback

from comm.read_and_write_excel import Excel
from keywords.key_word_http import KeyWordHttp


# http = KeyWordHttp()
# http.set_url('http://www.testingedu.com.cn:8081')
#
# # 获取token
# http.post('inter/HTTP/auth')
# print(http.relation_dict)
# http.save_relations_json('token', 'my_token')
# print(http.relation_dict)
#
# # 添加信息头文件
# print(http.session.headers)
# # http.add_header('token', http.response_result.get('token'))
# http.add_header('token', '->my_token')
# print(http.session.headers)
# # http.post('HTTP//register')
#
# userinfor = {assertequals
#     'username': 'yd123',
#     'password': '123456'
# }
# http.post('inter/HTTP/login', userinfor)
# http.assert_equal('status', 200)
# http.save_relations_json('userid', 'userid')
# http.post('inter/HTTP/logout', '->userid')
#
# http.assert_equal('status', 200)


def getfunc(obj, method):
    """
    反射获取关键字执行的参数
    """
    func = getattr(obj, method)
    arg = inspect.getfullargspec(func).__str__()
    arg = arg[arg.find('args=') + 5: arg.find(', varargs=None')]
    arg = eval(arg)
    arg.remove('self')
    return func, len(arg)


def run_case(keywords, cell_list):
    # 第一列，第二列不执行
    if len(cell_list[0]) > 0 or len(cell_list[1]) > 0:
        return
    print('cell_list =', cell_list)
    try:
        func = getfunc(keywords, cell_list[3])
        if func[1] == 0:
            func[0]()
        elif func[1] == 1:
            func[0](cell_list[4])
        elif func[1] == 2:
            func[0](cell_list[4], cell_list[5])
        elif func[1] == 2:
            func[0](cell_list[4], cell_list[5], cell_list[6])
        else:
            print('不支持')
    except:
        print(traceback.format_exc())


if __name__ == '__main__':

    excel = Excel()
    http = KeyWordHttp(excel)
    excel.open_excel(r'data\case\HTTP接口用例.xls')
    sheetname = excel.get_sheets()
    for sheet in sheetname:
        # 设置当前读取的sheet页面
        excel.set_sheet(sheet)
        for i in range(excel.rows):
            cell_li = excel.read_line()
            # print(cell_li)
            http.excel_write_row = i+1
            run_case(http, cell_li)
    excel.save()

