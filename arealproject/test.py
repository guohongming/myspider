# coding = 'UTF-8'

import threading
import random
import time
from  demo import Demo
from demo import Parser


class MyThread(threading.Thread):

    def __init__(self, start, output_name):
        """ Initialize elementary parameter """

        threading.Thread.__init__(self)
        self.begin = start
        self.file_name = output_name
        self.name = threading.current_thread().name

    def run(self):
        name = self.name
        i = self.begin
        end = i + 100
        while i < end:
            de = Demo()
            de.parse(i,name)
            print('第',i,'页已经写入文件')
            i += 1

def test(start):
    count = 0
    thread = []
    while count < 100:
        t = MyThread(start+count*100, str(count+1) + '.csv')
        if count+1 < 10:
            t.name = '00' + str(count+1) + '号线程'
        elif count+1 < 100:
            t.name = '0' + str(count+1) + '号线程'
        else:
            t.name = str(count+1) + '号线程'
        thread.append(t)
        count += 1

    print('主线程开始')

    count = 0
    while count < 100:
        thread[count].start()
        count += 1

    count = 0
    while count < 100:
        thread[count].join()
        time.sleep(random.choice(range(0, 20)))
        count += 1

    print('主线程结束')

if __name__ == '__main__':
    test(1)