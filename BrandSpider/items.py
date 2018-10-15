# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# Item 是保存爬取到的数据的容器；其使用方法和python字典类似， 并且提供了额外保护机制来避免拼写错误导致的未定义字段错误。
class BrandSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()

class DailyTurnoverItem(scrapy.Item):
    # define the fields for your item here like:
    site = scrapy.Field()
    date = scrapy.Field()
    turnover = scrapy.Field()
    url = scrapy.Field()
