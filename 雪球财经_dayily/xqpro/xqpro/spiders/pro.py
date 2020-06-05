# -*- coding: utf-8 -*-
import json
import re
import time

import demjson
import scrapy

from ..items import XqproItem


class ProSpider(scrapy.Spider):
    name = 'pro'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']


    def start_requests(self):
        for pn in range(1,15):
            url='https://xueqiu.com/snowman/service/cubes/rank?tid=PAMID&period=DAY&page={pn}'.format(
                pn=pn
            )
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)


    def parse(self, response):
        res=demjson.decode(txt=response.text,encoding='utf-8')
        for i in res.get('result_data').get('list')[:]:
            # for pn in range(1,6):
            detail_url='https://xueqiu.com/P/{syn}'.format(
                syn=i.get('symbol')
            )
            yield scrapy.Request(url=detail_url,callback=self.final,meta={'data':i},dont_filter=True)

    def final(self,response):
        res=re.findall('SNB.cubeInfo =(.*?)seajs.use',response.text,re.S|re.M)
        q1,q2,q3,__,ww=res[0].split(';')
        main=response.meta['data']
        q1,q2,q3=json.loads(q1),json.loads(q2.replace('\nSNB.cubePieData = ','')),json.loads(q3.replace('\nSNB.cubeTreeData = ',''))
        item=XqproItem()
        item['hodings']=q3
        for i in q1.get('sell_rebalancing').get('rebalancing_histories'):
            item['updated_at']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i.get('updated_at').__str__()[:10])))
            item['stock_name']=i.get('stock_name')
            item['gain_in_holding']=i.get('target_weight')-i.get('prev_weight_adjusted')
            item['stock_code']=i.get('stock_symbol')
            item['portfolio_user']=main
            yield item
