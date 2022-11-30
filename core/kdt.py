# -*- coding: utf-8 -*-
# Author:liu_ge
# @FileName: pom.py
# @Time : 2022/11/24 21:07
from logs.log import logger
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from core.setting import ui_setting


class KeyWord:

    def __init__(self, driver: WebDriver = None, request=None):
        self.request = request  # pytest和关键字驱动建立联系
        if driver:
            self.set_driver(driver)

    def set_driver(self, driver: WebDriver):
        logger.debug('为kw类设置driver')
        self.driver = driver
        print('999999999999999999999999999999')

        self.wait = WebDriverWait(driver, ui_setting.wait_max, poll_frequency=ui_setting.wait_poll)
        # self.wait = WebDriverWait(driver, 10)

    def get_kw_method(self, key):

        f = getattr(self, f"key_{key}", None)
        if not f:
            raise AssertionError(f"不存在的关键字：{key}")
        return f

    @allure.step('元素定位')
    def find_element(self, *args):
        # 封装过的元素定位方法，自动使用显式等待
        try:
            logger.info(f"正在定位元素{args}")
            print(f"正在定位元素{args}")
            el: WebElement = self.wait.until(lambda _: self.driver.find_element(*args))
            self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', el)
            logger.info(f"{el.tag_name}元素定位成功,位置：{el.rect}")
            print(f"{el.tag_name}元素定位成功,位置：{el.rect}")
            return el
        except Exception as e:
            logger.warning(f"元素{args}定位失败")
            print(f"元素{args}定位失败")

    def key_input(self, loc, content=None):
        ele = self.find_element(By.XPATH, loc)
        self.wait.until(lambda _: ele.is_enabled())
        try:
            ele.clear()
        except:
            print("清除元素文本失败")
        if content is not None:
            logger.info(f'正在输入文本:{content}')
            print(f'正在输入文本:{content}')
            ele.send_keys(content)

    def key_upload(self, loc, file):
        ele = self.find_element(By.XPATH, loc)
        self.wait.until(lambda _: ele.is_enabled())
        if file is not None:
            logger.info(f'正在上传文件:{file}')
            print(f'正在上传文件:{file}')
            ele.send_keys(file)
        else:
            logger.info('文件地址为空')
            print('文件地址为空')

    def key_js_code(self, loc, code):
        ele = self.find_element(By.XPATH, loc)
        logger.info(f'正在执行JS脚本:{code}')
        print(f'正在执行JS脚本:{code}')
        self.driver.execute_script(code, ele)

    def key_click(self, loc):
        ele = self.find_element(By.XPATH, loc)
        self.wait.until(lambda _: ele.is_enabled())
        self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
        logger.info(f'正在点击:{loc}')
        print(f'正在点击:{loc}')
        ele.click()

    def key_new_driver(self):
        driver = webdriver.Chrome()
        self.set_driver(driver)

    def key_get_page(self, url):
        self.driver.get(url)
        logger.info(f'正在访问网址:{url}')
        print(f'正在访问网址:{url}')

    @allure.step('文本相等断言')
    def key_assert_equal_text(self, loc, expect_text):
        ele = self.wait.until(
            lambda _: self.driver.find_element(By.XPATH, loc)
        )
        self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
        ele_text = ele.text
        ele_text = ele_text.strip()
        expect_text = expect_text.strip()
        logger.info(f'实际结果:{ele_text}')
        print(f'实际结果:{ele_text}')
        logger.info(f"期望结果:{expect_text}")
        print(f"期望结果:{expect_text}")
        if ele_text == expect_text:
            logger.info("相等断言成功，测试通过")
            print("相等断言成功，测试通过")
        assert ele_text == expect_text, logger.warning("断言失败,'{}'不等于'{}'".format(ele_text, expect_text))

    @allure.step('文本包含断言')
    def key_assert_contains_text(self, loc, expect_text):
        ele = self.wait.until(
            lambda _: self.driver.find_element(By.XPATH, loc)
        )
        self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
        ele_text = ele.text
        ele_text = ele_text.strip()
        expect_text = expect_text.strip()
        logger.info(f'实际结果:{ele_text}')
        print(f'实际结果:{ele_text}')
        logger.info(f"期望结果:{expect_text}")
        print(f"期望结果:{expect_text}")
        if expect_text in ele_text:
            flag = True
            logger.info("包含断言成功，测试通过")
            print("包含断言成功，测试通过")
        else:
            flag = False
        assert flag, logger.warning("断言失败,'{}'不在'{}'中".format(expect_text, ele_text))

    def key_driver_fixture(self, fixture_name):
        """
        使用pytest的fixture作用kw的driver
        :param fixture_name:
        :return:
        """
        driver = self.request.getfixturevalue(fixture_name)  # 根据字符串来启动夹具
        self.set_driver(driver)
