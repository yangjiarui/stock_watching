# -*- encoding: utf-8 -*-
"""
@File    : 对比excel.py
@Time    : 2020/3/26 15:35
@Author  : handsomejerry
@Email   : 834235185@qq.com
@Software: PyCharm
"""

import pandas as pd
pre=pd.read_csv(open('各基金持仓分析(0322_2).csv'))
now=pd.read_csv(open('各基金持仓分析(0328_1).csv'))


diff={}
for i in range(now.shape[0]):
    c=now.iloc[i,:]
    # diff[c[1]]=_
    try:
        diff[c[1]]['stock_code']=c[4]
    except:
        diff[c[1]]={}
    _=pre[pre['stock_code']==c[4]]
    try:
        diff[c[1]]['同比机构投资增加个数']=c[2]-_['appeal_count'].values[0]
        diff[c[1]]['同比机构投资增加额']=c[3]-_['money_invested'].values[0]
        diff[c[1]]['同比机构投资弹性']= round(((c[-2]-_['stock_mv'].values[0])/(c[3]-_['money_invested'].values[0])),4)
        diff[c[1]]['同比机构追加投资比例']= round(((c[3]-_['money_invested'].values[0])/(c[-2])),4)
    except:
        continue
    # f=f.append(pd.Series(diff),ignore_index=True)
ff=pd.DataFrame(diff).T
ff=ff.sort_values(by=['同比机构追加投资比例','同比机构投资弹性','同比机构投资增加个数','同比机构投资增加额'],ascending=False)

ff['同比机构投资弹性']=ff['同比机构投资弹性'].apply(lambda x:round(x*100,3).__str__()+'%')
ff['同比机构追加投资比例']=ff['同比机构追加投资比例'].apply(lambda x:round(x*100,3).__str__()+'%')


ff.to_csv('diff.csv')