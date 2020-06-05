# -*- coding: utf-8 -*-
import time

import demjson
import scrapy

from ..items import XqproItem


class ProSpider(scrapy.Spider):
    name = 'pro'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']


    def start_requests(self):
        for pn in range(1,8):
            url='https://xueqiu.com/snowman/service/cubes/rank?tid=PAMID&period=DAY&page={pn}'.format(
                pn=pn
            )
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)


    def parse(self, response):
        res=demjson.decode(txt=response.text,encoding='utf-8')
        for i in res.get('result_data').get('list')[:]:
            for pn in range(1,6):
                detail_url='https://xueqiu.com/service/tc/snowx/PAMID/cubes/rebalancing/history?cube_symbol={symbol}&count=20&page={pn}'.format(
                symbol=i.get('symbol')
                ,pn=pn
            )
                yield scrapy.Request(url=detail_url,callback=self.final,meta={'data':i},dont_filter=True)

            # pass
        #
        # pass
    def final(self,response):
        res=demjson.decode(txt=response.text,encoding='utf-8')
        main=response.meta['data']
        item=XqproItem()
        for i in res.get('list')[:]:
            i=i.get('rebalancing_histories')[0]
            item['updated_at']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i.get('updated_at').__str__()[:10])))
            item['stock_name']=i.get('stock_name')
            # main.get('rate')
            item['gain_in_holding']=i.get('target_weight')-i.get('prev_weight_adjusted')
            item['stock_code']=i.get('stock_symbol')
            item['portfolio_user']=main
            yield item



            # pass

    # pass