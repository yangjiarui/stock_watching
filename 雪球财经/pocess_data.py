﻿# -*- encoding: utf-8 -*-
"""
@File    : pocess_data.py
@Time    : 2020/4/3 18:40
@Author  : handsomejerry
@Email   : 834235185@qq.com
@Software: PyCharm
"""
import pymongo
import pandas as pd
import numpy as np
db=pymongo.MongoClient('localhost',27017)['雪球财经']
cur=db['0512'].find({})
counts={}
def sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s
for j in cur[:]:
  #
  #
  # counts[j.get("stock_name")]={}
  if (j.get('updated_at')>='2020-05-10 00:00:00') and (j.get('updated_at')<='2020-05-13 00:00:00')  :
    try:
        # counts[j.get("stock_name")]['appeal_count']+=1
        diff=sigmoid(j.get('gain_in_holding')*j.get('portfolio_user').get('rate'))
        counts[j.get("stock_name")]['cumdiff']+=(diff-0.5)
        if counts[j.get("stock_name")]['cumdiff']:
            counts[j.get("stock_name")]['buy_count']+=1
        # else:
        #     counts[j.get("stock_name")]['appeal_count']+=(-1)
        counts[j.get("stock_name")]['appeal_total']+=1
    except:
        counts[j.get("stock_name")]={}
        diff=sigmoid(j.get('gain_in_holding')*j.get('portfolio_user').get('rate'))
        counts[j.get("stock_name")]['cumdiff']=diff-0.5
        counts[j.get("stock_name")]['stock_code']=j.get('stock_code')
        # if counts[j.get("stock_name")]['cumdiff']:
        counts[j.get("stock_name")]['buy_count']=0
        # else:
        #     counts[j.get("stock_name")]['buy_count']=
        counts[j.get("stock_name")]['appeal_total']=1


# print('排名头部股票基金持仓股票分布情况')
# print(counts)
q=pd.DataFrame(counts).T
q['buy']=(q['buy_count']/q['appeal_total'])*100
q['buy']=q['buy'].apply(lambda x:round(x,2).__str__()+'%')
q=q.sort_values(by=['cumdiff','buy'],ascending=False,axis=0)
print(q)