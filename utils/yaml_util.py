# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: yaml_util.py
# @Time : 2022/11/8 14:54
import os
import yaml


def get_object_path():
    return os.getcwd()


def read_yaml(yaml_path, key):
    with open(get_object_path() + "/" + yaml_path, mode="r", encoding="utf-8") as f:
        result = yaml.load(stream=f, Loader=yaml.FullLoader)
        return result[key]


def write_yaml(yaml_path, data):
    with open(get_object_path() + "/" + yaml_path, mode="a", encoding="utf-8") as f:
        result = yaml.dump(data, stream=f, allow_unicode=True)
        return result


def clear_yaml(yaml_path):
    with open(get_object_path() + "/" + yaml_path, mode="w", encoding="utf-8") as f:
        f.truncate()


