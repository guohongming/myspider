__author__ = 'Guo'
# encoding = UTF-8

import re
import csv
import random
import time
import urllib.request
import socket
from bs4 import BeautifulSoup
import http.client

# 获取网页中的html代码
def get_content(url, data=None):
    """ Get html that url assigned """
    # header 是urllib.request.Request的一个参数，目的是模拟浏览器访问
    html = None
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
    timeout = random.choice(range(80, 180))
    # print(type(header))
    while True:
        try:
            req = urllib.request.Request(url, data, header)
            response = urllib.request.urlopen(req, timeout=timeout)
            html = response.read().decode('UTF-8', errors='ignore')
            response.close()
            break
        except urllib.request.HTTPError as e:
                print( '1:', e)
                time.sleep(random.choice(range(5, 10)))

        except urllib.request.URLError as e:
            print( '2:', e)
            time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))
        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return html

# 获取html中我们所需要的字段
def get_data(html):
    final = []
    bs = BeautifulSoup(html) # 创建BeautifulSoup对象
    body = bs.body  # 获取html中body部分
    # print(body.find_all('div'))

    data = body.find_all('div', {'id': '7d'})  # 获取我们所需要的div标签

    # print(data)
    li = []
    for i in data:
        li = i.find_all('li')  # 获取其中的li标签
        # print(li)
    for day in li:
        temp = []
        h1 = day.find('h1').string  # 获取星期几
        # print(type(h1))
        h2 = day.find('h2').string  # 获取日期
        p = day.find('p').string  # 获取天气
        ps = day.find_all('p')

        temp.extend((h1, h2, p))  # 放入一天的数据放入temp中
        final.append(temp)  # 将temp放入final中

    # print(final)
    return final  # 返回一周的数据

# 写入文件csv
def write_data(data, name):
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101190401.shtml'
    html = get_content(url)
    # print(type(html))
    # print(html)
    result = get_data(html)
    print(result)
    write_data(result, '本周天气.csv')
    # print(data1)






