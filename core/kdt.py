# -*- coding: utf-8 -*-
# Author:liu_ge
# @FileName: pom.py
# @Time : 2022/11/24 21:07
import inspect
import time
import allure
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from core.setting import ui_setting
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from selenium.webdriver.common.action_chains import ActionChains

from logs.logger_utils import *


class MyActionChains(ActionChains):
    p_count = 1

    def new_pointer(self):
        """
        创建一个新的指针
        :return:
        """
        self.p_count += 1
        pointer = self.w3c_actions.add_pointer_input("touch", f'p_{self.p_count}')
        p_action = PointerActions(pointer)
        return p_action


class KeyWord:

    def __init__(self, driver: WebDriver = None, request=None):
        self.request = request  # pytest和关键字驱动建立联系
        if driver:
            self.set_driver(driver)
        self.vars = {}  # 用来存放临时变量

    def set_driver(self, driver: WebDriver):
        print_debug_log('为kw类设置driver')
        self.driver = driver
        self.wait = WebDriverWait(driver, ui_setting.wait_max, poll_frequency=ui_setting.wait_poll)

    def get_kw_method(self, key):
        f = getattr(self, f"key_{key}", None)
        if not f:
            raise AssertionError(f"不存在的关键字：{key}")
        return f

    def key_input(self, loc, content=None):
        ele = self.find_element(loc)
        self.wait.until(lambda _: ele.is_enabled())
        try:
            ele.clear()
        except:
            print_info_log("清除元素文本失败")
        if content is not None:
            print_info_log(f'正在输入文本:{content}')
            ele.send_keys(content)

    def key_upload(self, loc, file):
        ele = self.find_element(loc)
        self.wait.until(lambda _: ele.is_enabled())
        if file is not None:
            print_info_log(f'正在上传文件:{file}')
            ele.send_keys(file)
        else:
            print_info_log('文件地址为空')

    def key_js_code(self, loc, code):
        ele = self.find_element(loc)
        print_info_log(f'正在执行JS脚本:{code}')
        self.driver.execute_script(code, ele)

    def key_click(self, loc):
        ele = self.find_element(loc)
        self.wait.until(lambda _: ele.is_enabled())
        try:
            self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
        except Exception as e:
            print_info_log('不支持元素添加样式')
        print_info_log(f'正在点击:{loc}')
        ele.click()
        print_info_log(f'点击成功:{loc}')

    def key_new_driver(self):
        driver = webdriver.Chrome()
        self.set_driver(driver)

    def key_get_page(self, url):
        self.driver.get(url)
        print_info_log(f'正在访问网址:{url}')

    @allure.step('元素定位')
    def find_element(self, loc):
        # 将字符串解析为by+value
        # 封装过的元素定位方法，自动使用显式等待
        l_ = loc.split(";;")
        if len(l_) == 1:
            l_.append("XPATH")  # 如果没有指定，默认为XPATH
        value, by, *_ = l_
        by = getattr(AppiumBy, by)

        try:
            print_info_log(f"正在定位元素{loc=}")
            el: WebElement = self.wait.until(lambda _: self.driver.find_element(by, value))
            try:
                self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', el)
            except Exception as e:
                print_info_log('不支持元素添加样式')
            if el.tag_name:
                print_info_log(f"{el.tag_name}元素定位成功,位置：{el.rect}")
            else:
                print_info_log(f"{el.text}元素定位成功,位置：{el.rect}")
            return el
        except Exception as e:
            print_error_log(f"元素{loc=}定位失败")
            raise e

    @allure.step('文本相等断言')
    def key_assert_equal_text(self, loc, expect_text):
        ele = self.wait.until(
            lambda _: self.find_element(loc)
        )
        try:
            self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
        except Exception as e:
            print_info_log('不支持元素添加样式')
        ele_text = ele.text
        ele_text = ele_text.strip()
        expect_text = expect_text.strip()
        print_info_log(f"期望结果:{expect_text}")
        if ele_text == expect_text:
            print_info_log("相等断言成功，当前步骤测试通过")
        assert ele_text == expect_text, print_error_log("断言失败,'{}'不等于'{}'".format(ele_text, expect_text))

    @allure.step('文本包含断言')
    def key_assert_contains_text(self, loc, expect_text):
        print_info_log('正在进行文本包含断言')
        try:
            ele = self.wait.until(
                lambda _: self.find_element(loc)
            )
        except Exception as e:
            raise e
        try:
            self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
        except Exception as e:
            print_info_log('不支持元素添加样式')

        ele_text = ele.text
        ele_text = ele_text.strip()
        expect_text = expect_text.strip()
        print_info_log(f'实际结果:{ele_text}')
        print_info_log(f"期望结果:{expect_text}")
        if expect_text in ele_text:
            flag = True
            print_info_log("包含断言成功，当前步骤通过")
        else:
            flag = False
        assert flag, print_error_log("断言失败,'{}'不在'{}'中".format(expect_text, ele_text))

    def key_driver_fixture(self, fixture_name):
        """
        使用pytest的fixture作为kw的driver
        :param fixture_name:
        :return:
        """
        driver = self.request.getfixturevalue(fixture_name)  # 根据字符串来启动夹具
        self.set_driver(driver)

    @allure.step('切换上下文')
    def key_context(self, context_name):
        print_info_log(f'所有的上下文：{self.driver.contexts}')
        self.driver.switch_to.context(context_name)
        print_info_log(f"上下文切换成功：{context_name}")

    @allure.step('保存变量')
    def key_var_save(self, loc, var_name):
        if "oast" in loc:
            ele = self.find_element_toast(loc)
        else:
            ele = self.find_element(loc)
        text = ele.text
        self.vars[var_name] = text
        print_info_log(f"保存变量{var_name} = {text}成功")

    @allure.step('输入变量')
    def key_var_input(self, loc, var_name):
        value = self.vars.get(var_name)
        print_info_log(f'取出变量{var_name} = {value}')
        self.key_input(loc, value)
        print_info_log(f'已输入变量{var_name} = {value}')

    def find_element_toast(self, loc):
        """
        专门为Toast消息封装的查找方法
        :param loc: 定位表达式
        :return: 返回查找到的元素对象
        """
        wait = WebDriverWait(self.driver, 5, 0.1)
        print_info_log("正在定位Toast元素")
        el = wait.until(ec.presence_of_element_located((MobileBy.XPATH, loc)))
        print_info_log("Toast元素定位成功")
        return el

    def key_absolutely_swipe(self, start_coord, end_coord, times):
        """
        根据给定坐标进行滑动
        :param start_coord: 起始坐标
        :param end_coord: 结束坐标
        :param times: 滑动次数
        :return: None
        """
        l_start = start_coord.split(",")
        start_x, start_y, *_ = l_start
        l_end = end_coord.split(",")
        end_x, end_y, *_ = l_end
        ac = ActionChains(self.driver)
        for i in range(1, times + 1):
            ac.w3c_actions.pointer_action.move_to_location(start_x, start_y)  # 移动到指定位置
            print_info_log(f'移动到指定起点{start_coord}')
            time.sleep(0.1)
            ac.w3c_actions.pointer_action.pointer_down()  # 按下
            print_info_log('光标按下')
            ac.w3c_actions.pointer_action.move_to_location(end_x, end_y)  # 滑动
            print_info_log('正在滑动')
            ac.w3c_actions.pointer_action.release()  # 抬起鼠标
            print_info_log(f'光标从{end_coord}抬起')
            ac.perform()
            print_info_log(f'第{i}次滑动完成')
        print_info_log('滑动操作完成')

    def key_repeat_click_ele(self, loc, times):
        el = self.find_element(loc)
        actions = ActionChains(self.driver)
        print_info_log('正在执行重复点击')
        for i in range(1, times + 1):
            print_info_log(f'第{i}次点击')
            actions.w3c_actions.pointer_action.click_and_hold(el)
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            # time.sleep(0.3)
            actions.perform()

    def key_relative_swipe(self, direction, times):
        """
        相对滑动方法
        :param direction: 需要滑动的方向
        :param times: 需要滑动的次数
        :return: None
        """
        size = self.driver.get_window_size()
        x = size['width']
        y = size['height']
        if direction == 'right':
            print_info_log('正在向右滑动屏幕')
            for i in range(1, times + 1):
                self.driver.swipe(x * 0.2, y * 0.5, x * 0.95, y * 0.5, 700)
                print_info_log(f'正在滑动第{i}次')
                time.sleep(0.2)
            print_info_log('滑动结束')
        elif direction == 'left':
            print_info_log('正在向左滑动屏幕')
            for i in range(1, times + 1):
                self.driver.swipe(x * 0.8, y * 0.5, x * 0.05, y * 0.5, 700)
                print_info_log(f'正在滑动第{i}次')
                time.sleep(0.2)
            print_info_log('滑动结束')
        elif direction == 'up':
            print_info_log('正在向上滑动屏幕')
            for i in range(1, times + 1):
                self.driver.swipe(x * 0.5, y * 0.8, x * 0.5, y * 0.2, 700)
                print_info_log(f'正在滑动第{i}次')
                time.sleep(0.2)
            print_info_log('滑动结束')
        elif direction == 'down':
            print_info_log('正在向下滑动屏幕')
            for i in range(1, times + 1):
                self.driver.swipe(x * 0.5, y * 0.2, x * 0.5, y * 0.8, 700)
                print_info_log(f'正在滑动第{i}次')
                time.sleep(0.2)
            print_info_log('滑动结束')

    def key_long_press_ele(self, loc, duration):
        el = self.find_element(loc)
        actions = ActionChains(self.driver)
        print_info_log('正在按下并保持')
        actions.w3c_actions.pointer_action.click_and_hold(el)
        actions.w3c_actions.pointer_action.pause(duration)
        print_info_log('光标已释放')
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print_info_log('长按已结束')

    def key_double_click_ele(self, loc):  # 待验证，执行会报错.............................
        el = self.find_element(loc)
        actions = ActionChains(self.driver)
        print_info_log('正在双击元素')
        actions.w3c_actions.pointer_action.double_click(el)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print_info_log('双击成功')
        # actions = ActionChains(self.driver)
        # actions.move_to_element(el)
        # print_info_log('正在双击元素')
        # actions.double_click()
        # actions.perform()
        # print_info_log('双击元素完成')
    def key_key_event(self, event_code):
        keycode_list = {
            "5": "拨号键",
            "6": "挂机键",
            "3": "Home键",
            "26": "电源键",
            "4": "返回键",
            "82": "菜单键",
            "27": "拍照键",
            "91": "话筒静音键",
            "164": "扬声器静音键",
            "24": "音量增加键",
            "25": "音量减小键",
            "23": "导航键 确定键",
            "92": "向上翻页键",
            "93": "向下翻页键",
            "67": "退格键",
            "112": "删除键",
        }
        key_name = keycode_list[str(event_code)]
        print_info_log(f'正在执行{key_name}事件')
        self.driver.keyevent(event_code)
        time.sleep(0.5)

    def key_un_lock(self, key):
        actions = ActionChains(self.driver)

        p_l = [
            (380, 1666),
            (718, 1666),
            (1055, 1666),
            (380, 2000),
            (710, 1640),
            (718, 2000),
            (380, 2341),
            (713, 2345),
            (1060, 2340)
        ]
        password = str(key)
        print_info_log('正在解锁九宫格')
        for i, p in enumerate(password):  # 枚举循环
            index = int(p) - 1  # 取出密码图案每个点位的下标
            x, y = p_l[index]
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            if i == 0:
                print_info_log('按下手指')
                actions.w3c_actions.pointer_action.pointer_down()
        print_info_log('抬起手指')
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        print_info_log('九宫格解锁完毕')
