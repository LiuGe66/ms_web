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
    wait_poll: float = 0.1
    # 浏览器类型
    driver_type: str = 'chrome'
    # 是否无界面运行
    gui: bool = True
    # 是否全屏
    window_max: bool = False
    # 主页地址
    home_url: str = ''
    # 是否截图
    cap_png: bool = True
    # 测试账号
    test_accounts: str = 'liuge002'
    # 测试密码
    test_pwd: str = 'liuge666'
    # 远程地址
    grid_url: str = ''
    # 是否使用远程
    use_grid: bool = False
    # 日志清理门限值
    logs_num_clear: int = 10
    # 浏览器debugger模式
    browser_debugger: bool = False
    # 设置cookies
    set_cookies: bool = False
    # 打开debugger模式后是否第一次运行
    first_debugger: bool = False

    debugger_gui: bool = False

    grid_node1_url: str = "127.0.0.1:5555"

    grid_node2_url: str = "127.0.0.1:5556"

    info_bar: bool = False

# 载入ini文件内容
def load_ini():
    path = Path('pytest.ini')
    if not path.exists():
        return {}

    ini = IniConfig('pytest.ini')

    if 'uitest' not in ini:
        return {}

    return dict(ini['uitest'].items())


settings = UISettings(**load_ini())
