# -*- encoding: utf-8 -*-
"""
@File    : pocess_datas.py
@Time    : 2020/2/27 17:52
@Author  : handsomejerry
@Email   : 834235185@qq.com
@Software: PyCharm
"""
from pprint import pprint
import pandas as pd
import pymongo
from WindPy import *
import datetime as ttt
db=pymongo.MongoClient('localhost',27017)['eastmoney']
cur=db['0328_1'].find({},{'con':1})


def app(x):
    if 'sh' in x:
        return x.split('sh')[-1]+'.SH'
    elif 'sz' in x:
        return x.split('sz')[-1]+'.SZ'
    else:
        pass


def pocess_stock(wind_data):
    # return pd.DataFrame(dict(zip(wind_data.Codes,wind_data.Data[0])))
    return pd.DataFrame(dict(zip(wind_data.Codes,wind_data.Data[0])),index=[0]).T

w.start()
index_date=(ttt.datetime.now()-ttt.timedelta(days=1)).strftime('%Y%m%d')




if __name__ == '__main__':
    counts={}
    for i in cur:
        c=i.get('con')
        for j in c.get('stocks')[:]:
            # counts[j.get("stock_name")]={}
            try:
                counts[j.get("stock_name")]['appeal_count']+=1
                counts[j.get("stock_name")]['money_invested']+=(j.get('money_in_stock'))
            except:
                counts[j.get("stock_name")]={}
                counts[j.get("stock_name")]['appeal_count']=1
                counts[j.get("stock_name")]['money_invested']=j.get('money_in_stock')
                counts[j.get("stock_name")]['stock_code']=j.get('stock_code')
    print('排名头部股票基金持仓股票分布情况')
    q=pd.DataFrame(counts).T
    q=q.sort_values(by=['money_invested','appeal_count'],ascending=False,axis=0)
    CODES=','.join(filter(lambda x:x!=None,(app(i) for i in q.iloc[:,2])))
    mv=w.wss("{codes}".format(codes=CODES), "mkt_cap_ard","unit=1;tradeDate={date}".format(date=index_date))
    mv=pocess_stock(mv)
    mv=mv.reset_index()
    mv.columns=['stock_code','stock_mv']
    q['stock_code']=q['stock_code'].apply(app)
    q=q.reset_index()
    all=pd.merge(q,mv,how='left',on='stock_code')
    all['left_to_invest']=1-all['money_invested']/all['stock_mv']
    all['left_to_invest']=all['left_to_invest'].apply(lambda x:round(x*100,3).__str__()+'%')
    pprint(all)
    all=all.sort_values(by=['money_invested','appeal_count'],ascending=False,axis=0)
    all.to_csv('各基金持仓分析(0328_1).csv')
    # qq=pd.read_csv('各基金持仓分析(新).csv')
    # qq.to_excel('各基金持仓分析(新).xlsx')
        # pass