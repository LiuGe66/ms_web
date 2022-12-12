# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test.py
# @Time : 2022/12/8 17:12
list1=["张三",'李四','王五']

gen=(name for name in list1)
print(next(gen))
print(next(gen))
print(next(gen))
