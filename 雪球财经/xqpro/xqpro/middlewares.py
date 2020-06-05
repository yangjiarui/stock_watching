# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from fake_useragent import UserAgent
from scrapy import signals




class RandomProxy(object):
    def __init__(self):
        self.ua=UserAgent()

    def to_cookie(self,q):
        q = q.split('; ')
        full = {}
        for i in q:
            if '=' in i:
                try:
                    full[i.split('=', 1)[0].strip()] = i.split('=', 1)[1].strip()
                except:
                    pass
        return full



    def process_request(self, request, spider):
        if 'service' in request.url:
            # request.headers['Cookie'] = cookie
            request.cookies = self.to_cookie('''
device_id=24700f9f1986800ab4fcc880530dd0ed; s=do1clcl6cp; bid=c6810e4da3f1b190f21481eef866d2e5_ka3pcfyd; __utmz=1.1589275078.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); xq_a_token=5bd24293ab375322c6054c7a9f914ed98f1a9caa; xqat=5bd24293ab375322c6054c7a9f914ed98f1a9caa; xq_r_token=4bd27f43eb12a9169019095cf9ff7e0a10999495; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjI5NDU1MzMzODAsImlzcyI6InVjIiwiZXhwIjoxNTkxODY2ODk0LCJjdG0iOjE1ODk3OTE3NDU1NTUsImNpZCI6ImQ5ZDBuNEFadXAifQ.TcoM-dHWXFg-XpO1TkFUZxct17WWjNyZ3xoKEDG9pxCSjUzuUuA5po5BrqWI-Zo-ePn2F0LGoXFQ5H1e6Fb29c8YZUBblG6ssyPQFqv-ph1htStn-vLNg9_kGYKCMqrRybY9U6cUnf6QXUg3aHH7yXmlmionYPOD930wsjGiKvlrgXxliTJCbqorfHVlil9R_B8ELq5WiszTD9SxaS_tTSK_uldwdSQWtWzuxW1qaAytY3Zl48OPJWCleLT1nm6GhTNLaSvtNToO3aVQDvxTcGS1kuZEgvGft-fEw8YEGku4NpAI_m8gsjMlF8HVC5xSHgbbYTch_9tpw1OhlADH_A; xq_is_login=1; u=2945533380; aliyungf_tc=AQAAACYIUD3s9gYAE0zkZVOMEtE1uk+c; acw_tc=2760820a15899516214701774e545ae34be05c8e541a70ea2a008c2af3f4bd; is_overseas=0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1589791923,1589796326,1589878743,1589951623; snbim_minify=true; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1589951635; __utma=1.517561539.1589275078.1589878743.1589951635.6; __utmc=1; __utmt=1; __utmb=1.1.10.1589951635
''')   #key:value对
        request.headers["User-Agent"] = self.ua.random
        request.meta["proxy"] = 'http://http-dyn.abuyun.com:9020'
        request.headers["Proxy-Authorization"] = 'Basic ' + 'SE00MDI4SDcyNjYwMTU4RDpFRTk1MEI3NjkyNjE0Mjc1'
            # if 'xiaohongshu' in request.url:
                #     request.headers["cookie"]='timestamp1=; hasaki=; timestamp2=; '

    # def randomproxy(self,request,spider):
    #
    #
    #     proxy_s =
    #     # 对应到代理服务器的信令格式里
    #     request.headers['Proxy-Authorization'] = 'Basic ' + 'SE00MDI4SDcyNjYwMTU4RDpFRTk1MEI3NjkyNjE0Mjc1'
    #     request.meta['proxy'] = 'http://' + proxy_s
    #



class XqproSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class XqproDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
