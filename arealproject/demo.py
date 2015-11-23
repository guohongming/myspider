# coding:utf-8

import json
import csv
from abc import abstractmethod, ABCMeta
from bs4 import BeautifulSoup
from spider import HttpClient


class Parser(object):

    _client = HttpClient()

    def get_page_charset(self,page):

        if not page:
            return self.default_charset

        bs = BeautifulSoup(page)
        # print (page)
        meta_content = bs.find("meta", {"content": True})

        if not meta_content:
            return self.default_charset

        meta_content_value = meta_content.get("content")
        meta_content_value_list = meta_content_value.split(";")

        if len(meta_content_value_list) < 2:
            return self.default_charset

        page_charset = meta_content_value_list[1].split("=")[1].strip()

        return page_charset

    def post(self, url, params, headers=None):

        html = None

        try:
            html = self._client.post(url, params, headers)

        except Exception as e :
            print(e)
            if not (e.code == self._not_found_err):
                raise

        finally:
            return html

    def write_data(self, data,name):

        file_name = name+'.csv'
        with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(data)


class Demo(Parser):

    def __init__(self):
        self.default_charset = "utf-8"
        self.host = 'http://www.jsgsj.gov.cn:58888/ecipplatform/nbServlet.json?nbEnter=true'
        self.main_url = 'http://www.jsgsj.gov.cn:58888/province/NoticeServlet.json?QueryExceptionDirectory=true'
        
    def parse(self, j, name1):
        count = 0
        i = j
        params = {
                  'showRecordLine': 1,
                  'pageNo': i,
                  'pageSize': 10
                  }
        content = self.post(self.main_url, params).decode('UTF-8')
        # print(content)
        dict1 = dict(json.loads(content))
        item1s = dict1.get('items')
        # print(item1s)
        #print(items)
        for item in item1s:

            main_id = None
            c_name = item.get('C1')
            c_id = item.get('C2')
            c_data = item.get('C3')


            params = {
                  'REG_NO':c_id,
                  'showRecordLine':"0",
                  'specificQuery':"gs_pb",
                  'propertiesName':"query_report_list",
                  # 'tmp': "Sun+Nov+22+2015+00:46:56+GMT+0800"
                  }

            content = self.post(self.host, params).decode('UTF-8')
            # print(content)
            content = '{"items":'+content+'}'
            dict1 = dict(json.loads(content))
            items = dict1.get('items')
            if items != []:
                for item in items:

                    num = item.get('ID')
                    main_id = num
                    break
                params = {
                    'MAIN_ID':main_id,
                    'OPERATE_TYPE':"1",
                    'TYPE':"NZGS",
                    'showRecordLine':"1",
                    'specificQuery':"gs_pb",
                    'propertiesName':"query_stockInfo",
                    'ID':main_id,
                    'ADMIT_MAIN':"08",
                    'pageNo':"1",
                    'pageSize':"5"
                }
                content = self.post(self.host, params).decode('UTF-8')
                # print(content)
                dic21 = dict(json.loads(content))
                item2s = dic21.get('items')
                for ite in item2s:
                    data1 = []
                    data = []
                    cont = ite.get('D1')
                    content_bs = BeautifulSoup(cont)
                    its = content_bs.find_all('td')
                    for it in its:
                        data.append(it.string)

                    # print(data)
                    data1.extend((c_name,c_id,c_data))
                    data1.extend(data)
                    # print(data1)
                    self.write_data(data1,name1)
            else:
                data1 = []
                data1.extend((c_name,c_id,c_data))
                # print(data1)
                self.write_data(data1,name1)

        #print(count)

if __name__ == '__main__':
    de = Demo()
    de.parse(1,'baogao')