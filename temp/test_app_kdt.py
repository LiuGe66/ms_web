# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test_app_kdt.py
# @Time : 2022/12/2 17:05
import time
from time import sleep
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from core.kdt import KeyWord
from selenium.webdriver import ActionChains


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


def test_app(start_app):
    title_path = "//*[@class='android.widget.TextView' and contains(@text,'第')]"
    kw = KeyWord(start_app)

    # 开始
    # kw.key_click("com.automaster.practice.through:id/btn_next;;ID")
    # kw.key_assert_contains_text(title_path, "第一关")
    # # 第一关
    # print("进入第一关")
    # kw.key_var_save("com.automaster.practice.through:id/textView4;;ID", "V1")
    # kw.key_var_input("com.automaster.practice.through:id/text_input;;ID", "V1")
    # kw.key_click("com.automaster.practice.through:id/btn_next;;ID")
    # kw.key_assert_contains_text(title_path, "第二关")
    # print("第一关通过")
    # # 第二关
    # print("进入第二关")
    # kw.key_var_save("/hierarchy/android.widget.Toast", "V2")
    # kw.key_var_input("com.automaster.practice.through:id/text_input;;ID", "V2")
    # kw.key_click("com.automaster.practice.through:id/btn_next;;ID")
    # kw.key_assert_contains_text(title_path, "第三关")
    # print("第二关通过")
    #
    # print("进入第三关")
    # kw.key_context("WEBVIEW_com.automaster.practice.through")  # 切换到webview
    # kw.key_var_save("/html/body/p", "V3")
    # start_app.switch_to.context("NATIVE_APP")  # 回到原生app
    # kw.key_var_input("com.automaster.practice.through:id/text_input;;ID", "V3")
    # kw.key_assert_contains_text(title_path, "第四关")
    # print("第三关通过")
    #
    print("进入第四关")
    ele = kw.find_element("com.automaster.practice.through:id/btn_next;;ID")
    ac = ActionChains(start_app)
    ac.move_to_element(ele)  # 光标移动
    ac.w3c_actions.pointer_action.pointer_down()  # 按下鼠标
    ac.w3c_actions.pointer_action.pause(1.5)  # 等待1秒
    ac.w3c_actions.pointer_action.release()  # 抬起鼠标
    ac.perform()
    kw.key_assert_contains_text(title_path, "第五关")
    print('第四关通过')

    print('进入第五关')
    # el = kw.find_element("com.automaster.practice.through:id/textView;;ID")
    # print(el.rect)
    start_x, start_y = 2590, 580
    end_x, end_y = 630, 480

    ac.w3c_actions.pointer_action.move_to_location(start_x, start_y)  # 移动到指定位置
    print('移动到指定位置')
    ac.w3c_actions.pointer_action.pointer_down()  # 按下
    print('按下')
    ac.w3c_actions.pointer_action.move_to_location(end_x, end_y)  # 滑动
    print("滑动")
    ac.w3c_actions.pointer_action.release()  # 抬起鼠标
    print("抬起")
    ac.perform()

    # kw.key_assert_contains_text(title_path, "第六关")
    # print('第五关通过')
    #
    # print('进入第六关')
    #
    # p_l = [
    #     (270, 1290),
    #     (710, 1290),
    #     (1150, 1290),
    #     (270, 1640),
    #     (710, 1640),
    #     (1140, 1640),
    #     (270, 2100),
    #     (710, 2100),
    #     (1160, 2100)
    # ]
    # password = "321456987"
    # num = len(password)
    # for i, p in enumerate(password):
    #     index = int(p) - 1
    #     print()
    #     x, y = p_l[index]
    #     # print(f'{x=},{y=}')
    #     ac.w3c_actions.pointer_action.move_to_location(x, y)
    #     if i == 0:
    #         print('按下手指')
    #         ac.w3c_actions.pointer_action.pointer_down()
    # print('抬起手指')
    # ac.w3c_actions.pointer_action.release()
    # ac.perform()
    # kw.key_assert_contains_text(title_path, "第七关")
    # print('第六关测试通过')

#
# def test_2(use_app):
#     title_path = "//*[@class='android.widget.TextView' and contains(@text,'第')]"
#     kw = KeyWord(use_app)
#     ac = MyActionChains(use_app)
#     el_1 = kw.find_element("com.automaster.practice.through:id/btn_me;;ID")
#     p_1 = ac.new_pointer()
#     # p_1.click(el_1)  # 点击第一个元素
#     # 修改后的
#     p_1.move_to(el_1)
#     p_1.pointer_down()
#     p_1.pause(0.2)
#     p_1.pointer_up()
#
#     el_2 = kw.find_element("com.automaster.practice.through:id/btn_next;;ID")
#     p_2 = ac.new_pointer()
#     # p_2.click(el_2)  # 点击第二个元素
#     p_2.move_to(el_2)
#     p_2.pointer_down()
#     p_2.pause(0.2)
#     p_2.pointer_up()
#
#     ac.perform()
#
#     kw.key_assert_contains_text(title_path, "第八关")
#
#     # ac = MyActionChains(use_app)
#     # ac.w3c_actions.pointer_action.move_to()
#     #
#     # p_2 = ac.new_pointer()
#     # p_2.move_to()
#     # p_2.click()
#
#     print('进入第八关')
#
#
# def test_3(use_app):
#     kw = KeyWord(use_app)
#     packagename = use_app.current_package
#     activityname = use_app.current_activity
#     print(f'当前的包是：{packagename}')
#     print(f'当前的Activity是：{use_app.current_activity}')
#     use_app.start_activity(packagename, "NewActivity")
#     print("启动新的activity")
#
#
# def test_4(use_app):
#     res = use_app.execute_script('mobile:exeEmuConsoleCommand', {
#         "command": "sensor set acceleration 10:20:30",
#         # "args": "-lha"
#     })
#     print(res)
#
#     res = use_app.execute_script('mobile:exeEmuConsoleCommand', {
#         "command": "sensor set acceleration 0:1:-30",
#         # "args": "-lha"
#     })
#     print(res)
