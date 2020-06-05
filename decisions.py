# -*- coding: utf-8 -*-
# @Time    : 2019/12/10 11:49
# @Author  : Handsomejerry
# @Site    : 
# @File    : decisions.py
# @Software: PyCharm

import redis
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler

con = redis.Redis(host='localhost', port=6379,encoding='utf-8',db=1)

class calc_realtime(object):
    def __init__(self):
        self.li=[self.get_values(con.hgetall(i.decode('utf-8')),i.decode('utf-8')) for i in con.keys()]

    def get_values(self,pai_trade_dict,name):
        li=[float(i.decode('utf-8')) for i in pai_trade_dict.values()]
        if np.round(li[-1],4)>np.round(np.mean(li[:-1]),4):
            return name+':'+'差距变大'
        elif np.round(li[-1],4)<np.round(np.mean(li[:-1]),4):
            return name+':'+'差距变小'

    def get_res(self):
        a=0
        for i in self.li:
            if i:
                a+=1
                print(i,a)
def run():
    obs=calc_realtime()
    obs.get_res()

if __name__ == '__main__':
    # sched1=BlockingScheduler()
    # sched1.add_job(run,'interval',seconds=5)
    # sched1.start()
    run()
