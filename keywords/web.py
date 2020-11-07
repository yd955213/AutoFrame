#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : web.py
@Time   : 2020/11/7 3:54
@Author : yd
@Version: 1.0
@ToDo    : 封装web自动化关键字
"""
import time
import traceback
from selenium import webdriver


class AutoWeb:
    """
    封装web自动化关键字
    自动化测试时，禁止频繁启动停止浏览器
    原因：启动很慢，运行也比较慢，不过，启动之后Webdriver的操作速度虽然不快但还是可以接受的
    """

    def __init__(self):
        self.drive = None
        self.element = None

    def start_browser(self, browser='chrome'):
        """
        启动浏览器：支持chrome、firefox、ie（IE兼容性不好，坑很多）
        自动化测试时，禁止频繁启动停止浏览器
        原因：启动很慢，运行也比较慢，不过，启动之后Webdriver的操作速度虽然不快但还是可以接受的
        :param browser:chrome、firefox、ie
        :return:
        """
        # 启动火狐浏览器
        if browser == 'firefox':
            self.drive = webdriver.Firefox()
            # 启动IE浏览器
        elif browser == 'ie':
            self.drive = webdriver.Ie()
        else:
            # 默认打开chrome浏览器，其自动化测试兼容好
            self.drive = webdriver.Chrome()

        self.maximize()
        self.drive.implicitly_wait(10)
        return True

    def maximize(self):
        """
        最大化浏览器
        :return:
        """
        try:
            self.drive.maximize_window()
        except:
            traceback.format_exc()
            print('最大化浏览器失败')

    # def set_window_size(self, x, y, width, height):
    #     """
    #     设置浏览器窗口模式大小
    #     :param x:
    #     :param y:
    #     :param width:
    #     :param height:
    #     :return:
    #     """
    #     try:
    #         self.drive.set
    #     except:

    def visit_url(self, url='None'):
        """
        访问被测页面
        :param url:
        :return:
        """
        try:
            self.drive.get(url)
        except:
            traceback.format_exc()
            print('访问页面失败')

    def input(self, locator='None', content='None'):
        """
        找到元素后，并输入文本内容
        :param locator: 定位器
        :param content: 输入文本内容
        :return: 是否输入成功
        """
        try:
            element = self.__locator_element(locator=locator)
            element.send_keys(str(content))
            return True
        except:
            traceback.format_exc()
            print('元素未找到或者输入失败')
            return False

    def click(self, locator):
        """
        找到元素，并点击
        :param locator: 定位器
        :return: 是否点击成功
        """
        try:
            element = self.__locator_element(locator=locator)
            element.click()
            return True
        except Exception:
            traceback.format_exc()
            print('元素未找到或者点击失败')
            return False

    def js_click(self, locator):
        """
        找到元素，并点击
        :param locator: 定位器
        :return: 是否点击成功
        """
        try:
            element = self.__locator_element(locator=locator)
            self.drive.execute_script("$(arguments[0]).click()", element)
            return True
        except:
            print('元素未找到或者点击失败')
            return False

    def switch_window(self, index='0'):
        """
        切换窗口
        :param index:需要切换到的窗口序号
        :return:是否切换成功
        """
        try:
            # 将输入的index转化为字符串
            index = int(index)
            # 获取当前页面有多少个窗口选项
            handle = self.drive.window_handles
            # 切换
            self.drive.switch_to.window(handle[index])
            return True
        except:
            traceback.format_exc()
            print('窗口切换失败，需切换的窗口序号%s' % index)
            return False

    def into_iframe(self, locator='None'):
        """
        进入iframe
        :param locator: 定位器
        :return: 是否进入成功
        """
        try:
            element = self.__locator_element(locator=locator)
            # self.drive.switch_to_frame(element)   # 已过时
            self.drive.switch_to.frame(element)
        except:
            traceback.format_exc()
            print('进入iframe失败')
            return False

    def out_iframe(self):
        """
        退出所以iframe
        :return: True
        """
        # self.drive.switch_to_default_content()      # 已过时
        self.drive.switch_to.default_content()
        return True

    def run_js(self, js='None'):
        """
        执行js
        :param js: 可执行的语句
        :return:
        """
        try:
            self.drive.execute_script(js)
            return True
        except:
            traceback.format_exc()
            print('js语言执行失败')
            return False

    def assert_equal(self, actual_result, expected_result):
        """
        断言是否相等
        :param actual_result: 实际结果
        :param expected_result: 预期结果
        :return:
        """
        if actual_result == expected_result:
            return True
        else:
            return False

    def sleep(self, times='1'):
        """
        固定等待时间,默认等待1s'
        :param times: 需要等待的时间
        :return:
        """
        try:
            times = int(times)
            time.sleep(times)
        except:
            traceback.format_exc()
            time.sleep(1)
            print('固定等待输入格式不对，程序自动默认等待1s')

    def close_window(self):
        """
        关闭当前窗口页面
        :return:
        """
        self.drive.close()
        return True

    def quit(self):
        """
        退出浏览器；
        自动化测试时，禁止频繁启动停止浏览器
        原因：启动很慢，运行也比较慢，不过，启动之后Webdriver的操作速度虽然不快但还是可以接受的
        :return:
        """
        try:
            self.drive.quit()
            return True
        except:
            traceback.format_exc()
            return False

    # def __locator_element(self, locator='None'):
    #     """
    #     重写__locator_element方法，规定只使用xpath定位元素
    #     :param locator:
    #     :return:
    #     """
    #     self.element = self.drive.find_element_by_xpath(locator)
    #     return self.element

    def __locator_element(self, locator='None', method='xpath'):
        """
        8种定位方式，默认使用xpath
        基于method的值，来选择定位的方式，并且使用locator作为定位表达式
        :param method:定位方式类型
        :param locator:定位表达式
        :return:
        """
        # xpath定位，最大优势，可以用text()文本定位
        # 放在第一个便于自动化时第一个判决就可以找到xpath
        try:
            if method == 'xpath':
                self.element = self.drive.find_element_by_xpath(locator)
            # 基于元素的id属性进行定位，实际上用的就是  # id通过css选择器定位。  用kw.
            elif method == 'id':
                self.element = self.drive.find_element_by_id(locator)
            # 基于元素name属性定位 用 wd
            elif method == 'name':
                self.element = self.drive.find_element_by_name(locator)
            # 基于元素标签名定位，就是input标签
            elif method == 'tagname':
                self.element = self.drive.find_element_by_tag_name(locator)
            # 基于css样式class属性定位 s_ipt
            elif method == 'classname' or method == 'class':
                self.element = self.drive.find_element_by_class_name(locator)
            # 基于超链接的文本内容定位，只能用于a元素
            elif method == 'linktext' or method == 'link':
                self.element = self.drive.find_element_by_link_text(locator)
            # 基于超链接的部分文本内容定位，只能用于a元素
            elif method == 'partiallinktext' or method == 'partiallink':
                self.element = self.drive.find_element_by_partial_link_text(locator)
            # css选择器定位。 速度快
            elif method == 'css':
                self.element = self.drive.find_element_by_css(locator)
            # 输入mothod不匹配时，默认使用xpath
            else:
                self.element = self.drive.find_element_by_xpath(locator)

            return self.element
        except Exception:
            traceback.format_exc()
            return False
