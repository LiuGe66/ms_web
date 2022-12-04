# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: setting.py
# @Time : 2022/11/29 10:10
from pathlib import Path

from iniconfig import IniConfig
from pydantic import BaseSettings, DirectoryPath


class UISettings(BaseSettings):
    # 报告生成路径
    allure_report_dir: DirectoryPath = './report'
    # 是否自动打开报告
    allure_show: bool = True
    # 最大显式等待时间
    wait_max: float = 10
    # 显式等待轮询间隔
    wait_poll: float = 0.01
    # 浏览器类型
    driver_type: str = 'chrome'
    # 是否无界面运行
    gui: bool = True
    # 是否全屏
    window_max: bool = False
    # 报告是否截图
    is_screenshot: bool = True
    # 主页地址
    home_url: str = 'http://shop-xo.hctestedu.com'
    # 是否截图
    cap_png: bool = True
    # 测试账号
    test_accounts: str = 'liuge002'
    # 测试密码
    test_pwd: str = 'liuge666'

    grid_url: str = ''

    use_grid: bool = False


# 载入ini文件内容
def load_ini():
    path = Path('pytest.ini')
    if not path.exists():
        return {}

    ini = IniConfig('pytest.ini')

    if 'uitest' not in ini:
        return {}

    return dict(ini['uitest'].items())


ui_setting = UISettings(**load_ini())
