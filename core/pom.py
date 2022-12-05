# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: pom.py
# @Time : 2022/11/24 21:07

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait



class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.check_element()

    def check_element(self):
        '''
        把属性中的字串变成真正的元素，检查是否有元素丢失
        :return:
        '''

        for attr in dir(self):
            if attr.startswith("ele_"):  # 我们自己定义的元素属性
                loc = getattr(self, attr)  # 获取属性内容
                el = self.find_element(By.XPATH, loc)  # 定位元素

                setattr(self, attr, el)  # 设置属性

    def find_element(self, *args):
        # 封装过的元素定位方法，自动使用显示等待
        print(f"正在定位元素{args}")
        el = self.wait.until(lambda _: self.driver.find_element(*args))
        print("元素定位成功")
        return el

    def _input(self, ele: WebElement, content=None):
        self.wait.until(lambda _: ele.is_enabled())
        ele.clear()
        if content is not None:
            ele.send_keys(content)

    def click(self, ele: WebElement):
        self.wait.until(lambda _: ele.is_enabled())
        ele.click()

    def get_msg(self):
        msg = self.wait.until(
            lambda _: self.driver.find_element(By.XPATH, '//*[@class="prompt-msg"]').text
        )
        return msg


class HomePage(BasePage):
    ele_a_login = '//*[text()="登录"]'
    ele_ipt_search = '//*[@id="search-input"]'
    ele_btn_search = '//*[@id="ai-topsearch"]'

    def to_login(self):
        # 跳转到登录页面
        self.click(self.ele_a_login)
        return LoginPage(self.driver)


class LoginPage(BasePage):
    ele_ipt_username = "//*[@name='accounts']"
    ele_ipt_password = "//*[@name='pwd']"
    ele_btn_submit = "//*[@type='submit' and text()='登录']"

    def login(self, username, password):
        self._input(self.ele_ipt_username, username)
        self._input(self.ele_ipt_password, password)
        self.click(self.ele_btn_submit)


class GoodsPage(BasePage):
    ele_btn_favor = "//*[text()='收藏']"  # 收藏按钮
    ele_text_favor = "//*[@class='goods-favor-count']"  # 收藏数量显示元素

    def favor(self):
        """进行收藏"""
        self.click(self.ele_btn_favor)

    def get_favor_count(self):
        """获取数量"""
        text = self.ele_text_favor.text
        text = text.replace("(", "").replace(")", "")
        value = int(text)
        return value


class UserGoodsFavor(BasePage):
    ele_btn_check_all = (
        "//button[text()='全选']"
    )
    ele_btn_delete = (
        '//*[contains(@data-confirm-msg,"删除后不可恢复")]'  # 删除按钮
        # '/html/body/div[4]/div[3]/div/div[2]/form/div[2]/button[1]'
    )
    loc_ele_btn_confirm = (
        '//span[text()="确定"]'
    )

    def delete_all(self):
        self.click(self.ele_btn_check_all)
        self.click(self.ele_btn_delete)
        # loc前缀的元素不会自动定位
        self.click(self.find_element(By.XPATH, self.loc_ele_btn_confirm))
