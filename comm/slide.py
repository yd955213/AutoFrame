#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : slide.py
@Time   : 2020/11/7 21:39
@Author : yd
@Version: 1.0
@ToDo    : 实现滑块验证的拖动识别
"""
import base64
import json
import random
import time
import cv2
import pyautogui
import requests


from selenium.webdriver import ActionChains

from global_path import get_global_path


class Slide:
    def __init__(self, driver):
        """
        滑块验证码识别类
        :param driver:
        """
        self.driver = driver
        self.target_xpath = ""
        self.template_xpath = ""
        self.base_param = None
        # 背景图的宽度
        self.background_width = None

    def find_pictrue(self, target="../data/imgs/slide_block.png", template="../data/imgs/slide_background.png"):
        """
        找出图像中最佳匹配位置
        :param target: 目标即背景图
        :param template: 模板即需要找到的图
        :return: 返回最佳匹配及其最差匹配和对应的坐标
        """
        print(target)
        print(template)
        # 打开背景图
        target_rgb = cv2.imread(get_global_path(target))
        # 灰度处理
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        # 打开模板图
        template_rgb = cv2.imread(get_global_path(template), 0)
        self.background_width = template_rgb.shape[1]
        # 获取
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        print(value)
        # 返回最佳匹配的x坐标
        return value[2]

    def slide_img(self, src='', host=None, filepath="../data/imgs/t.png"):
        """
        下载验证码图片
        :param src: 图片
        :param host: 相对地址需要添加的主机地址
        :param filepath: 保存的图片位置
        :return: 保存的成功的图片位置，失败None
        """
        if src is None:
            return None

        # 处理base64图片
        if src.startswith('data:'):
            src = src[src.find('base64,') + 7:]
            return self.base64_to_img(src, filepath=get_global_path(filepath))

        # 处理相对路径url地址图片
        if not src.startswith('http'):
            src = host + "/" + src

        # 使用requests下载图片
        response = requests.get(src)
        # 获取的文本实际上是图片的二进制文本
        img = response.content
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        with open(filepath, 'wb') as f:
            f.write(img)
        return filepath

    def base64_to_img(self, base64_str, filepath="../data/imgs/t.png"):
        """
        base64图片转二进制存储
        :param base64_str: base64字符串
        :param filepath: 保存图片地址
        :return:
        """
        try:
            imgdata = base64.b64decode(base64_str)
            file = open(get_global_path(filepath), 'wb')
            file.write(imgdata)
            file.close()
            return filepath
        except:
            return None

    def slide_verify(self, xpath1, xpath2, jsonp=None):
        """
        验证码滑动实现
        :param xpath1: 背景图片定位器
        :param xpath2: 模板图片定位器
        :param jsonp: 微调参数json配置字符串
        :jsonp 详解：
            : slide : 滑动方式，selenium：使用selenium原生滑动，更稳定；pyautogui：校验滑动轨迹的滑动，必须使用pyautogui
            : target : 背景图片保存位置
            : template : 模块图片保存位置
            : host : 图片相对地址host主机地址
            : offset-x : 开始位置，x左边偏移（右边为正，左边为负）
            : offset-y : 开始位置，y左边偏移（下方为正，上方为负）
            : offset :  滑动位置偏移量（右边为正，左边为负）
            : template-zoom : 模板文件缩放比例
            : zoom : windows缩放比例
            : refresh : 刷新重试元素xpath
        :return:
        """
        self.base_param = {
            'zoom': 1,
            'target': '../data/imgs/slide_block.png',
            'template': '../data/imgs/slide_background.png',
            'host': '',
            'offset-x': 0,
            'template-zoom': 1,
            'offset-y': 0,
            'offset': 0,
            'slide': 'selenium',
            'refresh': '',
        }
        # 取第一次匹配的y坐标开始位置
        y = 0
        # 处理微调参数
        if not jsonp is None:
            jsonp = json.loads(jsonp)
            self.base_param.update(jsonp)
        # print(self.base_param)

        i = 0
        self.driver.implicitly_wait(3)
        # 重试10次
        while i < 10:
            # 如果不是第一次，则等待3s
            if i > 0:
                time.sleep(3)

            # 获取背景图片元素
            try:
                ele = self.driver.find_element_by_xpath(xpath1)
            except Exception as e:
                break

            # 如果匹配成功，背景图片不显示了，则返回成功
            succ = False
            try:
                succ = ele.is_displayed()
            except:
                print('here')
                break

            if i > 0 and succ == False:
                break
            else:
                # 如果滑动失败，则点击重试元素，重新获取图片
                if self.base_param["refresh"] != "":
                    eler = self.driver.find_element_by_xpath(self.base_param["refresh"])
                    eler.click()
                    time.sleep(2)

            i += 1

            # 背景图片地址
            src1 = ele.get_attribute('src')
            # 如果是selenium滑动，需要计算图片缩放比例
            w1 = ele.size['width']
            # 获取滑块元素
            ele1 = self.driver.find_element_by_xpath(xpath2)
            # 获取滑块图片
            src2 = ele1.get_attribute('src')
            # 下载图片
            self.slide_img(src1, filepath=self.base_param['target'], host=self.base_param['host'])
            self.slide_img(src2, filepath=self.base_param['template'], host=self.base_param['host'])
            # 获取背景图片实际大小
            img = cv2.imread(self.base_param['target'])
            w2 = img.shape[1]
            # 获取匹配到滑块的x坐标滑动距离
            x = self.find_pictrue(target=self.base_param['target'], template=self.base_param['template'])
            # print(x)

            # 使用selenium原生滑动
            if self.base_param['slide'] == 'selenium':
                # 计算缩放比例，计算偏移量
                x = int(x * w1 / w2) - self.base_param['offset']
                action = ActionChains(self.driver)  # 实例化一个action对象
                action.click_and_hold(ele1).perform()  # perform()用来执行ActionChains中存储的行为
                action.move_by_offset(x, 0).pause(0.8).perform()
                action.release().perform()

            # 使用pyautogui滑动
            else:
                # 获取元素位置
                ele_x = ele.location['x']
                ele_y = ele.location['y']
                # 计算缩放比例
                if self.base_param['zoom'] != 1:
                    x = int(x * self.base_param['zoom'])
                    ele_x = int(ele_x * self.base_param['zoom'])
                    ele_y = int(ele_y * self.base_param['zoom'])

                # 计算开始位置x的偏移量
                if self.base_param['offset-x'] != 0:
                    ele_x = ele_x + self.base_param['offset-x']

                # 计算开始位置y的便宜量
                if self.base_param['offset-y'] != 0:
                    ele_y = ele_y + self.base_param['offset-y']

                # 计算移动距离模板的缩放比例
                if self.base_param['template-zoom'] != 1:
                    x = int(x * self.base_param['template-zoom'])

                # 计算移动距离x的偏移量
                if self.base_param['offset'] != 0:
                    x = x + self.base_param['offset']

                # 去第一次元素y的坐标
                if i == 1:
                    y = ele_y

                # print(ele_x, ele_y)
                # 调用pyautogui，实现轨迹变化滑动
                self.slide_by_pyautogui(ele_x, y, x)

        self.driver.implicitly_wait(10)

    def slide_by_pyautogui(self, x, y, x_offset, y_offset, screen_ratio='1.00'):
        """
        使用pyautogui模拟鼠标拖动模块滑动
        :param x: 鼠标开始位置x
        :param y: 鼠标开始位置y
        :param x_offset: 横坐标偏移量
        :param y_offset: 纵坐标偏移量
        :param screen_ratio: 屏幕缩放比例，默认1.00
        :return:
        """
        # 移动鼠标到起始位置 pyautogui默认鼠标在0，0 位置；duration 耗时 单位s
        pyautogui.moveTo(x, y, duration=0.1)
        # 按下鼠标键
        pyautogui.mouseDown()
        '''
        模拟人公司手动校验滑块位置，第一次超出位置，第二次未到位置，第三次对准
        备注：有可能第一次或者第二次就滑动成功
        '''
        screen_ratio = float(screen_ratio)
        # 模拟非直线滑动
        x_temp = random.randint(5, 15)
        x = (x + x_offset) * screen_ratio + x_temp
        y = (y + y_offset) * screen_ratio + x_temp
        pyautogui.moveTo(x, y, duration=0.38)
        # print(x, y)
        # 往回滑
        x_temp_1 = random.randint(-9, -5)
        x_temp += x_temp_1
        x += x_temp_1
        y += x_temp_1
        pyautogui.moveTo(x, y, duration=0.2)
        # print(x, y)
        # 第3次滑动到位置附近
        x += x_temp + random.randint(-1, 1)
        y += x_temp + random.randint(-1, 1)
        pyautogui.moveTo(x, y, duration=0.1)

        # print(x, y)
        pyautogui.mouseUp()  # 松开鼠标
