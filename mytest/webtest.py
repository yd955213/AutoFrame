#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : webtest.py
@Time   : 2020/11/7 6:04
@Author : yd
@Version: 1.0
@ToDo    : web自动化测试
"""
from keywords.web import AutoWeb


class POTest:

    def __init__(self):
        self.web = AutoWeb()
        self.web.start_browser()
        self.web.visit_url('http://www.testingedu.com.cn:8000/index.php')

    def long_in_ok(self):
        # 点击登录按钮
        boolean = self.web.click('//div[@class="fl nologin"]/a[1]')
        # 等待页面刷新
        self.web.sleep(1)
        # 输入用户名
        self.web.input('//input[@id="username"]', '13800138006')
        # 输入密码
        self.web.input('//input[@id="password"]', '123456')
        # 输入验证码
        self.web.input('//input[@id="verify_code"]', '123456')
        # 点击登录
        self.web.click('//a[@name="sbtbutton"]')
        if not boolean:
            self.web.quit()
        else:
            print("成功")

    def buy_phone(self):
        # 点击我的订单 会新增一个窗口:处理关闭当前窗口，再切换到第一个窗口
        self.web.click('//li[contains(a, "我的订单")][1]/a')
        self.web.close_window()
        self.web.switch_window(0)
        self.web.sleep(3)
        # 文本框中输入手机，并点击搜索
        self.web.input('//input[@name="q"]', '手机')
        self.web.click('//form[@id="sourch_form"]/a')
        # 购买4个Apple 苹果 iPhone 6
        self.web.input('//a[contains(text(), "Apple 苹果 iPhone 6")][1]/../following-sibling::div/div/input', 2)
        # //input[@id="number_27"]/../p/a[1] 点击2次 加数量的箭头
        self.web.click('//a[contains(text(), "Apple 苹果 iPhone 6")][1]/../following-sibling::div/div[1]/p/a[1]')
        self.web.click('//a[contains(text(), "Apple 苹果 iPhone 6")][1]/../following-sibling::div/div[1]/p/a[1]')
        # 加入购物车
        self.web.click('//a[contains(text(), "Apple 苹果 iPhone 6")][1]/../following-sibling::div/div[2]/a')
        # 进入iframe
        self.web.into_iframe('//iframe[@name="layui-layer-iframe1"]')
        # 去购物车结算
        self.web.click('//a[contains(text(), "去购物车结算")]')
        # self.web.click('//a[contains(text(), "Apple 苹果 iPhone 6")]')

        # //a[contains(text(), "Apple 苹果 iPhone 6")]
        # 去结算
        self.web.click('//a[contains(text(),"去结算")]')
        self.web.sleep(1)
        # 选择第二个地址（默认有4个地址供选择）
        self.web.click('//span[contains(text(),"更多地址")]')
        self.web.click('//div[@class="consignee-list p"]/ul/li[2]/div[2]/span[4]')
        # 提交订单
        self.web.click('//button[@class="checkout-submit"]')

        self.web.sleep(3)
        # 支付方式先选择财付通在选择支付宝
        self.web.click('//img[@src="/plugins/payment/tenpay/logo.jpg"]')
        self.web.sleep(1)
        self.web.click('//img[@src="/plugins/payment/alipay/logo.jpg"]')

        # 确认支付方式
        self.web.click('//a[contains(text(), "确认支付方式")]')

    def logout(self):
        # 点击安全退出
        self.web.click('//div[@class="fl islogin hide"]/a[2]')


if __name__ == '__main__':
    test = POTest()
    test.long_in_ok()

    test.buy_phone()
