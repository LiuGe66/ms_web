# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: conftest.py
# @Time : 2022/11/24 16:15
import json
import time
from pathlib import Path
import pytest
from selenium import webdriver
from core import pom
from core.setting import ui_setting
from selenium.webdriver.firefox.options import Options
from logs.log import logger


def chrome_no_gui_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # options.add_argument('--incognito')
    # options.add_argument('disable-cache')
    no_gui_driver = webdriver.Chrome(chrome_options=options)
    return no_gui_driver


def firefox_no_gui_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    no_gui_driver = webdriver.Firefox(options=options)
    return no_gui_driver


@pytest.fixture(scope="class")
def driver():
    if not ui_setting.cap_png:
        logger.info('截图功能已关闭')
        print('截图功能已关闭')
    if ui_setting.driver_type == "firefox":
        logger.info('正在使用Firefox浏览器')
        print('正在使用Firefox浏览器')
        if not ui_setting.gui:
            driver_ = firefox_no_gui_driver()
            logger.info('正在以无界面模式运行浏览器')
            print('正在以无界面模式运行浏览器')
            if ui_setting.window_max:
                driver_.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            yield driver_
            driver_.quit()
        elif ui_setting.gui:
            driver_ = webdriver.Firefox()
            if ui_setting.window_max:
                driver_.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            yield driver_
            driver_.quit()
    elif ui_setting.driver_type == "chrome":

        logger.info('正在使用Chrome浏览器')
        print('正在使用Chrome浏览器')
        if not ui_setting.gui:
            driver_ = chrome_no_gui_driver()
            logger.info('正在以无界面模式运行浏览器')
            print('正在以无界面模式运行浏览器')
            if ui_setting.window_max:
                driver_.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            yield driver_
            driver_.quit()
        elif ui_setting.gui:
            driver_ = webdriver.Chrome()
            if ui_setting.window_max:
                driver_.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            yield driver_
            driver_.quit()
            time.sleep(0.5)


def set_cookies(driver):
    cookies = []
    path = Path('temp/cookies/cookies.json')
    if path.exists():
        cookies = json.loads(path.read_text())

    logger.info(f"加载cookies{cookies}")
    for cookie in cookies:
        driver.add_cookie(cookie)
        logger.info(f"设置cookie:{cookie}")

    driver.get(ui_setting.home_url)


def is_login(driver):
    return "退出" in driver.page_source


@pytest.fixture(scope='session')
def user_driver():
    """
    返回已登录状态的浏览器
    :return:
    """
    if not ui_setting.cap_png:
        logger.info('截图功能已关闭')
        print('截图功能已关闭')
    if ui_setting.driver_type == "chrome":
        logger.info('正在使用Chrome浏览器')
        print('正在使用Chrome浏览器')
        if not ui_setting.gui:
            driver = chrome_no_gui_driver()
            logger.info('正在以无界面模式运行浏览器')
            print('正在以无界面模式运行浏览器')
            if ui_setting.window_max:
                driver.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            driver.get(ui_setting.home_url)
            set_cookies(driver)  # 加载登录状态

            if not is_login(driver):
                page = pom.HomePage(driver)
                page = page.to_login()  # 跳转到登录页面
                page.login(ui_setting.test_accounts, ui_setting.test_pwd)
                msg = page.get_msg()
                assert '登录成功' == msg
                # 保存cookies到临时文件
                cookies = driver.get_cookies()
                with open("temp/cookies/cookies.json", "w") as f:
                    f.write(json.dumps(cookies))

            yield driver
            driver.quit()
        elif ui_setting.gui:
            driver = webdriver.Chrome()
            if ui_setting.window_max:
                driver.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            driver.get(ui_setting.home_url)
            set_cookies(driver)  # 加载登录状态

            if not is_login(driver):
                page = pom.HomePage(driver)
                page = page.to_login()  # 跳转到登录页面
                page.login(ui_setting.test_accounts, ui_setting.test_pwd)
                msg = page.get_msg()
                assert '登录成功' == msg
                # 保存cookies到临时文件
                cookies = driver.get_cookies()
                with open("temp/cookies/cookies.json", "w") as f:
                    f.write(json.dumps(cookies))
            yield driver
            driver.quit()

    elif ui_setting.driver_type == "firefox":
        logger.info('正在使用Firefox浏览器')
        print('正在使用Firefox浏览器')
        if not ui_setting.gui:
            driver = firefox_no_gui_driver()
            logger.info('正在以无界面模式运行浏览器')
            print('正在以无界面模式运行浏览器')
            if ui_setting.window_max:
                driver.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            driver.get(ui_setting.home_url)
            set_cookies(driver)  # 加载登录状态

            if not is_login(driver):
                page = pom.HomePage(driver)
                page = page.to_login()  # 跳转到登录页面
                page.login(ui_setting.test_accounts, ui_setting.test_pwd)
                msg = page.get_msg()
                assert '登录成功' == msg
                # 保存cookies到临时文件
                cookies = driver.get_cookies()
                with open("temp/cookies/cookies.json", "w") as f:
                    f.write(json.dumps(cookies))

            yield driver
            driver.quit()
        elif ui_setting.gui:
            driver = webdriver.Firefox()
            if ui_setting.window_max:
                driver.maximize_window()
                logger.info('正在以最大化窗口运行浏览器')
                print('正在以最大化窗口运行浏览器')
            driver.get(ui_setting.home_url)
            set_cookies(driver)  # 加载登录状态

            if not is_login(driver):
                page = pom.HomePage(driver)
                page = page.to_login()  # 跳转到登录页面
                page.login(ui_setting.test_accounts, ui_setting.test_pwd)
                msg = page.get_msg()
                assert '登录成功' == msg
                # 保存cookies到临时文件
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
