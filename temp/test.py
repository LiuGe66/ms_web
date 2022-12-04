# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test.py
# @Time : 2022/12/2 21:51

from appium.webdriver import Remote
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

caps = {
    # "platformName": "Android",
    # "platformVersion": "10",
    # "deviceName": "CUYDU19625011655",
    # "app": "/Users/mrding/automaster_release_1.3.apk",
    "appium:platformName": "Android",
    "appium:deviceName": "1a44c444fb0b7ece",
    "appium:appPackage": "com.automaster.practice.through",
    "appium:appActivity": ".MainActivity",
    "appium:platformVersion": "10.0",
    "appium:noReset": "true",
    "appium:dontStopAppOnReset": True
}
driver = Remote("http://127.0.0.1:4723/wd/hub", caps)

# driver.find_element(By.ID, "com.automaster.practice.through:id/btn_next")

wait = WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((MobileBy.ID, "com.automaster.practice.through:id/btn_next"))).click()
txt = wait.until(ec.visibility_of_element_located((MobileBy.ID, "com.automaster.practice.through:id/textView4"))).text

ele = wait.until(ec.visibility_of_element_located((MobileBy.ID, "com.automaster.practice.through:id/text_input")))
ele.clear()
ele.send_keys(txt)

wait.until(ec.visibility_of_element_located((MobileBy.ID, "com.automaster.practice.through:id/btn_next"))).click()
print(driver.page_source)  # 通过这个进行调试
wait = WebDriverWait(driver, 5, 0.1)
txt = wait.until(ec.presence_of_element_located((MobileBy.XPATH, "//android.widget.Toast"))).text
print(txt)