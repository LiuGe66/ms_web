import os
import pytest
from core.setting import settings

if __name__ == '__main__':
    pytest.main()
    os.system('allure generate temp/allure_node2/ -o ./testcases/node2_report/ --clean')
    # if settings.allure_show:
    #     os.system('allure open report -p 9022')
