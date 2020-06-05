# -*- coding: utf-8 -*-
import copy

import scrapy,json,demjson
import io,sys,re,datetime

from kafka import KafkaProducer
from scrapy_splash import SplashRequest

from ..items import XhsPcItem

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
import redis
from urllib.parse import unquote
# r = redis.Redis(host='123.56.196.177',port=6379,db=12)
from scrapy_redis.spiders import RedisSpider


class XhsPcSpider(RedisSpider):
# class XhsPcSpider(scrapy.Spider):
    name = 'final'
    allowed_domains = ['xiaohongshu.com','360.com','eastmoney.com']
    # a = r.lpop('小红书_测试:start_urls')
    # dbpush =redis.StrictRedis('localhost',6379,db=1)
# r_name = '小红书_测试:start_urls'
    redis_key = 'eastmoney:start_urls'
    # start_urls = ['http://fund.eastmoney.com/006265.html']
    # list_count = r.llen(r_name)
    script = """
                    function main(splash, args)
                        splash:go(args.url)
                        splash:wait(3.3)
                        splash:runjs("ffe=()=>{document.querySelector('#quotationItem_DataTable > div.item_title.hd > div:nth-child(1)').click()}")
                	     splash:evaljs("ffe()")
                        splash:wait(2.3)
                  return {
                    html = splash:html(),
                  }
                    end
                    """

    def make_request_from_data(self, data):
        res=json.loads(data)

        headers=self.to_head("""
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: EMFUND1=null; EMFUND2=null; HAList=a-sz-002594-%u6BD4%u4E9A%u8FEA; em_hq_fls=js; _adsame_fullscreen_12706=1; ASP.NET_SessionId=ivpv5m11v4ombrfarb2lykrv; st_si=30947743766998; st_asi=delete; EMFUND0=null; EMFUND3=02-27%2013%3A59%3A47@%23%24%u56FD%u6CF0%u4E2D%u8BC1%u5168%u6307%u901A%u4FE1%u8BBE%u5907ETF%u8054%u63A5A@%23%24007817; EMFUND4=02-27%2013%3A59%3A11@%23%24%u5BCC%u56FD%u4E2D%u8BC1%u667A%u80FD%u6C7D%u8F66%28LOF%29@%23%24161033; EMFUND5=02-27%2014%3A03%3A48@%23%24%u4E1C%u8D22%u4E2D%u8BC1%u901A%u4FE1C@%23%24008327; EMFUND6=02-27%2015%3A07%3A06@%23%24%u5E7F%u53D1%u4E2D%u8BC1%u5168%u6307%u6C7D%u8F66%u6307%u6570C@%23%24004855; EMFUND7=02-27%2014%3A15%3A32@%23%24%u521B%u91D1%u5408%u4FE1%u79D1%u6280%u6210%u957F%u80A1%u7968A@%23%24005495; EMFUND8=02-27%2016%3A17%3A57@%23%24%u666F%u987A%u4E2D%u8BC1TMT150ETF%u8054%u63A5@%23%24001361; EMFUND9=02-27 16:18:17@#$%u9E4F%u534E%u5730%u4EA7%u5206%u7EA7@%23%24160628; st_pvi=99658311359710; st_sp=2020-02-27%2013%3A34%3A29; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2Fdata%2Ffundranking.html; st_sn=5; st_psi=20200227161817357-0-7803399985
Host: fund.eastmoney.com
Pragma: no-cache
Referer: http://fund.eastmoney.com/data/
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
                """)
        splah_args = {
            # 'wait': 3,
            "http_method":"GET",
            "images":0,
            # "timeout":1800,
            "render_all":1,
            # "headers":headers,
            'lua_source': self.script,
            # "cookies":cookies,
            # "proxy":"http://101.200.153.236:8123",
        }

        return SplashRequest(url=res.get('fund_detail_url'), callback=self.parse, endpoint='execute',args=splah_args,
                            headers=headers,meta={'main':copy.deepcopy(res)} ,dont_filter=True)

    # for index in range(list_count):
    #     # str(r.lindex(r_name, index),encoding='utf-8')
    #     url = 'https://www.xiaohongshu.com/discovery/item/{}'.format(str(r.lindex(r_name, index),encoding='utf-8'))
    #     start_urls.append(url)

    def to_head(self,q):
        q = q.split('\n')
        full = {}
        for i in q:
            if ':' in i:
                full[i.split(':', 1)[0].strip()] = i.split(':', 1)[1].strip()
        return full

    def parse(self, response):
        item=XhsPcItem()
        tonow_ytm=response.xpath('//dl[@class="dataItem03"]/dd[last()]/span[last()]/text()').extract_first()
        stocks=response.xpath('//*[@id="position_shares"]/div[1]/table/tbody/tr')
        res=response.meta.get('main')
        res['tonow_ytm'],res['stocks']=tonow_ytm,[]
        res['time_record']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fund_money=float(res.get('fund_money'))
        for i in stocks[1:]:
            stock_name=i.xpath('td/a/@title').extract_first()
            stock_current_ytd=i.xpath('td[2]/text()').extract_first()
            stock_code=i.xpath('td/a/@href').extract_first().split('/')[-1].split('.')[0]
            res['stocks'].append({'stock_name':stock_name,
                                  'stock_current_position':stock_current_ytd,
                                  'money_in_stock':(float(stock_current_ytd.split('%')[0])*fund_money)/100,
                                  'stock_code':stock_code})
        item['con']=res
        yield item

        # urlholdsmoney_url=response.url.replace('http://fund.eastmoney.com/','http://fundf10.eastmoney.com/jbgk_')
        # yield scrapy.Request(url=urlholdsmoney_url,callback=self.parse_final,meta={})




