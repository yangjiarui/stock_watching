# -*- coding: utf-8 -*-
# @Time    : 2019/12/6 10:05
# @Author  : Handsomejerry
# @Site    : 
# @File    : 2redis.py
# @Software: PyCharm
import datetime
import json
import random
import time
import pandas as pd
import redis
import tushare as ts
from apscheduler.schedulers.blocking import BlockingScheduler

def next1():
    i = -1
    while 1:
        i += 1
        yield i
z=next1()
class toridis(object):
    def __init__(self):
        self.next=z.__next__()
    def get_bars2redis(self,code):
        cur=ts.get_realtime_quotes(code)
        it= {}
        for key,value in cur.to_dict().items():
            it[key]=value.get(0)
        con.hset(it.pop('code'),self.next.__str__(),json.dumps(it))



def next2():
    i = -1
    while 1:
        i += 1
        yield i
z2=next2()
class popredis(object):
    def __init__(self):
        self.next=z.__next__()
    def delet(self,code):
        [con.hdel(code,self.next.__str__()) for i in codes]
        # [obs.get_bars2redis(code=i) for i in codes]


def run():
    obs = toridis()
    [obs.get_bars2redis(code=i) for i in codes]
    print('to2redis')

def deletrun():
    obs2=popredis()
    [obs2.delet(code=i) for i in codes]
    print('delet2redis')

if __name__ == '__main__':
    con = redis.Redis(host='localhost', port=6379)
    codes=ts.get_hs300s()['code'].values[:2]
    [con.hset('stock_names',random.random().__str__()[2:-7],j) for j in codes]
    sched1=BlockingScheduler()
    sched1.add_job(run,'interval',seconds=10)
    time.sleep(10)
    sched1.add_job(deletrun,'interval',seconds=17)
    sched1.start()





    # a=obs.get_bar()
