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
from keywords.web import AutoWeb


# 对应allure 项目名
@allure.feature('自动化生成测试报告')
class TestLogin:
    # yaml_data = None
    try:
        # 如果yml格式读取失败
        yaml_data = ReadCasesYaml().read(os.path.abspath('data/case/cases.yml'))
        print(yaml_data)
    except:
        exit(-1)

    def setup_class(self):
        self.web = AutoWeb()
        self.web.start_browser()

    def teardown_class(self):
        self.web.sleep(3)
        self.web.quit()
    
    @allure.step
    def run_step(self, func, params):
        """
        显示每一步执行步骤
        :param func: 关键字函数
        :param params: 参数列表
        :return:
        """
        func(*params)
    
    @allure.story('login')
    @pytest.mark.parametrize('all_cases', yaml_data['loginPage'])
    def test_case(self, all_cases):
        """
        数据驱动实现
        """
        allure.dynamic.title(all_cases.get('title'))
        allure.dynamic.description(all_cases.get('description'))
        # 获取cases.yml的测试用例
        logger.info(all_cases)
        test_cases_list = all_cases.get('cases')
        # try:
        for case_step in test_cases_list:
            print('case_step = %s ' % case_step)
            print(case_step.get('method'))
            print(hasattr(self.web, case_step.get('method')))
            
            if hasattr(self.web, case_step.get('method')):
                # 通过反射查找关键字执行相应的函数
                # func = getattr(self.test_login,  case_step.get('method'))
                func = self.web.__getattribute__(case_step.get('method'))
                
                self.step_name = case_step.get('name')
                print("case_name = %s" % self.step_name)
                # print(func)
                # 函数valuse（）按顺序获取参数
                print('case_step = %s' % case_step)
                print('case_step = %s' % case_step.valuse())
                params_list = list(case_step.valuse())[2:]
                with allure.step(self.step_name):
                    try:
                        self.run_step(func, params_list)
                        result = self.run_step(func, params_list)
                    except Exception as err:
                        logger.error(case_step)
                        logger.exception(err)
                        # allure.attach(get_error_img(1.25), "失败")
                        pytest.fail('用例执行失败：{}'.format(err))
                    if result:
                        assert True
                    else:
                        assert False
            else:
                print('%s函数不存在' % case_step.get('method'))
                return False
        # except Exception as e:
        #     logger.exception(e)


if __name__ == '__main__':

    # # 使用allure 需要自行下载安装allure
    # pytest.main(["-s", "loginCases.py", "--alluredir", "../reportTemp/temp"])
    # # 执行命令行，生成allure测试报告
    # os.system('allure generate ../reportTemp/temp -o ../reportTemp/report --clean')
    dic = [{'name': '打开登录页', 'method': 'visit_url', 'url': 'http://testingedu.com.cn:8000/index.php/Home/user/login.html'}, {'name': '输入用户名', 'method': 'input', 'locator': '//*[@id="username"]', 'value': 13800138006}, {'name': '输入密码', 'method': 'input', 'locator': '//*[@id="password"]', 'value': 123456}, {'name': '输入验证码', 'method': 'input', 'locator': '//*[@id="verify_code"]', 'value': 111111}, {'name': '点击登录', 'method': 'click', 'locator': '//*[@id="loginform"]/div/div[6]/a'}]
    print(dic.values())