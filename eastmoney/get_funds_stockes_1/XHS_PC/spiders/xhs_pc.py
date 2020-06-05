# -*- coding: utf-8 -*-
import copy

import scrapy,json,demjson
import io,sys,re,datetime

from kafka import KafkaProducer
from scrapy_splash import SplashRequest

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
import redis
from urllib.parse import unquote
# r = redis.Redis(host='123.56.196.177',port=6379,db=12)
from scrapy_redis.spiders import RedisSpider


# class XhsPcSpider(RedisSpider):
class XhsPcSpider(scrapy.Spider):
    name = 'pro'
    allowed_domains = ['xiaohongshu.com','360.com','eastmoney.com']
    # a = r.lpop('小红书_测试:start_urls')
    # r_name = '小红书_测试:start_urls'
    # redis_key = '小红书_C101304:start_urls'
    # dbpush = redis.Redis(host='139.198.0.141', port=6381,db=1)
    dbpush =redis.StrictRedis('localhost',6379,db=1)
    start_urls = ['http://fund.eastmoney.com/data/fundranking.html#tgp;c0;r;szzf;pn50;ddesc;qsd20190227;qed20200227;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb']
    # start_urls = ['https://hao.360.com/?safe']
    # list_count = r.llen(r_name)
    script = """
                    function main(splash, args)
                        splash:go(args.url)
                        splash:wait(3.8)
                        splash:runjs("ffe=()=>{document.getElementById('pnum').value='%s';document.querySelector('#pagebar > input.pgo').click()}")
                	     splash:evaljs("ffe()")
                        splash:wait(3.3)
                  return {
                    html = splash:html(),
                  }
                    end
                    """


    def start_requests(self):
        headers = self.to_head('''
                Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
                Accept-Encoding: utf8
                Accept-Language: zh-CN,zh;q=0.9
                Cache-Control: max-age=0
                Connection: keep-alive
                Cookie: st_si=75488570979445; st_sn=1; st_psi=20200205194001392-0-9489432292; st_asi=delete; st_pvi=40417307822800; st_sp=2020-02-05%2019%3A40%3A01; st_inirUrl=; ASP.NET_SessionId=imbotrddja1sr10nzbjs0hpc
                Host: fund.eastmoney.com
                If-Modified-Since: Wed, 05 Feb 2020 11:22:31 GMT
                Referer: http://fund.eastmoney.com/data/fundranking.html
                Upgrade-Insecure-Requests: 1
                User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36
        ''')
        for i in range(1,40):
            splah_args = {
            # 'wait': 3,
                    "http_method":"GET",
                    "images":0,
                    # "timeout":1800,
                    "render_all":1,
                    # "headers":headers,
                    'lua_source': self.script%i,
                    # "cookies":cookies,
                    # "proxy":"http://101.200.153.236:8123",
        }

            yield SplashRequest(url=self.start_urls[0], callback=self.parse, endpoint='execute',args=splah_args,
                            headers=headers,dont_filter=True)

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
        funds=response.xpath('//*[@id="dbtable"]/tbody/tr')
        for i in funds[:]:
            rankth=i.xpath('td[2]/text()').extract_first()
            fund_name=i.xpath('td[4]/a/@title').extract_first()
            fund_code=i.xpath('td[3]/a/text()').extract_first()
            fund_time=i.xpath('td[5]/text()').extract_first()
            fund_pre=i.xpath('td[7]/text()').extract_first()
            daily_ytm=i.xpath('td[8]/text()').extract_first()
            weekly_ytm=i.xpath('td[9]/text()').extract_first()
            monthly_ytm=i.xpath('td[10]/text()').extract_first()
            threemounth_ytm=i.xpath('td[11]/text()').extract_first()
            fund_detail_url=i.xpath('td[4]/a/@href').extract_first()
            fund_position_url=fund_detail_url.replace('fund.eastmoney.com/','fundf10.eastmoney.com/jbgk_')


            yield scrapy.Request(url=fund_position_url,callback=self.parse_final,meta={'to_redis':copy.deepcopy({'rankth':rankth,'fund_name':fund_name,
                                                                 'fund_code':fund_code,'fund_time':fund_time,
                                                                 'fund_pre':fund_pre,'daily_ytm':daily_ytm,
                                                                 'weekly_ytm':weekly_ytm,'monthly_ytm':monthly_ytm,
                                                             'threemounth_ytm':threemounth_ytm,
                                                             'fund_detail_url':fund_detail_url})},dont_filter=True)
    def pocess_unit(self,res):
        if '亿' in res:
            a=res.split('亿')[0]
            return (float(a)*10000000).__str__()
        else:
            return None


    def parse_final(self,response):
        all=response.meta['to_redis']
        fund_money=response.xpath('//table[contains(@class,"info")]/tr[4]/td/text()').extract_first().split('元')[0]
        all.update({'fund_money':self.pocess_unit(fund_money)})




        self.dbpush.lpush('eastmoney:start_urls',json.dumps(all))
        print('push_to_redis')

        # pass

            # self.dbpush.lpush('eastmoney:start_urls',json.dumps({'rankth':rankth,'fund_name':fund_name,
            #                                                      'fund_code':fund_code,'fund_time':fund_time,
            #                                                      'fund_pre':fund_pre,'daily_ytm':daily_ytm,
            #                                                      'weekly_ytm':weekly_ytm,'monthly_ytm':monthly_ytm,
            #                                                  'threemounth_ytm':threemounth_ytm,
            #                                                  'fund_detail_url':fund_detail_url}))
        # print('push2redis!!!')

