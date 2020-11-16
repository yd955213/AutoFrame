# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   screen_shot.py
@Time   :   2020-11-11 14:04
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import cv2

from global_path import get_abspath


def get_error_img(obj, zoom=1.25):
    """
    错误截图
    :param zoom:
    :return:
    """
    path = get_abspath('data/imgs/tmp.png')
    if obj.ele is None:
        return obj.driver.get_screenshot_as_png()
    else:
        # 标注元素位置
        obj.driver.get_screenshot_as_file(path)
        # 使用cv2画图
        img = cv2.imread(path)
        # 先获取位置
        location = obj.ele.location
        # 再获取元素的大小
        size = obj.ele.size
        # 再计算缩放
        x = int(location['x'] * zoom)
        y = int(location['y'] * zoom)
        # 去画一个矩形
        cv2.rectangle(img, (x, y), (x + int(size['width'] * zoom), y + int(size['height'] * zoom)), (0, 0, 255), 5)
        # 把画好的图保存
        cv2.imwrite(path, img)
        # 再读出二进制返回
        with open(path, 'rb') as f:
            file = f.read()
        return file
