# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: pom.py
# @Time : 2022/12/15 1:37
from core.kdt import KeyWord


class LoginPage(KeyWord):
    def login(self,url,username,password):
        self.key_get_page(url)
        