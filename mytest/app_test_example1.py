# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   app_test_example1.py
@Time   :   2020-11-13 8:58
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   
"""
import time
from telnetlib import EC

from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

caps = {
    "deviceName": "73MR50Q273",
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "appPackage": "com.teemmo.recolive",
    "appActivity": ".activity.StartActivity",
    "noRese": True,
    "unicodeKeyboard": True,
    "resetKeyboard": True,
    "automationName": "UIAutomator2"
}

driver = webdriver.Remote(r'http://localhost:4723/wd/hub', caps)

driver.implicitly_wait(10)
# 点击LOGO 长按后弹出密码框，进入设置界面
el1 = driver.find_element_by_id("com.teemmo.recolive:id/id_log_iv")
# 实现长按
TouchAction(driver).long_press(el=el1, duration=3000).perform()
# 输入密码
el2 = driver.find_element_by_id("com.teemmo.recolive:id/et_psw")
el2.send_keys("123456")
# 点击确定
el3 = driver.find_element_by_id("com.teemmo.recolive:id/btn_confirm")
el3.click()
# 点击 名单管理
el1 = driver.find_element_by_xpath('//*[@text="名单管理"]')
el1.click()
# 点击添加人员
el2 = driver.find_element_by_id("com.teemmo.recolive:id/iv_add")
el2.click()
# 输入姓名
el3 = driver.find_element_by_id("com.teemmo.recolive:id/et_name")
el3.send_keys("yd123")
# 选择性别
el4 = driver.find_element_by_id("com.teemmo.recolive:id/rbtn_male")
el4.click()
# 选择权限
el5 = driver.find_element_by_id("com.teemmo.recolive:id/rbtn_admin")
el5.click()
el7 = driver.find_element_by_id("com.teemmo.recolive:id/et_phone")
el7.send_keys("1")
el8 = driver.find_element_by_id("com.teemmo.recolive:id/et_id")
el8.send_keys("2")
el9 = driver.find_element_by_id("com.teemmo.recolive:id/et_staffNum")
el9.send_keys("3")
el10 = driver.find_element_by_id("com.teemmo.recolive:id/et_cardNum")
el10.send_keys("4")
el11 = driver.find_element_by_id("com.teemmo.recolive:id/et_department")
el11.send_keys("5")
el12 = driver.find_element_by_id("com.teemmo.recolive:id/et_post")
el12.send_keys("test")
# 设置有效期
el1 = driver.find_element_by_id("com.teemmo.recolive:id/tv_date")
el1.click()
el2 = driver.find_element_by_id("com.teemmo.recolive:id/tv_from")
el2.click()
el3 = driver.find_element_by_id("com.teemmo.recolive:id/tv_sure")
el3.click()
el4 = driver.find_element_by_id("com.teemmo.recolive:id/tv_to")
el4.click()
TouchAction(driver).press(x=267, y=1174).move_to(x=272, y=1125).release().perform()
el4 = driver.find_element_by_id("com.teemmo.recolive:id/tv_sure")
el4.click()
el5 = driver.find_element_by_id("com.teemmo.recolive:id/btn_confirm")
el5.click()

el6 = driver.find_element_by_id("com.teemmo.recolive:id/week_1")
el6.click()
el7 = driver.find_element_by_id("com.teemmo.recolive:id/week_2")
el7.click()
el8 = driver.find_element_by_id("com.teemmo.recolive:id/week_3")
el8.click()
el6 = driver.find_element_by_id("com.teemmo.recolive:id/week_4")
el6.click()
el7 = driver.find_element_by_id("com.teemmo.recolive:id/week_5")
el7.click()
el8 = driver.find_element_by_id("com.teemmo.recolive:id/week_6")
el8.click()
el8 = driver.find_element_by_id("com.teemmo.recolive:id/week_7")
el8.click()
el12 = driver.find_element_by_id("com.teemmo.recolive:id/btn_confirm")
el12.click()
time.sleep(0.5)
xpath_locator = "//*[@text=\"请配置图片\"]".format()
try:
    WebDriverWait.until(EC.precence_of_element_located(MobileBy.XPATH, xpath_locator))

    print('找到')
except Exception as e:
    print('错误')

# # 点击识别设置
# el1 = driver.find_element_by_xpath('//*[@text="识别设置"]')
# el1.click()

# # 调节相识度设置
# el1 = driver.find_element_by_id("com.teemmo.recolive:id/tv_progress")
# print(el1.text)
# el2 = driver.find_element_by_id("com.teemmo.recolive:id/sb_threshold")
# # 获取seekbar控件本身的（尺寸）宽度
# seekbar_width = el2.size.get('width')
# print(seekbar_width)
# # seekbar_height = el2.size.get('height')
# # seekbar_x = el2.location.get('x')
# seekbar_y = el2.location.get('y') + el2.size.get('height') / 2
# print(seekbar_y)
# end_location = float(seekbar_width * 80 / 95)
# print(end_location)
# TouchAction(driver).press(x=end_location, y=seekbar_y).perform()
# # # 相识度阈值设置为60%
# print(el1.text)
