import base64
import requests

img_ = '../temp/_test.jpg'

with open(img_, 'rb') as img:
    # 使用base64进行编码
    b64encode = base64.b64encode(img.read())
    s = b64encode.decode()
    # print(s)

res = requests.request(method='post', url='http://127.0.0.1:80/web/verify', data=s)
print(res.text)

