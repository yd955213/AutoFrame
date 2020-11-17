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
import requests, traceback, json

from comm.read_and_write_excel import MyColor
from comm.type_judgment import is_dict
from run_main import config


class KeyWordHttp:
    arrow = '->'

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
        self.excel_write_row = 1;

    def set_url(self, url):
        """
        合成接口地址
        :param url:
        :return:
        """
        if url is None:
            url = 'None'
            self.__write_excel(False, '接口地址错误')
        self.url = url
        self.__write_excel(True, '')
        return True

    def post(self, path, params=None):
        """
        http post方法,以字典形式传递键值对
        :param path: 接口地址
        :param params: 参数字典
        :return: 成功或者失败
        """
        path = self.__is_ready(path, params, mode='post')

        try:
            self.response_result = self.session.post(path, data=params).text
            self.__process_response_result()
        except Exception as e:
            print(traceback.format_exc())
            self.__write_excel(False, traceback.format_exc())
            return False

    def get(self, path, params=None):
        """
        http get 方法,以字典形式传递键值对
        :param path: 接口地址
        :param params: 参数字典
        :return: 成功或者失败
        """

        path = self.__is_ready(path, params, mode='get')

        try:
            self.response_result = self.session.get(path, data=params).text
            self.__process_response_result()
        except Exception as e:
            print(traceback.format_exc())
            self.__write_excel(False, traceback.format_exc())
            return False

    def put(self, path, params=None):
        """
        http put方法，后期增加
        """
        path = self.__is_ready(path, params, mode='get')

    def delete(self, path, params=None):
        """
        http delete 方法，后期增加
        """
        path = self.__is_ready(path, params, mode='get')

    def add_header(self, key, value=None):
        """
        添加请求头
        :param key:header的键
        :param value:header的值
        :return:
        """
        value = self.__get_relations(value)
        self.session.headers[key] = value
        self.__write_excel(True,'')
        return True

    def remove_header(self, key):
        """
        从请求头删除一个键值对
        :param key: 需要删除的键
        :return: 成功失败
        """
        try:
            self.session.headers.pop(key)
            self.__write_excel(True,'')
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            pass
        return True

    def assert_equal(self, key, value):
        """
        断言json结果中某个键的值等于value
        :param key:想要断言实际返回结果的json的键
        :param value:想要断言实际返回结果的json的值
        :return:
        """
        if self.response_result is None:
            self.__write_excel(False, '断言失败,实际结果返回为空')
            return False

        if is_dict(self.response_result):
            if key in self.response_result:
                if self.response_result.get(key) == value:
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

    def assert_equal_json(self, json_string):
        """
        断言json结果中多个键的值等于value
        :param json_string:
        :return:
        """
        if self.response_result is None:
            self.__write_excel(False, '断言失败,实际结果返回为空')
            return False

        try:
            # 传入的参数不为json
            json_string = json.loads(json_string)
            self.__write_excel(True,'')
        except Exception as e:
            self.__write_excel(False, '断言失败,预期结果非json字符串：{}'.format(json_string))
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

    def assert_contains_string(self, value=None):
        """
        断言某字符串是否包含value
        :param value:
        :return:
        """
        if value is None or value == "":
            self.__write_excel(False, "断言失败,预期结果不能为空")
            return False

        if self.response_result is None:
            self.__write_excel(False, "断言失败,实际结果为空")
            return False

        # 返回结果为空时的处理
        if self.response_result.__contains__(value):
            self.__write_excel(True, "断言成功")
            return True
        else:
            self.__write_excel(False, "断言失败,实际结果不包含：{}".format(value))
            return False

    # def quit(self, user_name):
    #     """
    #     根据用户名获取token，并退出登陆
    #     :param user_name: 用户名
    #     :return:
    #     """
    #     if self.token_list.get(user_name) is not None:
    #         self.session.headers['token'] = self.token_list.get(user_name)
    #         self.post_data('/inter/HTTP/logout')
    #         self.__write_excel(True,'')
    #     else:
    #         self.__write_excel(False,"")

    def save_relations_json(self, key_name=None, relation_key_name=None):
        """
        将上一步操作返回的结果self.response_result的键对应的值，保存在self.relations中,
        :param key_name: 返回结果 self.response_result 的键
        :param relation_key_name:  关联字典self.relations 的键
        """
        if not is_dict(self.response_result):
            self.__write_excel(False, "断言失败，实际结果不是jsong格式，无法实现关联")
            return False

        if self.response_result.get(key_name) is None:
            self.__write_excel(False, "关联结果值为空，欲关联键={}".format(key_name))
            return False

        # 实现关联， 这样可以在其他关键字中通过__get__relations
        self.relation_dict[relation_key_name] = self.response_result.get(key_name)
        self.__write_excel(True, '')

    def __get_relations(self, params=None):
        """
        根据params获取关联self.relation_dict字典中的值
        :param params: 需要关联的参数，格式必须为 ->xxx ,xxx为relation_dict的键，需要保证xxx,已经使用self.save_relations_json()保存至
        self.relation_dic中
        :return: 关联后的字符串
        """
        if params is None:
            return None
        if not str(params).find(self.arrow) == -1:
            print('params = ', params)
            for key in self.relation_dict:
                params = params.replace('->' + key, str(self.relation_dict.get(key)))
        return params

    def __is_ready(self, path, params=None, mode='post'):
        """
        以字典形式传递键值对
        :param path: 接口地址
        :param params: 参数字典
        :return: 成功或者失败
        """
        if params is None or params == '':
            self.__write_excel(False, '关键字{},获取的参数为空'.format(mode))
            params = None
        else:
            # 实现关联
            self.__get_relations(params)

        if path is None or path == '':
            # 接口地址不能为空
            self.__write_excel(False, '关键字{},获取的请求url为空'.format(mode))

        if not path.startswith('http'):
            path = self.url + '/' + path
        return path

    def __process_response_result(self):
        print(self.response_result)
        try:
            # json格式处理 转义
            self.response_result = json.loads(self.response_result)
            self.__write_excel(True, self.response_result)
            return True
        except Exception as e:
            print(traceback.format_exc())
            self.__write_excel(False, self.response_result + '/n' + traceback.format_exc())
            return False

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
        p1 = params.split('&')
        for key_value in p1:
            index = key_value.find('=')
            if index >= 0:
                key = key_value[0:index]
                value = key_value[index + 1:]
                param[key] = value
            else:
                param[key_value] = None

        return param

    def __write_excel(self, status, msg, dsc=None):
        """
        写入关键字运行结果
        :param status: 运行的状态
        :param msg: 实际运行结果
        :return: 无
        """
        if status is True:
            self.excel.write(self.excel_write_row, config.get('status'), "PASS", MyColor.GREEN)
        else:
            self.excel.write(self.excel_write_row, config.get('status'), "FAIL", MyColor.RED)

        # 有时候实际结果过长，我们就只保存前30000个字符
        msg = str(msg)
        if len(msg) > 30000:
            msg = msg[0:30000]

        self.excel.write(self.excel_write_row, config.get('result'), str(msg))

        if dsc is not None or not dsc == '':
            self.excel.write(self.excel_write_row, config.get('remark'), str(dsc))
