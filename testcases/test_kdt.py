# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test_kdt.py
# @Time : 2022/11/26 10:58
import time
from logs.log import logger
import pytest
from core.kdt import KeyWord

huace = 'http://shop-xo.hctestedu.com/index.php'
mashang = 'http://101.34.221.219:8010/'


# def test_login(driver):
#     kw = KeyWord(driver)
#     kw.get_page(huace)
#     kw.key_click('//*[text()="登录"]')
#     kw.key_input("//*[@name='accounts']", "liuge002")
#     kw.key_input("//*[@name='pwd']", "liuge666")
#     kw.key_click("//button[contains(@excel_data-am-loading,'{load') and text()='登录']")
#     kw.key_assert_equal_text('//*[@class="prompt-msg"]', "登录成功")
#
#
# def test_goods_favor(clear_favor_driver):
#     kw = KeyWord(clear_favor_driver)
#     kw.key_get_page("http://shop-xo.hctestedu.com/index.php?s=/index/goods/index/id/1.html")
#     kw.key_click("//*[text()='收藏']")
#     kw.key_assert_equal_text('//*[@class="prompt-msg"]', "收藏成功")
# # #
#
# def test_update_userinfo(user_driver):
#     kw = KeyWord(user_driver)
#     kw.get_page('http://shop-xo.hctestedu.com/index.php?s=/index/personal/index.html')
#     kw.key_click("//*[contains(text(),'编辑')]")
#     kw.key_input("//*[contains(@placeholder,'昵称')]", "liuge666")
#     kw.key_click("//button[@class='am-close']")
#     kw.key_click("//*[@class='am-radio-inline am-margin-right-sm'][3]")
#     kw.key_input("//*[@name='birthday']", "2020-5-10")
#     kw.key_click("//*[text()='保存']")

    # kw.key_assert_equal_text('//*[@class="prompt-msg"]', "编辑成功")

# @pytest.mark.repeat(1)
# def test_update_user_avatar(user_driver):
#     kw = KeyWord(user_driver)
#     kw.key_get_page("http://shop-xo.hctestedu.com/index.php?s=/index/personal/index.html")
#     # 元素不可交互，因为元素不可见，解决办法：修改css position static
#     kw.key_click("//*[text()='修改']")
#     kw.key_js_code('//*[@id="user-avatar-popup"]/div/div[2]/form/div[2]/div/input',
#                    'arguments[0].style="position: static;"')
#     kw.key_input('//*[@id="user-avatar-popup"]/div/div[2]/form/div[2]/div/input', 'D:\\1.png')
#
#     kw.key_click("//*[text()='确认上传']")
#     kw.key_assert_equal_text('//*[@class="prompt-msg"]', "上传成功")
