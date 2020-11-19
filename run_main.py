from script.interface_case import InterfaceCase
# When I wrote this, only God and I understood what I was doing
# Now, God only knows

# 开始接口测试
InterfaceCase(r'data\case\HTTP接口用例.xls').run()

# # 使用allure 需要自行下载安装allure
# pytest.main(["-s", "script1/loginCases.py", "--clean-alluredir", "reportTemp/temp"])
# # 执行命令行，生成allure测试报告
# os.system('allure generate reportTemp/temp -o reportTemp/report --clean')
