__author__ = 'Guo'
# encoding = UTF-8

import csv


def read_file(name):
    with open(name, newline='' ) as f:
        f_csv = csv.reader(f)
        #print(type(f_csv))
        #for row in f_csv:
        #    print(row)
        write_file('基本信息表.csv',f_csv)


def write_file(name,data):
        file_name = name
        with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerows(data)

if __name__ == '__main__':
    i = 0
    while i< 100:
        if i+1 < 10:
            filename = '00' + str(i+1) + '号线程'+'.csv'
        elif i+1 < 100:
            filename = '0' + str(i+1) + '号线程'+'.csv'
        else:
            filename = str(i+1) + '号线程'+'.csv'
        i += 1
        read_file(filename)
        print(i,'写入')


