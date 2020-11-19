# !/uer/bin/env python
# _*_ encoding: utf-8 _*_
"""
@File   :   key_word_http.py
@Time   :   2020-11-03 15:45
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   接口关键字封装
"""
import os

import requests, traceback, json

from comm.configs import config
from comm.read_and_write_excel import MyColor
from comm.type_judgment import is_dict, is_string, is_Null, is_None_in_list


class KeyWordHttp:
    # 关联字典拆分字符串
    arrow = '->'
    r_arrow = '<-'

    def __init__(self, excel):
        # 创建session管理
        self.session = requests.session()
        # 接口请求地址
        self.url = ''
        self.response = None
        # 请求结果,如果返回json字符串，处理为字典，否则为字符串
        self.response_result = None
        # 用于关联关键字之间的结果，用于业务场景测试
        self.relation_dict = {}
        self.excel = excel
        self.excel_write_row = 0
        self.path = None
        self.parameter = None

    def set_url(self, *args):
        """
        合成接口地址
        :return:
        """
        if is_None_in_list(args):
            args[0] = 'None'
            self.__write_excel(False, '接口地址错误')
        self.url = args[0]
        self.__write_excel(True, '')
        return True

    def post(self, *args):
        """
        http post方法,以字典形式传递键值对
        :return: 成功或者失败
        """
        if is_None_in_list(args):
            self.__write_excel(False, '传入参数为空')
            return False

        args = self.__is_ready(*args)
        params = args[1]
        if not is_dict(params):
            params = params.encode('utf8')
        try:
            self.response_result = self.session.post(args[0], data=params).text
            self.__write_excel(True,
                               '请求url:' + str(self.path) + '\r\n' + '\r\n' +
                               '请求参数：' + str(self.parameter) + '\r\n' + '\r\n' +
                               '返回结果：' + self.response_result)
        except Exception as e:
            print(traceback.format_exc())
            self.__write_excel(False,
                               '请求url:' + str(self.path) + '\r\n' + '\r\n' +
                               '请求参数：' + str(self.parameter) + '\r\n' + '\r\n' +
                               '返回结果：' + str(self.response_result) + '\r\n' + '\r\n' +
                               '异常信息：' + traceback.format_exc())
            self.response_result = None
            return False

        if self.response_result is None:
            return False
        else:
            self.__process_response_result()
            return True

    def get(self, *args):
        """
        http get 方法,以字典形式传递键值对
        :return: 成功或者失败
        """

        if is_None_in_list(args):
            self.__write_excel(False, '传入参数为空')
            return False

        args = self.__is_ready(*args)
        params = args[1]
        if not is_dict(params):
            params = params.encode('utf8')

        try:
            self.response_result = self.session.get(args[0], data=params).text
            self.__write_excel(True,
                               '请求url:' + str(self.path) + '\r\n' + '\r\n' +
                               '请求参数：' + str(self.parameter) + '\r\n' + '\r\n' +
                               '返回结果：' + self.response_result)
        except Exception as e:
            print(traceback.format_exc())
            self.__write_excel(False,
                               '请求url:' + str(self.path) + '\r\n' + '\r\n' +
                               '请求参数：' + str(self.parameter) + '\r\n' + '\r\n' +
                               '返回结果：' + str(self.response_result) + '\r\n' + '\r\n' +
                               '异常信息：' + traceback.format_exc())
            self.response_result = None
            return False

        if self.response_result is not None:
            self.__process_response_result()

    def put(self, *args):
        """
        http put方法，后期增加
        """
        pass

    def delete(self, *args):
        """
        http delete 方法，后期增加
        """
        pass

    def add_header(self, *args):
        """
        添加请求头
        :return:
        """
        if is_None_in_list(args):
            self.__write_excel(False, '传入参数为空')
            return False

        val = self.__get_relations(args[1])
        self.session.headers[args[0]] = val
        self.__write_excel(True, self.session.headers)
        return True

    def remove_header(self, *args):
        """
        从请求头删除一个键值对
        """
        try:
            self.session.headers.pop(args[0])
            self.__write_excel(True, self.session.headers)
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            pass
        return True

    def assert_equal(self, *args):
        """
        断言json结果中某个键的值等于某个值
        :return:
        """

        if is_None_in_list(args):
            self.__write_excel(False, '传入参数为空')
            return False

        key = args[0]
        value = args[1]
        if value.find(self.arrow) >= 0:
            value = self.__get_relations(value)

        if self.response_result is None:
            self.__write_excel(False, '断言失败,实际结果返回为空')
            return False

        if is_dict(self.response_result):
            if key in self.response_result:
                if str(self.response_result.get(key)) == str(value):
                    self.__write_excel(True, "断言成功")
                    return True
                else:
                    self.__write_excel(False, "断言失败,键{}的值为{}不等于{}".format(key, self.response_result.get(key), value))
                    return False
            else:
                self.__write_excel(False, '断言失败，结果中无键值:{}'.format(key))
        else:
            self.__write_excel(False, '断言失败,实际结果为字符串，无法断言json')
            return False

    def assert_equal_json(self, *args):
        """
        断言json结果中多个键的值等于value
        :return:
        """
        if is_None_in_list(args):
            self.__write_excel(False, '传入参数为空')
            return False

        if self.response_result is None:
            self.__write_excel(False, '断言失败,实际结果返回为空')
            return False

        try:
            # 传入的参数不为json
            json_string = json.loads(args[0])
            self.__write_excel(True, '')
        except Exception as e:
            self.__write_excel(False, '断言失败,预期结果非json字符串：{}'.format(args[1]))
            return False

        try:
            json_dic = {}
            response_dic = {}
            for key in json_string.keys():
                # 这是只判断字符串，如’1‘==1，认为是相等的，如要判断类型，去掉str()
                if str(json_string.get(key)) != str(self.response_result.get(key)):
                    json_dic[key] = json_string.get(key)
                    response_dic[key] = self.response_result.get(key)
            else:
                if len(json_dic.keys()) == 0:
                    self.__write_excel(True, self.response_result)
                    return True
                else:
                    self.__write_excel(False, '断言失败：预期结果值{}，实际结果值{}'.format(str(json.dumps(json_dic))),
                                       str(json.dumps(response_dic)))
                    return False
        except Exception as e:
            self.__write_excel(False, '断言失败：{}'.format(traceback.format_exc()))
            return False

    def assert_contains_string(self, *args):
        """
        断言某字符串是否包含某个值
        :return:
        """
        if is_None_in_list(args):
            self.__write_excel(False, "断言失败,预期结果不能为空")
            return False

        if self.response_result is None:
            self.__write_excel(False, "断言失败,实际结果为空")
            return False

        value = args[0]
        if value.find(self.arrow) >= 0:
            value = self.__get_relations(value)

        # 返回结果为空时的处理
        if self.response_result.__contains__(value):
            self.__write_excel(True, "断言成功")
            return True
        else:
            self.__write_excel(False, "断言失败,实际结果不包含：{}".format(value))
            return False

    def save_relations_json(self, *args):
        """
        保存管理字典的值
        """
        if not is_dict(self.response_result):
            self.__write_excel(False, "断言失败，实际结果不是jsong格式，无法实现关联")
            return False

        if self.response_result.get(args[0]) is None:
            self.__write_excel(False, "关联结果值为空，欲关联键={}".format(args[0]))
            return False

        # 实现关联， 这样可以在其他关键字中通过__get__relations
        self.relation_dict[args[1]] = self.response_result.get(args[0])
        self.__write_excel(True, self.relation_dict)

    def __get_relations(self, params=None):
        """
        根据params获取关联self.relation_dict字典中的值 格式必须为:->xxx<-
        :return: 关联后的字符串
        """
        if params is None:
            return None
        if not str(params).find(self.arrow) == -1:
            for key in self.relation_dict:
                params = params.replace(self.arrow + key + self.r_arrow, str(self.relation_dict.get(key)))
        return params

    def __is_ready(self, *args, mode='post'):
        """
        以字典形式传递键值对
        :return: 成功或者失败
        """
        parm = ''
        if len(args) > 1:
            li = list(args[1:])
            if is_None_in_list(li):
                self.__write_excel(status='', dsc='关键字{},请求参数为空'.format(mode))
            else:
                # 实现关联
                li[0] = self.__get_relations(li[0])

        if is_Null(args[0]):
            self.__write_excel(False, '关键字{},请求url为空'.format(mode))

        if not args[0].startswith('http'):
            self.path = self.url + '/' + args[0]
        else:
            self.path = args[0]

        self.parameter = self.__get_data(li[0])

        return self.path, self.parameter

    def __process_response_result(self):
        try:
            # json格式处理 转义
            self.response_result = json.loads(self.response_result)
            self.__write_excel(status='', msg='', dsc='结果为json,请使用 assert_equal、assert_equal_json 断言')
            # return True
        except Exception as e:
            self.__write_excel(status='', msg='', dsc='结果为字符串,请使用 assert_contains_string() 断言')

            # return False

    def __get_data(self, params):
        """
        url参数转字典
        :param params: 需要转字典的参数
        :return: 转换后的字典
        """
        if params is None:
            return None

        # 定义一个字典，用来保存转换后的参数
        param = {}
        if params.find('&') >= 0 or params.find('=') >= 0:
            p1 = params.split('&')
            for key_value in p1:
                index = key_value.find('=')
                if index >= 0:
                    key = key_value[0:index]
                    value = key_value[index + 1:]
                    param[key] = value
                else:
                    param[key_value] = None
        else:
            param = params

        return param

    def __write_excel(self, status=False, msg='', dsc=''):
        """
        写入关键字运行结果
        :param status: 运行的状态
        :param msg: 实际运行结果
        :param dsc: 备注信息
        :return: 无
        """
        if status is True:
            self.excel.write(row=self.excel_write_row, column=config.get('status'), value="PASS", color=MyColor.GREEN)
        elif status is False:
            self.excel.write(row=self.excel_write_row, column=config.get('status'), value="FAIL", color=MyColor.RED)

        if not is_Null(msg):
            # 有时候实际结果过长，我们就只保存前30000个字符
            msg = str(msg)
            if len(msg) > 30000:
                msg = msg[0:30000]
            self.excel.write(row=self.excel_write_row, column=config.get('result'), value=str(msg))

        try:
            if not is_Null(dsc):
                self.excel.write(row=self.excel_write_row, column=config.get('remark'), value=str(dsc))
        except:
            pass
