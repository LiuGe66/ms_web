import os
import pytest
from core.setting import ui_setting

if __name__ == '__main__':
    pytest.main()
    os.system('allure generate temp/allure -o report --clean')
    # if ui_setting.allure_show:
    #     os.system('allure open report -p 9022')
