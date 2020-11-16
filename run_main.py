import os
import pytest

from comm.file_tools import FileTools
from global_path import get_abspath


# 全局变量
config = FileTools(get_abspath('./config/config.properties')).read_config_text()


# 使用allure 需要自行下载安装allure
pytest.main(["-s", "script/loginCases.py", "--clean-alluredir", "reportTemp/temp"])
# 执行命令行，生成allure测试报告
os.system('allure generate reportTemp/temp -o reportTemp/report --clean')
