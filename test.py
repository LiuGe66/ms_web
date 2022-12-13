#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import os
# import webdriver_helper
# from selenium import webdriver
# from time import sleep
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait
# from webdriver_helper import debugger
#
# options = webdriver.ChromeOptions()
# # os.popen("D:\\tools\\chrome.bat")
# # options.debugger_address = "127.0.0.1:9222"
# driver = webdriver_helper.get_webdriver()
# driver.get('http://vip.ytesting.com/')
# driver.find_element(By.XPATH, '//*[@id="password"]')
# debugger(driver)
class Ttt:
    def a(self):
        pass

    def b(self):
        pass

    def c(self):
        pass


def get_methods(self):
    return list(filter(lambda methods: not methods.startswith("_") and callable(getattr(self, methods)), dir(self)))


if __name__ == '__main__':
    print(get_methods(Ttt))