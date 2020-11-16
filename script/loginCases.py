# !/uer/bin/env python
# -*- coding: utf-8 -*-
"""
@File   :   loginCases.py
@Time   :   2020-11-10 14:14
@Author :   yang_dang
@Contact    :   664720125@qq.com
@Version    :   1.0
@Description   :   登录测试用来
"""
import os

import allure
import pytest
from comm.logger import logger
from comm.readYaml import ReadCasesYaml
from comm.screen_shot import get_error_img
from keywords.web import AutoWeb


# 对应allure 项目名
@allure.feature('自动化生成测试报告')
class TestLogin:
    # yaml_data = None
    try:
        # 如果yml格式读取失败
        yaml_data = ReadCasesYaml().read(os.path.abspath('data/case/cases.yml'))
        if yaml_data is None or yaml_data == {}:
            logger.error('获取测试用例为空')
            exit(-1)
        # print(yaml_data)
    except Exception as e:
        logger.error(e)
        exit(-1)

    def setup_class(self):
        """

        """
        self.web = AutoWeb()
        self.web.start_browser()
        # 访问首页获取必须的cookie
        self.web.visit_url('http://www.testingedu.com.cn:8000/index.php')

    def teardown_class(self):
        self.web.sleep(3)
        self.web.quit()

    @allure.step
    def run_step(self, func, params):
        """
        显示每一步执行步骤
        :param func: 关键字函数
        :param params: 参数列表
        # :param method: 关键字函数
        # :param parameter: 参数列表
        :return:
        """
        return func(*params)

    def teardown(self):
        # 点击安全退出
        self.web.click('//div[@class="fl islogin hide"]/a[2]')

    @allure.story('login')
    @pytest.mark.parametrize('all_cases', yaml_data['loginPage'])
    def test_case(self, all_cases):
        """
        用例参数化
        """
        # allure.dynamic.title(all_cases.get('title'))
        allure.dynamic.title(all_cases['title'])
        # allure.dynamic.description(all_cases.get('description'))
        allure.dynamic.description(all_cases['description'])
        # 获取cases.yml的测试用例
        logger.info(all_cases)
        test_cases_list = all_cases.get('cases')
        # try:
        for case_step in test_cases_list:
            if hasattr(self.web, case_step.get('method')):
                # 通过反射查找关键字执行相应的函数
                # func = getattr(self.test_login,  case_step.get('method'))
                func = self.web.__getattribute__(case_step.get('method'))

                print(func.__code__.co_argcount)  # 参数个数
                print(func.__code__.co_varnames)  # 所有参数名
                self.step_name = case_step.get('name')
                # 函数valuse（）按顺序获取参数
                print('case_step = %s' % case_step)
                params_list = list(case_step.values())[2:]
                print('case_step——list = %s' % params_list)
                with allure.step(self.step_name):
                    # try:
                    result = self.run_step(func, params_list)
                    # except Exception as err:
                    #     logger.error(case_step)
                    #     logger.exception(err)
                    #     # 失败给出异常信息
                    #     pytest.fail('用例执行失败：{}'.format(err))
                    #     # 失败截图
                    #     allure.attach(get_error_img(self.web), '失败截图', allure.attachment_type.PNG)
                    print(result)
                    if result:
                        assert True
                    else:
                        assert False
                # # 用例执行完成时，截图
                    allure.attach(self.web.drive.get_screenshot_as_png(), '结果截图', allure.attachment_type.PNG)
            else:
                logger.error('%s函数不存在' % case_step.get('method'))
                return False

            # 用例执行完成时，截图
            allure.attach(self.web.drive.get_screenshot_as_png())
        # except Exception as e:
        #     logger.exception(e)


if __name__ == '__main__':

    # 使用allure 需要自行下载安装allure
    pytest.main(["-s", "loginCases.py", "--alluredir", "../reportTemp/temp"])
    # 执行命令行，生成allure测试报告
    os.system('allure generate ../reportTemp/temp -o ../reportTemp/report --clean')

