# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: conftest.py
# @Time : 2022/11/24 16:15
import json
import shutil
from pathlib import Path
import pytest
from selenium import webdriver
from core.setting import settings
from selenium.webdriver.firefox.options import Options
from utils.logger_utils import *


# @pytest.fixture(scope="session", autouse=True)
def start_appium():
    flag = 0
    while flag == 0:
        result = os.popen('netstat -aon|findstr "4723"')  # 查询端口占用情况
        time.sleep(1)
        content = result.read()  # 读取cmd窗口返回的文本内容
        # if "ESTABLISHED" in content:
        if "4723" in content and "LISTENING" in content:  # 如果4723端口被占用则退出
            # "127.0.0.1:4723"
            print_warning_log('========================Appium服务已就绪========================')
            flag = 1
            break
        else:  # 如果4723端口没被占用则启动appium服务
            print_warning_log('========================准备启动Appium服务========================')
            time_str = str(
                time.strftime('%Y_%m_%d_%H%M%S', time.localtime(time.time())))
            os.system(f'start /b appium > D:\\Python_project\\ui_1129\\logs\\appium_logs\\appium_{time_str}.log 2>&1 &')
            time.sleep(5)


def chrome_driver():
    options = webdriver.ChromeOptions()
    if not settings.info_bar:
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        driver = webdriver.Chrome(options=options)
        return driver
    if settings.use_grid:
        print_warning_log('正在以grid模式执行测试')
        driver = webdriver.Remote(
            command_executor=settings.grid_url,
            options=options
        )
        return driver

    if settings.browser_debugger:
        print_warning_log('正在以debugger模式运行浏览器')
        if settings.first_debugger:
            os.popen("D:\\tools\\chrome.bat")
        options.debugger_address = "127.0.0.1:9222"

    if settings.gui:
        print('运行到这里了吗58行')
        driver = webdriver.Chrome(options=options)
        print('运行到这里了吗60行')
        if settings.window_max:
            driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        elif settings.debugger_gui:
            print_info_log('正在以调试窗口运行浏览器')
            driver.set_window_position(1, 1)
            driver.set_window_size(1800, 550)
        return driver
    elif not settings.gui:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        no_gui_driver = webdriver.Chrome(options=options)
        print_warning_log('正在以无界面模式运行浏览器')
        if settings.window_max:
            no_gui_driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return no_gui_driver


def firefox_driver():
    if not settings.gui:
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        no_gui_driver = webdriver.Firefox(options=options, service_log_path='./logs/logs/geckodriver.log')
        print_warning_log('正在以无界面模式运行浏览器')
        if settings.window_max:
            no_gui_driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return no_gui_driver
    elif settings.gui:
        driver = webdriver.Firefox(service_log_path='./logs/logs/geckodriver.log')
        if settings.window_max:
            driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return driver


def set_cookies(driver):
    path = Path('temp/cookies/cookies.json')
    print_info_log('访问默认主页')
    driver.get(settings.home_url)
    cookies = driver.get_cookies()
    with open("./temp/cookies/cookies.json", "w") as f:
        f.write(json.dumps(cookies))
    # if path.exists():
    #     cookies = json.loads(path.read_text())
    print_info_log('正在尝试设置cookie')
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
            print_debug_log(f"设置cookie:{cookie}")
        except Exception as e:
            pass
    driver.refresh()


@pytest.fixture(scope="session")
def driver():
    if not settings.cap_png:
        print_warning_log('截图功能已关闭')
    if settings.driver_type == "firefox":
        print_info_log('正在使用Firefox浏览器')
        driver_ = firefox_driver()
        yield driver_
        driver_.quit()

    elif settings.driver_type == "chrome":
        print_info_log('正在使用Chrome浏览器')
        driver_ = chrome_driver()
        if settings.set_cookies:
            set_cookies(driver_)
        yield driver_
        driver_.quit()


@pytest.fixture(scope='session')
def start_app():
    # master大师
    # from appium.webdriver import Remote as a_Remote
    # caps = {
    #     "appium:platformName": "Android",
    #     "appium:deviceName": "1a44c444fb0b7ece",
    #     "appium:appPackage": "com.automaster.practice.through",
    #     "appium:appActivity": ".MainActivity",
    #     "appium:platformVersion": "10.0",
    #     "appium:noReset": True,
    #     "appium:dontStopAppOnReset": True
    # }
    # driver = a_Remote("http://127.0.0.1:4723/wd/hub", caps)
    # yield driver
    # driver.quit()

    # 读书屋
    # from appium.webdriver import Remote as a_Remote
    # caps = {
    #
    #     "appium:platformName": "Android",
    #     "appium:deviceName": "1a44c444fb0b7ece",
    #     "appium:platformVersion": "10.0",
    #     "appium:noReset": True,
    #     "appium:dontStopAppOnReset": True,
    #     "appium:appActivity": ".ui.home.MainActivity",
    #     "appium:appPackage": "com.zhao.myreader"
    # }
    #
    # driver = a_Remote("http://127.0.0.1:4723/wd/hub", caps)
    # yield driver
    # driver.quit()

    # # 应用宝
    # from appium.webdriver import Remote as a_Remote
    # caps = {
    #     "appium:platformName": "Android",
    #     "appium:deviceName": "1a44c444fb0b7ece",
    #     "appium:appPackage": "com.tencent.android.qqdownloader",
    #     "appium:appActivity": "com.tencent.pangu.link.SplashActivity",
    #     "appium:platformVersion": "10",
    #     "appium:noReset": True,
    #     "appium:dontStopAppOnReset": True
    # }
    # driver = a_Remote("http://127.0.0.1:4723/wd/hub", caps)
    # yield driver
    # driver.quit()

    # 微信
    from appium.webdriver import Remote as a_Remote
    start_appium()
    caps = {
        "appium:platformName": "Android",
        "appium:deviceName": "1a44c444fb0b7ece",
        "appium:appPackage": "com.tencent.mm",
        "appium:appActivity": ".ui.LauncherUI",
        "appium:platformVersion": "10",
        "appium:noReset": True,
        "appium:dontStopAppOnReset": True
    }
    driver = a_Remote("http://127.0.0.1:4723/wd/hub", caps)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def clear_logs():
    path = os.getcwd()
    files_count = len(os.listdir(path + "\\logs\\logs"))
    num = settings.logs_num_clear
    if files_count >= num:
        # 先强制删除指定目录
        shutil.rmtree(path + "\\logs\\logs")
        # 再新建一个同名目录
        os.mkdir(path + "\\logs\\logs")
        print_info_log("log数量超过{}条，日志目录已清空".format(num))

    # 清除appium日志
    result = os.popen('netstat -aon|findstr "4723"')  # 查询端口占用情况
    time.sleep(0.2)
    content = result.read()  # 读取cmd窗口返回的文本内容
    # if "ESTABLISHED" in content:
    if "4723" not in content:  # 如果4723端口没被占用则判断是否超限
        appium_files_count = len(os.listdir(path + "\\logs\\appium_logs\\"))
        if appium_files_count >= num:
            # 先强制删除指定目录
            shutil.rmtree(path + "\\logs\\appium_logs\\")
            # 再新建一个同名目录
            os.mkdir(path + "\\logs\\appium_logs\\")
            print_info_log("appium_log数量超过{}条，日志目录已清空".format(num))
