# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test_pom.py
# @Time : 2022/11/24 22:38
from logs.log import logger
import pytest
from core import pom


# @pytest.mark.skip
# def test_login(driver):
#     logger.info("-----------------测试用例开始执行-----------------")
#     # driver.get("http://shop-xo.hctestedu.com/")
#     driver.get("http://101.34.221.219:8010/")
#
#     page = pom.HomePage(driver)
#     page = page.to_login()  # 跳转到登录页面
#     page.login('liuge002', 'liuge666')
#     msg = page.get_msg()
#     assert '登录成功' == msg
#
#
# def test_goods_favor(user_driver, clear_favor):
#     """
#
#     :param user_driver: 已登录的浏览器
#     :param clear_favor: 清除收藏的端口
#     :return:
#     """
#     # user_driver.get('http://shop-xo.hctestedu.com/index.php?s=/index/goods/index/id/2.html')
#     user_driver.get('http://101.34.221.219:8010/?s=goods/index/id/5.html')
#     page = pom.GoodsPage(user_driver)  # 进行元素自动定位
#     favor_count = page.get_favor_count()  # 获取旧的收藏数量
#     page.favor()  # UI交互
#     msg = page.get_msg()
#     assert msg == '收藏成功'
#     new_favor_count = page.get_favor_count()  # 获取新的收藏数量
#     assert new_favor_count == favor_count + 1


