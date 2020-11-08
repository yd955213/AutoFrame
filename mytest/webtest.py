#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

"""
@File   : webtest.py
@Time   : 2020/11/7 6:04
@Author : yd
@Version: 1.0
@ToDo    : web自动化测试
"""
from comm.verify import Verify
from keywords.web import AutoWeb


class POTest:

    def __init__(self):
        self.web = AutoWeb()
        self.web.start_browser()
        self.web.visit_url('http://www.testingedu.com.cn:8000/index.php')
        self.want_buy_goods = None

    def set_want_buy_goods(self, want_buy_goods='Apple 苹果 iPhone 6'):
        """
        设置想要买入的商品
        :param want_buy_goods:
        :return:
        """
        self.want_buy_goods = want_buy_goods

    def long_in_ok(self):
        # 点击登录按钮
        self.web.click('//div[@class="fl nologin"]/a[1]')
        # 等待页面刷新
        self.web.sleep(1)
        # 输入用户名
        self.web.input('//input[@id="username"]', '13800138006')
        # 输入密码
        self.web.input('//input[@id="password"]', '123456')
        # 识别验证码
        self.web.verify_recognition(locator='//imgs[@id="verify_code_img')
        # 输入验证码
        print(self.web.verify_code)
        self.web.input('//input[@id="verify_code"]', self.web.verify_code)
        # 点击登录
        boolean = self.web.click('//a[@name="sbtbutton"]')
        if not boolean:
            self.web.quit()
        else:
            print("成功")

    def __find_woods(self):
        """
        在我的订单中进行商品搜索
        :return:
        """
        # # 点击我的订单 会新增一个窗口:处理关闭当前窗口，再切换到第一个窗口
        # self.web.click('//li[contains(a, "我的订单")][1]/a')
        # self.web.close_window()
        # self.web.switch_window(0)
        # self.web.sleep(3)
        # 去我的订单界面
        self.web.visit_url('http://www.testingedu.com.cn:8000/index.php/Home/Order/order_list.html')
        self.web.sleep(2)
        # 文本框中输入手机，并点击搜索
        self.web.input('//input[@name="q"]', self.want_buy_goods)
        self.web.click('//form[@id="sourch_form"]/a')

        # 滚动到条滚动显示找到需要购买的Apple 苹果 iPhone 6 元素
        self.web.hovering('//a[contains(text(), "'+self.want_buy_goods+'")]')
        # # 便于观察，做个等待
        # self.web.sleep(2)

    def __pay(self):
        self.web.sleep(1)
        # 选择第二个地址（默认有4个地址供选择）
        self.web.click('//span[contains(text(),"更多地址")]')
        self.web.click('//div[@class="consignee-list p"]/ul/li[2]/div[2]/span[4]')
        # 提交订单
        self.web.click('//button[@class="checkout-submit"]')

        self.web.sleep(1)
        # 支付方式先选择财付通在选择支付宝
        self.web.click('//imgs[@src="/plugins/payment/tenpay/logo.jpg"]')
        self.web.sleep(1)
        self.web.click('//imgs[@src="/plugins/payment/alipay/logo.jpg"]')

        # 确认支付方式
        self.web.click('//a[contains(text(), "确认支付方式")]')
        self.web.sleep(2)

    def __pay_in_shopping_car(self):
        """
        加入购物车后，在购物车种点击去结算进行结算
        :return:
        """
        self.web.sleep(1)
        # 滚动到去结算元素位置
        self.web.hovering('//a[contains(text(),"去结算")]')
        # 点击去结算
        self.web.click('//a[contains(text(),"去结算")]')
        self.__pay()

    def buy_model_1(self):
        """
        搜索页面直接加入购物车，并在提示框种进行结算
        这里有问题：点击加入购物车时，有的商品直接弹出iframe界面提示添加成功，有的时直接跳转到商品信息界面
        :return:
        """
        self.__find_woods()
        # 购买数量 输入2
        self.web.input('//a[contains(text(), "'+self.want_buy_goods+'")][1]/../following-sibling::div/div/input', 2)
        self.web.sleep(1)
        # //input[@id="number_27"]/../p/a[1] 点击2次 加数量的箭头
        self.web.click('//a[contains(text(), "'+self.want_buy_goods+'")][1]/../following-sibling::div/div[1]/p/a[1]')
        self.web.sleep(1)
        self.web.click('//a[contains(text(), "'+self.want_buy_goods+'")][1]/../following-sibling::div/div[1]/p/a[1]')
        self.web.sleep(1)
        # 加入购物车
        self.web.click('//a[contains(text(), "'+self.want_buy_goods+'")][1]/../following-sibling::div/div[2]/a')
        self.web.sleep(1)
        # '''
        # 在iframe提示框中结算
        # '''
        # 进入iframe
        self.web.into_iframe('//iframe[@name="layui-layer-iframe1"]')
        # 去购物车结算
        self.web.click('//a[contains(text(), "去购物车结算")]')

        self.__pay_in_shopping_car()

    def buy_model_2(self):
        """
        找到购买的元素，点击图片进入商品
        :return:
        """
        self.__find_woods()
        # 点击图片，跳转商品购买页面
        self.web.click('//a[contains(text(),"'+self.want_buy_goods+'")]/../../div[1]/a/imgs')
        # 数量栏输入3阁商品，点击+2次，点击-1次
        self.web.input('//*[@id="number"]', 3)
        for i in range(3):
            self.web.click('//*[@id="buy_goods_form"]/div/div[5]/ul/li[2]/div[1]/a[2]')
        self.web.click('//*[@id="buy_goods_form"]/div/div[5]/ul/li[2]/div[1]/a[2]')
        # # 立即购买
        # self.web.click('//a[@id="buy_now"]')
        # 加入购物车
        self.web.click('//a[@id="join_cart"]')
        '''
        关闭提示界面，在商品页，的我的购物车中结算
        '''
        # 进入iframe
        # self.web.into_iframe('//iframe[@class="bdselect_share_bg"]')
        # 关闭提示框 加入购物车后，等待弹框
        self.web.sleep(1)
        self.web.click('//div[@id="layui-layer1"]/span/a')
        # 退出iframe
        # self.web.out_iframe()
        # 找打我的购物车，鼠标悬停在上面
        self.web.hovering('//span[contains(text(),"我的购物车")]')
        # 点击去购物车结算
        self.web.click('//a[contains(text(),"去购物车结算")]')
        self.__pay_in_shopping_car()

    def register(self):
        # 点击注册//iframe[@class="bdselect_share_bg"]
        self.web.click('//a[contains(text(), "注册")]')
        self.web.sleep(2)
        # 选择邮箱注册
        self.web.click('//a[contains(text(), "邮箱注册")]')
        # 输入邮箱
        self.web.input('//input[@name="username"]', '664720125@qq.com')
        # 输入图像验证码
        self.web.verify_recognition('//imgs[@id="reflsh_code2"]')
        self.web.input('//input[@name="verify_code"]', self.web.verify_code)
        # 输入邮箱验证码
        self.web.input('//input[@name="code"]', '1')
        # 输入设置密码
        self.web.input('//input[@id="password"]', '654321')
        # 输入确认密码
        self.web.input('//input[@id="password2"]', '654321')
        # 输入推荐人手机
        self.web.input('//input[@name="invite"]', '12345678976')

    def screen_shor(self):
        self.web.visit_url('http://www.testingedu.com.cn:8000/home/User/login.html')
        self.web.screenshot('//imgs[@id="verify_code_img"]')

    def logout(self):
        # 点击安全退出
        self.web.click('//div[@class="fl islogin hide"]/a[2]')


if __name__ == '__main__':
    test = POTest()
    test.long_in_ok()
    # test.set_want_buy_goods()
    test.set_want_buy_goods("Samsung/三星 Galaxy S9 SM-G9600/DS 全网通 4G手机")
    #
    test.buy_model_1()
    test.buy_model_2()
    test.screen_shor()

