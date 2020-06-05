# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XqproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    gain_in_holding= scrapy.Field()
    updated_at= scrapy.Field()
    stock_name= scrapy.Field()
    stock_code= scrapy.Field()
    portfolio_user= scrapy.Field()