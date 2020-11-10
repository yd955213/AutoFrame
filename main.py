# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pytest


# del/s/q d:\123 ----(用于删除文件夹下的子文件)
# rd/s/q d:\123  ---(用于删除文件夹)
# /s 参数为子目录
# /q 参数为不用确认

if os.path.isdir('reportTemp/'):
    os.system(r'rd .\reportTemp\temp\ /s/q')
    os.system(r'rd .\reportTemp\report\ /s/q')
# 使用allure 需要自行下载安装allure
pytest.main(["-s", "testCases/loginCases.py", "--alluredir", "reportTemp/temp"])
# 执行命令行，生成allure测试报告
os.system('allure generate reportTemp/temp -o reportTemp/report --clean')

