# -*- coding: utf-8 -*-            
# Author:liu_ge
# @FileName: find_pic.py
# @Time : 2022/12/16 19:34
import base64
import cv2
import requests

from utils.logger_utils import print_info_log


def FindPic(target='../temp/bg.jpg', template='../temp/bl.jpg'):
    target_rgb = cv2.imread(target)  # 先把背景图片转成rgb
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)  # 做灰度处理
    template_rgb = cv2.imread(template, 0)  # 再把缺口文件转成rgb
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)  # 匹配缺口位置
    value = cv2.minMaxLoc(res)  # 返回匹配的x坐标
    print(value)
    # template_image = cv2.imread("../temp/bg.jpg")
    # print("shape =", template_image.shape)

    return value[2][0]


def get_x(ele_bl, ele_bg):
    base64_bl = ele_bl.get_attribute('src')[22:]  # 将元素图片转码至base64
    base64_bg = ele_bg.get_attribute('src')[22:]  # 将元素图片转码至base64
    f = open("D:\\Python_project\\ui_1129\\temp\\bg.jpg", mode='wb')  # 将base64转成本地图片
    f.write(base64.b64decode(base64_bg))
    f.close()
    f = open("D:\\Python_project\\ui_1129\\temp\\bl.jpg", mode='wb')  # 将base64转成本地图片
    f.write(base64.b64decode(base64_bl))
    f.close()

    x = FindPic("D:\\Python_project\\ui_1129\\temp\\bg.jpg", "D:\\Python_project\\ui_1129\\temp\\bl.jpg")
    new_x = int(x * (280 / 360)*1.25)
    return new_x


def verify_str():
    img_ = './temp/_test.png'

    with open(img_, 'rb') as img:
        # 使用base64进行编码
        print_info_log('正在对验证码图片进行base64编码')
        b64encode = base64.b64encode(img.read())
        print_info_log('正在对验证码图片进行base64解码')
        s = b64encode.decode()
        # print(s)
    print_info_log('正在向验证码解码平台发送post请求')
    res = requests.request(method='post', url='http://127.0.0.1:80/web/verify', data=s)
    print_info_log(f'解码到的字串为:{res.text}')
    return res.text



if __name__ == '__main__':
    FindPic('../temp/bg.jpg', '../temp/bl.jpg')
