# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: database_utils.py
# @Time : 2022/11/11 19:22
import os
import pymysql
import yaml


class DataBaseUtil:
    def get_new_path(self):
        return os.getcwd().split("utils")[0]
    # 读取配置文件数据：
    def read_database_config(self, one_key):
        with open(os.getcwd() + "/utils/config.yaml", mode="r", encoding="utf-8") as f:
            result = yaml.load(stream=f, Loader=yaml.FullLoader)
            return result[one_key]

    # 创建连接
    def create_conn(self):
        conf = self.read_database_config("database_config")
        self.conn = pymysql.connect(
            host=conf['host'],
            port=conf['port'],
            database=conf['database'],
            user=conf['user'],
            password=conf['password']
        )
        return self.conn

    def execute_sql(self, sql):
        # 创建游标
        self.cs = self.create_conn().cursor()
        # 通过游标执行sql
        self.cs.execute(sql)
        value = self.cs.fetchone()
        self.close_resource()
        return value

    def close_resource(self):
        self.cs.close()
        self.conn.close()


if __name__ == '__main__':
    db = DataBaseUtil()
    re = db.execute_sql("SELECT CAST(original_price AS SIGNED) FROM sxo_cart WHERE id=97;")
    print(re)
    print(type(re))
    a = re[0]
    print(a)
