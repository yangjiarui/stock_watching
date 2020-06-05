import copy
import json
import time
# from pprint import pprint
import pandas as pd
import redis
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
# from sklearn.metrics.pairwise import cosine_similarity

con = redis.Redis(host='localhost', port=6379,encoding='utf-8')
calcon = redis.Redis(host='localhost', port=6379,encoding='utf-8',db=1)

def next1():
    i = -1
    while 1:
        i += 1
        yield i
z=next1()
class dataclass(object):
    def __init__(self):
        self.n=z.__next__()
    def warpper(self,code,i):
        _=con.hget(code,i)
        try:
            return json.loads(_).get('price')
        except:
            pass

    def get_values(self):
        self.get_codes()
        dicts={}
        [dicts.update({co:[self.warpper(code=co, i=i) for i in range(6)]}) for co in self.codes]
        return pd.DataFrame(dicts)

    def get_codes(self):
        a = con.hgetall('stock_names')
        if a:
            self.codes=[i.decode('utf-8') for i in a.values()]
        else:
            pass

    def calcu_mid(self,haves):
        while 1:
            try:
                current = haves.pop()
            except:
                # print('完成此批次!!')
                break
            [calcon.hset(current + '_2_' + pair,self.n.__str__(), self.make_cosin(self.dff[current], self.dff[pair])) for pair in
             haves]
        print('余弦相似度2redis')

    def calcu(self):
        df=self.get_values()
        self.dff = df.dropna()
        self.haves=self.dff.columns.to_list()
        # while 1:
        self.calcu_mid(haves=copy.deepcopy(self.haves))
            # print('余弦相似度2redis!!')

    def make_cosin(self,a,b):
        a,b=np.array(a,dtype='float64'),np.array(b,dtype='float64')
        return np.arccos(np.dot(a,b)/( np.linalg.norm(a) * np.linalg.norm(b)))*(180/np.pi)

        # return cosine_similarity([a,b])
def next2():
    i = -1
    while 1:
        i += 1
        yield i
z2=next2()
class pop(object):
    def __init__(self):
        self.n = z2.__next__()
        self.keys=calcon.keys()
    def deletredis(self):
        [con.hdel(i.decode('utf-8'), self.n.__str__()) for i in self.keys]
        # [obs.get_bars2redis(code=i) for i in codes]
        print('delet2redis')


def run():
    obj = dataclass()
    obj.calcu()
def delet():
    obj=pop()
    obj.deletredis()



if __name__ == '__main__':
    sched1 = BlockingScheduler()
    sched1.add_job(run, 'interval', seconds=10)

    sched1.add_job(delet, 'interval', seconds=30)
    sched1.start()

















