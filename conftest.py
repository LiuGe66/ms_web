# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: conftest.py
# @Time : 2022/11/24 16:15
import json
import shutil
from pathlib import Path
import pytest
from selenium import webdriver
from core import pom
from core.setting import ui_setting
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
                # time.strftime('%Y_%m_%d %H-%M-%S', time.localtime(time.time())))
                time.strftime('%Y_%m_%d_%H%M%S', time.localtime(time.time())))
            # os.system('start /b appium > D:\\Python_project\\ui_1129\\logs\\appium_{time_str}.log 2>&1 &')
            os.system(f'start /b appium > D:\\Python_project\\ui_1129\\logs\\appium_logs\\appium_{time_str}.log 2>&1 &')
            time.sleep(5)

def chrome_driver():
    if ui_setting.gui:
        options = webdriver.ChromeOptions()
        options.add_argument(r'--user-data-dir=C:\Users\sixyco\AppData\Local\Google\Chrome\User Data\Default')
        driver = webdriver.Chrome(chrome_options=options)
        if ui_setting.window_max:
            driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return driver
    elif not ui_setting.gui:
        options = webdriver.ChromeOptions()
        options.add_argument(r'--user-data-dir=C:\Users\sixyco\AppData\Local\Google\Chrome\User Data\Default')
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        no_gui_driver = webdriver.Chrome(chrome_options=options)
        print_info_log('正在以无界面模式运行浏览器')
        if ui_setting.window_max:
            no_gui_driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return no_gui_driver


def firefox_driver():
    if not ui_setting.gui:
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--disable-gpu")
        no_gui_driver = webdriver.Firefox(options=options, service_log_path='./logs/logs/geckodriver.log')
        print_info_log('正在以无界面模式运行浏览器')
        if ui_setting.window_max:
            no_gui_driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return no_gui_driver
    elif ui_setting.gui:
        driver = webdriver.Firefox(service_log_path='./logs/logs/geckodriver.log')
        if ui_setting.window_max:
            driver.maximize_window()
            print_info_log('正在以最大化窗口运行浏览器')
        return driver


@pytest.fixture(scope="session")
def driver():

    if not ui_setting.cap_png:
        print_info_log('截图功能已关闭')
    if ui_setting.driver_type == "firefox":
        print_info_log('正在使用Firefox浏览器')
        driver_ = firefox_driver()
        yield driver_
        driver_.quit()

    elif ui_setting.driver_type == "chrome":
        print_info_log('正在使用Chrome浏览器')
        driver_ = chrome_driver()
        yield driver_
        driver_.quit()



def set_cookies(driver):
    cookies = []
    path = Path('temp/cookies/cookies.json')
    if path.exists():
        cookies = json.loads(path.read_text())
    print_info_log('正在尝试设置cookie')
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
            print_debug_log(f"设置cookie:{cookie}")
        except Exception as e:
            pass
    print(f'设置cookies后访问主页{ui_setting.home_url}')
    driver.get(ui_setting.home_url)


def is_login(driver):
    if "请输入搜索文字" in driver.page_source:
        print_info_log('页面处于已登录状态')
        flag = 1
    else:
        print_info_log('页面处于已未登录状态')
        flag = 0

    return flag


@pytest.fixture(scope='session')
def user_driver():
    """
    返回已登录状态的浏览器
    :return:
    """
    if not ui_setting.cap_png:
        print_info_log('截图功能已关闭')
    if ui_setting.driver_type == "chrome":
        print_info_log('正在使用Chrome浏览器')
        driver = chrome_driver()
        print_info_log('正在以无界面模式运行浏览器')
        print_debug_log(f'user_driver夹具正在访问主页{ui_setting.home_url}')
        driver.get(ui_setting.home_url)
        set_cookies(driver)  # 加载登录状态

        if not is_login(driver):
            page = pom.HomePage(driver)
            page = page.to_login()  # 跳转到登录页面
            page.login(ui_setting.test_accounts, ui_setting.test_pwd)
            msg = page.get_msg()
            assert '登录成功' == msg
            print_info_log('保存cookies到临时文件')
            cookies = driver.get_cookies()
            with open("temp/cookies/cookies.json", "w") as f:
                f.write(json.dumps(cookies))
        yield driver
        driver.quit()

    elif ui_setting.driver_type == "firefox":
        print_info_log('正在使用Firefox浏览器')
        driver = firefox_driver()
        print_debug_log(f'user_driver夹具正在访问主页{ui_setting.home_url}')
        driver.get(ui_setting.home_url)
        set_cookies(driver)  # 加载登录状态
        if not is_login(driver):
            print_info_log('正在重新登录')
            page = pom.HomePage(driver)
            page = page.to_login()  # 跳转到登录页面
            page.login(ui_setting.test_accounts, ui_setting.test_pwd)
            msg = page.get_msg()
            assert '登录成功' == msg
            print_info_log('保存cookies到临时文件')
            cookies = driver.get_cookies()
            with open("temp/cookies/cookies.json", "w") as f:
                f.write(json.dumps(cookies))
        yield driver
        driver.quit()

        if not is_login(driver):
            page = pom.HomePage(driver)
            page = page.to_login()  # 跳转到登录页面
            page.login(ui_setting.test_accounts, ui_setting.test_pwd)
            msg = page.get_msg()
            assert '登录成功' == msg
            print_info_log('保存cookies到临时文件')
            cookies = driver.get_cookies()
            with open("temp/cookies/cookies.json", "w") as f:
                f.write(json.dumps(cookies))
        yield driver
        driver.quit()


@pytest.fixture()
def clear_favor_driver(user_driver):
    user_driver.get('http://shop-xo.hctestedu.com/index.php?s=/index/usergoodsfavor/index.html')
    page = pom.UserGoodsFavor(user_driver)
    if page.ele_btn_check_all.is_enabled():
        page.delete_all()
        msg = page.get_msg()
        assert msg == "删除成功"
    else:
        pass
        yield user_driver




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
    num = ui_setting.logs_num_clear
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

