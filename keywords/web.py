#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : web.py
@Time   : 2020/11/7 3:54
@Author : yd
@Version: 1.0
@ToDo    : 封装web自动化关键字
"""
import os
import time
import traceback
from selenium import webdriver
from selenium.webdriver import ActionChains

from comm.logger import logger
from comm.slide import Slide
from comm.verify import Verify


class AutoWeb:
    """
    封装web自动化关键字
    自动化测试时，禁止频繁启动停止浏览器
    原因：启动很慢，运行也比较慢，不过，启动之后Webdriver的操作速度虽然不快但还是可以接受的
    """

    def __init__(self):
        self.drive = None
        self.element = None
        # ie浏览器支持自动化时坑很多，需要特别处理，这里记录当前获取到的浏览器
        self.browser = 'chrome'
        self.verify_code = None
        # 被测电脑的系统显示文本的缩放比例， win10 在缩放与布局中查看 根据系统设置改造，后期修改为配置项，或将系统缩放设置为1
        self.screen_ratio = '1.00'
        # 保存js脚本运行后的返回值
        self.js_data = 'None'
        # 下载照片的宽或者高
        self.img_width = 'None'
        self.img_height = 'None'
        # 关联的字典
        self.relations = {}

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

        self.__maximize()
        self.drive.implicitly_wait(10)
        return True

    def __maximize(self):
        """
        最大化浏览器
        :return:
        """
        try:
            self.drive.maximize_window()
        except:
            logger.exception(traceback.format_exc())
            logger.exception('最大化浏览器失败')

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
            return True
        except:
            logger.exception(traceback.format_exc())
            logger.exception('访问页面失败')
            return False

    def input(self, locator='None', content='None'):
        """
        找到元素后，并输入文本内容
        :param locator: 定位器
        :param content: 输入文本内容
        :return: 是否输入成功
        """
        # print('input=%s' % locator)
        try:
            element = self.__locator_element(locator=locator)
            element.send_keys(str(content))
            return True
        except:
            logger.exception(traceback.format_exc())
            logger.exception('元素未找到或者输入失败')
            return False

    def click(self, locator='None'):
        """
        找到元素，并点击
        :param locator: 定位器
        :return: 是否点击成功
        """
        try:
            # ie调用.click()没有作用，使用js点击
            if self.browser == "ie":
                return self.__js_click(locator)
            else:
                element = self.__locator_element(locator=locator)
                element.click()
                return True

        except Exception:
            logger.exception(traceback.format_exc())
            logger.exception('元素未找到或者点击失败')
            return False

    def __js_click(self, locator='None'):
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
            logger.exception('元素未找到或者点击失败')
            logger.exception(traceback.format_exc())
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
            logger.exception(traceback.format_exc())
            logger.exception('窗口切换失败，需切换的窗口序号%s' % index)
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
            return True
        except:
            logger.exception(traceback.format_exc())
            logger.exception('进入iframe失败')
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
            # print(js)
            self.js_data = self.drive.execute_script(js)
            return True
        except:
            logger.exception(traceback.format_exc())
            logger.exception('js语言执行失败')
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

    def sleep(self, times=1):
        """
        固定等待时间,默认等待1s'
        :param times: 需要等待的时间
        :return:
        """
        try:
            times = int(times)
            time.sleep(times)
            return True
        except:
            logger.exception(traceback.format_exc())
            time.sleep(1)
            logger.exception('固定等待输入格式不对，程序自动默认等待1s')
            return False

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
            logger.exception(traceback.format_exc())
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
            logger.exception(traceback.format_exc())
            return False

    def moveto_element_js(self, high='1000'):
        """通过js增量滚动，防止页面分页加载,默认向下滚动1000像素
        :param high: 向下滚动多少像素，默认1000像素
        :return: 成功
        """
        self.run_js('window.scrollBy(0, %d)' % high)
        return True

    def hovering(self, locator='None'):
        """
        找到元素，将鼠标悬停在上面，用一些特定场景:如，鼠标移动到元素上，会出现下拉框
        :param locator: 定位表达式
        :return: 成功或者失败
        """
        try:
            element = self.__locator_element(locator)
            # ie浏览器使用js滚动到所以查找的元素位置
            if self.browser == 'ie':
                x = element.location.get('x')
                y = element.location.get('y')
                self.run_js('window.scrollTo(%d,%d)' % (x, y))
            else:
                action = ActionChains(self.drive)
                action.move_to_element(element).perform()
            return True
        except:
            logger.exception(traceback.format_exc())
            return False

    def screenshot(self, locator='None', save_img_path='../data/imgs/verify_img.png'):
        """
        在当前元素上进行截图,默认格式：.png
        :param locator: 定位表达式
        :param save_img_path: 截图图片保存路径
        :return:
        """
        try:
            element_img = self.__locator_element(locator)
            element_img.screenshot(filename=save_img_path)
            return True
        except:
            logger.exception(traceback.format_exc())
            return False

    def verify_recognition(self, locator='None', img_path='../data/imgs/verify_img.png', code_type='1902'):
        """
        常见4~6位英文数字验证码识别识别
        :param locator: 定位表达式
        :param code_type: 验证码类型 参考:http://www.chaojiying.com/price.html
        :param img_path:
        :return:
        """
        try:
            self.screenshot(locator, img_path)
            # 提供的账号和密码，超级鹰平台图片识别一分钱识别一次，账号没有可能无法识别
            verify1 = Verify('wuqingfqng', '6e8ebd2e301f3d5331e1e230ff3f3ca5', '96001')
            self.verify_code = verify1.post_picture(code_type=code_type, im=img_path)
            return self.verify_code
        except:
            logger.exception(traceback.format_exc())
            return 'None'

    def __get_element_src(self, locator='None'):
        """
        根据元素定位，获取元素中src属性的url地址，下载照片
        :param locator: 定位表达式
        :return: 查找元素的src信息
        """
        try:
            element = self.__locator_element(locator)
            # 获取照片url
            element_src = element.get_attribute('src')

            self.width = element.size['width']
            self.height = element.size['height']
            return element_src
        except:
            logger.exception(traceback.format_exc())
            return None

    def slide(self, slide_block_locator="None", slide_background_locator='None'):
            try:
                src = self.__get_element_src(slide_block_locator).get_attribute('src')
                if src.startswith('data:'):
                    pass
                    # self.__slide_base64(slide_block_locator, slide_background_locator)
                else:
                    self.__slide_url(slide_block_locator, slide_background_locator)
                return True
            except:
                return False

    def __slide_url(self, slide_block_locator="None", slide_background_locator='None'):
        """
        一键滑动:使用cv2找出图像中最佳匹配位置，拖动滚动条实现滚动
        :param slide_block_locator: 滑块元素定位表达式
        :param slide_background_locator: 滑块背景图定位表达式
        :return:
        """
        # 滑动模块类
        slide_1 = Slide(self.drive)
        # 下载保存照片
        block_path = slide_1.slide_img(host=self.__get_element_src(slide_block_locator),
                                       filepath='../data/imgs/slide_block.png')
        background_path = slide_1.slide_img(host=self.__get_element_src(slide_background_locator),
                                            filepath='../data/imgs/slide_background.png')

        # 获取x轴坐标
        x = slide_1.find_pictrue(target=block_path, template=background_path)
        # 计算图片缩放比 计算拖动距离  保存的图片为原始比例，但页面的显示的照片又缩放，这里获取缩放比例
        # 由于滑块的x坐标不为0， 此处的32时通过画图获取的
        x = int(x * slide_1.background_width / self.width) - 32
        '''滑动'''
        action = ActionChains(self.drive)
        # 点击滑块
        action.click_and_hold(self.__locator_element(slide_block_locator)).perform()
        action.move_by_offset(x, 0).perform()
        self.sleep('1')

    def slide_base64(self, slide_block_locator="None", slide_background_locator='None'):
        """

        :param slide_block_locator:
        :param slide_background_locator:
        :return:
        """

        # 滑动模块类
        slide_1 = Slide(self.drive)
        # 保存滑块图片
        slide_block_path = slide_1.slide_img(src=self.__get_element_src(slide_block_locator),
                                             filepath='../data/imgs/slide_block.png')
        # self.__get_element_src运行后获取对应元素
        # 获取滑块在屏幕显示的页面中的位置
        location_slide_block = self.element.location
        # print(location_slide_block)
        # 获取滑块的矩形长宽
        size_slide_block = self.element.size
        # print(size_slide_block)

        # 保存滑块背景图片
        slide_background_path = slide_1.slide_img(src=self.__get_element_src(slide_background_locator),
                                                  filepath='../data/imgs/slide_background.png')

        x_offset, y_offset = slide_1.find_pictrue(target=slide_block_path, template=slide_background_path)
        # 背景图和页面显示的背景图有缩放 注意：self.width 这里时滑块背景的宽度
        # print(self.width)
        x_offset = int(x_offset * self.width / slide_1.background_width)
        # print(x_offset)
        # 获取浏览器页面上方的高度
        self.run_js('return window.outerHeight - window.innerHeight;')
        browser_header = self.js_data
        # print('browser_header:%s' % browser_header)
        # 计数模块的中心位置
        x_slide = int(location_slide_block['x']) + size_slide_block['width'] // 2
        y_slide = (int(location_slide_block['y']) + int(browser_header)) + size_slide_block['height'] // 2
        # 计数模块中心位置时，x_offset相当于移动了size_slide_block['width'] // 2个长度，这里减去
        # x_offset -= size_slide_block['width'] // 2
        # y_offset -= size_slide_block['height'] // 2
        # print(x_slide, y_slide)

        # 滑块拖动时，一般y位移不变，为0
        slide_1.slide_by_pyautogui(x_slide, y_slide, x_offset, 0, screen_ratio=self.screen_ratio)

    def upload_picture(self, locator, path='../data/imgs/upload.png'):
        """
        实现文件上传
        :param locator: 定位表达式
        :param path: 上传文件的路径:绝对路径
        :return: 是否成功
        """
        try:
            path = os.path.abspath(path)
            if os.path.isfile(path):
                element = self.__locator_element(locator)
                element.sendkeys(path)
                return True
            else:
                logger.exception('文件不存在，路径：%s' % path)
                return False
        except:
            logger.exception(traceback.format_exc())
            return False

    def gettext(self, locator='None', parameter_name='None'):
        """
        获取文本，保存参数
        :param locator: 文本元素定位器
        :param parameter_name: 需要保存的参数名字
        :return:
        """
        ele = self.__find_ele(locator)
        self.relations[parameter_name] = ele.text
        return True

    def __get_relations(self, s):
        """
        获取关联后的字符串
        约定，如果要使用关联的变量，形式为{paramname}
        :param s: 需要关联的字符串
        :return: 返回关联后的字符串
        """
        if s is None or s == '':
            return ''
        else:
            s = str(s)
            for key in self.relations.keys():
                s = s.replace('{' + key + '}', self.relations[key])
            return s
