# -*- coding: utf-8 -*-
# Author:liu_ge
# @FileName: pom.py
# @Time : 2022/11/24 21:07
import random
import time
import allure
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from webdriver_helper import debugger
from core.setting import ui_setting
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from selenium.webdriver.common.action_chains import ActionChains
from utils.logger_utils import *
from utils.database_utils import DataBaseUtil


# class MyActionChains(ActionChains):
#     p_count = 1
#
#     def new_pointer(self):
#         """
#         创建一个新的指针
#         :return:
#         """
#         self.p_count += 1
#         pointer = self.w3c_actions.add_pointer_input("touch", f'p_{self.p_count}')
#         p_action = PointerActions(pointer)
#         return p_action


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

    @allure.step('元素文本断言')
    def key_assert_text(self, loc, expect_value):
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
        l_ = expect_value.split(":")
        if len(l_) == 1:
            l_.insert(0, "相等")  # 如果没有指定，默认为相等
        assert_type, expect_value, *_ = l_
        if assert_type == "相等":
            print_info_log('正在进行元素文本相等断言')
            try:
                self.driver.execute_script('arguments[0].style="border: 5px solid #f83030 ;"', ele)
            except Exception as e:
                print_info_log('不支持元素添加样式')
            ele_text = ele.text
            ele_text = ele_text.strip()
            expect_text = expect_value.strip()
            if ele_text == expect_text:
                print_info_log(f"断言成功,'{ele_text}'等于'{expect_text}'")
            assert ele_text == expect_text, print_error_log(f"断言失败,'{ele_text}'不等于'{expect_text}'")
        elif assert_type == "包含":
            print_info_log('正在进行元素文本包含断言')
            ele_text = ele.text
            ele_text = ele_text.strip()
            expect_text = expect_value.strip()
            if expect_text in ele_text:
                flag = True
                print_info_log("包含断言成功，当前步骤通过")
            else:
                flag = False
            assert flag, print_error_log("断言失败,'{}'不在'{}'中".format(expect_text, ele_text))

    @allure.step('源码包含断言')
    def key_assert_resource_contains_text(self, expect_text):
        print_info_log('正在进行源码包含断言')
        print_info_log(f"期望源码包含:{expect_text}")
        resource_text = self.driver.page_source
        if expect_text in resource_text:
            print_info_log("源码包含断言成功")
        else:
            assert 0, print_error_log(f'源码包含断言失败,"{expect_text}"不在源码中')

    def key_assert_database(self, sql, expect_value):
        """
        数据库断言方法
        :param sql: sql查询语句
        :param expect_value: 期望结果参数。默认为相等断言，如果想要做包含断言则语法为："包含:手机", 注意：excel表格里不用填双引号，其中的冒号是英文
        :return:
        """
        db = DataBaseUtil()
        actual_value = db.execute_sql(sql)
        sql_result_str = ','.join(actual_value)
        l_ = expect_value.split(":")
        if len(l_) == 1:
            l_.insert(0, "相等")  # 如果没有指定，默认为相等
        assert_type, expect_value, *_ = l_
        if assert_type == "相等":
            print_info_log('正在进行数据库相等断言')
            if sql_result_str == expect_value:
                print_info_log(f'数据库断言通过,"{expect_value}"等于"{sql_result_str}"')
            else:
                print_error_log(f'数据库断言失败,"{expect_value}"不等于"{sql_result_str}"')
        elif assert_type == "包含":
            print_info_log('正在进行数据库包含断言')
            if expect_value in sql_result_str:
                print_info_log(f'数据库断言通过,"{expect_value}"包含于"{sql_result_str}"')
            else:
                print_info_log(f'数据库断言失败,"{expect_value}"不包含在"{sql_result_str}"内')

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

    def key_sleep(self, time_):
        print_info_log(f'休眠{time_}秒')
        time.sleep(time_)

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
        # actions.w3c_actions.pointer_action.double_click(el)
        # actions.w3c_actions.pointer_action.release()
        actions.double_click(el)
        time.sleep(0.05)
        actions.release()
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

    def key_action_chains_keyboard(self, key_name, times=None):
        """
        键盘操作
        :param key_name: 键名
        :param times: 执行次数
        :return:
        """
        ac = ActionChains(self.driver)
        if key_name.islower() and len(key_name) == 1:
            print_error_log(f'如果想要输入字母按键，请将"{key_name}"大写')
        if key_name.isupper() and len(key_name) == 1:
            key_name = key_name.lower()
            if times:
                for i in range(1, times + 1):
                    ac.send_keys(key_name)
                    ac.perform()
                    time.sleep(0.2)
            elif not times:
                ac.send_keys(key_name)
                ac.perform()
                time.sleep(0.2)
        else:
            key_name = key_name.upper()  # 字串转大写
            if times:  # 如果有次数参数就循环操作
                for i in range(1, times + 1):
                    print_info_log(f'第{i}次按下{key_name}键')
                    keys = getattr(Keys, key_name)
                    ac.send_keys(keys)
                    ac.perform()
                    time.sleep(0.2)
                print_info_log(f'{key_name}键操作完成')
            elif not times:  # 没有次数参数就操作1次
                print_info_log(f'按下"{key_name}"键')
                keys = getattr(Keys, key_name)
                ac.send_keys(keys)
                ac.perform()
                print_info_log(f'"{key_name}"键操作完成')
                time.sleep(0.2)

    def key_keyboard_down(self, key_name):
        key_name = key_name.upper()  # 字串转大写
        ac = ActionChains(self.driver)
        keys = getattr(Keys, key_name)
        print_info_log(f'正在按下"{key_name}"键')
        ac.key_down(keys)
        ac.perform()

    def key_keyboard_up(self, key_name):
        key_name = key_name.upper()  # 字串转大写
        ac = ActionChains(self.driver)
        keys = getattr(Keys, key_name)
        print_info_log(f'正在抬起"{key_name}"键')
        ac.key_up(keys)
        ac.perform()

    def key_select_box(self, loc, select_args):
        """
        选择下拉菜单的关键字
        :param loc:
        :param select_args:select_by_visible_text->选项可视文本;select_by_index->选项索引;select_by_value->选项value.
        :return:
        """
        l_ = select_args.split(";;")
        if len(l_) == 1:
            l_.append("select_by_visible_text")  # 如果没有指定，默认为select_by_visible_text
        value, by, *_ = l_
        el = self.find_element(loc)
        select = Select(el)
        print_info_log(f'正在选择下拉菜单"{value}"')
        getattr(select, by)(value)
        print_info_log(f'选择下拉菜单"{value}"成功')

    def key_alert(self, btn_str=None):
        try:
            self.wait.until(ec.alert_is_present())
            alert = self.driver.switch_to.alert
            print_info_log('切换到alert')
        except:
            alert = self.wait.until(ec.alert_is_present())
            print_info_log('未切换成功,直接操作')
        finally:
            if btn_str == '确定' or btn_str == '确认' or btn_str == '同意' or btn_str is None:
                print_info_log('执行accept')
                alert.accept()
                time.sleep(3)
            elif btn_str == '取消' or btn_str == '拒绝':
                print_info_log('执行dismiss')
                alert.dismiss()
                time.sleep(3)

    @allure.step('切换窗口句柄')
    def key_switch_handles(self, index_num=None):
        handles = self.driver.window_handles
        # current_handle = self.driver.current_window_handle
        if not index_num:
            print_info_log(f'正在切换窗口句柄到handles:0')
            self.driver.switch_to.window(handles[0])
        else:
            print_info_log(f'正在切换窗口句柄到handles:{index_num}')
            self.driver.switch_to.window(handles[index_num])
        print_info_log('窗口句柄切换完成')

    def key_slider(self, slider, slider_bar, percent=None):
        """
        滑块拖动关键字
        :param slider: 滑块定位表达式
        :param slider_bar: 滑槽定位表达式
        :param percent: 滑动比例，例如：1或者0.6
        :return:
        """
        if percent:
            percent = float(percent)
        else:
            percent = int(1)
        slider_ele = self.find_element(slider)
        slider_bar_ele = self.find_element(slider_bar)
        print_info_log('正在计算滚动条需要拖动的行程')
        delta_x = slider_bar_ele.size['width'] * percent
        ac = ActionChains(self.driver)
        ac.click_and_hold(slider_ele).perform()
        i = 1
        total_length = 0
        while True:
            random_lens = random.randint(3, 15)
            print_info_log(f'正在拖动第{i}次')
            ac.move_by_offset(random_lens, 0).perform()
            print_info_log(f'本次拖动距离为{random_lens}个像素')
            total_length = total_length + random_lens  # 已拖动距离
            print_info_log(f'已拖动行程为{total_length}个像素')
            remainder_length = delta_x - total_length  # 剩余距离
            print_info_log(f'剩余行程为{remainder_length}个像素')
            time.sleep(0.07)
            if remainder_length < 0:
                print_info_log('完成拖动,准备释放鼠标')
                break
            i += 1
        print_info_log('正在释放鼠标')
        ActionBuilder(self.driver).clear_actions()

