__author__ = 'Guo'
# coding:utf-8

import requests
from bs4 import BeautifulSoup

# 解决编码问题
try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from io import StringIO


def login():
    header = {
        'Host':"www.zhihu.com",
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        'Accept':"*/*",
        'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding':"gzip, deflate",
        'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8"
    }

    session = requests.session() #　处理ｃｏｏｋｉｅ

    res = session.get('http://www.zhihu.com/captcha.gif',headers = header)  # seesionh会记下访问验证码的cookie
    with open('captcha.jpg', 'wb') as fp:
        fp.write(res.content)     #　讲验证码图片保存在本地。
    # print(res.content)
    #print(res.cookies)
    # cook = res.cookies
    capt = input('input captcha')  # 手动读取
    xsrf = BeautifulSoup(session.get('http://www.zhihu.com/#signin').content).find('input', attrs={'name': '_xsrf'})['value'] # 从源码中获取的表单中的一个字段
    print(xsrf)
    data = {
        '_xsrf': xsrf,
        'email': 'guohongming03@gmail.com',
        'password': 'guo1006575211',
        'remember_me': 'true',
        'captcha': capt
    }

    response = session.post('http://www.zhihu.com/login/email',data = data,headers = header ) # post 登录时提交的表单，此时session中是保存了此时的cookie 的

    print(response.status_code)
    print(response.content.decode('utf-8'))
    html = session.get('http://www.zhihu.com/#signi') # 再次访问，由于cookie 的存在，记下了登录的状态，所以此时就可以获取我们登录之后的类容了啦。

    print(html.content.decode('utf-8'))


if __name__ == '__main__':
    login()