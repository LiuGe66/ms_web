# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: test_excel.py
# @Time : 2022/11/27 11:48
from pathlib import Path
from core.excel_kdt import data_by_excel, create_case
from logs.logger_utils import *

test_dir = Path(__file__).parent.parent / 'excel_data/'
file_list = test_dir.glob('test_*.xlsx')  # 自动收集excel文件
_case_count = 0  # 用例数量
for file in file_list:
    data = data_by_excel(file)

    for case, suite_name in create_case(data, file):
        _case_count += 1
        globals()[f"Test_{_case_count}_{suite_name}"] = case
print_debug_log("所有excel文件测试用例生成完成")
