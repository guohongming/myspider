__author__ = 'Guo'
# coding:utf-8
import requests
from bs4 import  BeautifulSoup

def write_in_text(data):
    with open('ip.txt','a',newline='') as f:
        f.write(data)
        f.write('\r\n')

def get_html():
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
    }

    res = requests.get('http://www.xicidaili.com/', headers = header)

    # print(res.text)

    bs = BeautifulSoup(res.text)
    links = bs.find_all('tr',{'class':'odd'})
    for link in links:
        tds = link.find_all('td')
        td1 = tds[1]
        td2 = tds[2]
        ip = td1.string+':'+td2.string
        # print(ip)
        write_in_text(ip)

def read_txt():
    ips = []
    with open('ip.txt') as f:
        lines = f.readlines()
        for line in lines:
            ip = line.replace('\n','')
            ips.append(ip)
    return ips



if  __name__ == '__main__':
    get_html()
    ips = read_txt()
    i = 0
    while i <len(ips):
        print(ips[i])
        i += 1

