import re
import json
import scrapy
from collections import Iterable

from BrandSpider.items import BrandSpiderItem


class YidaiSpider(scrapy.Spider):
    name = "yidai"
    allowed_domains = ["yidai.com"]
    start_urls = ["https://www.yidai.com/invest/index.html?page=" + str(i) for i in range(1, 1613)] #1613

    def parse(self, response):
        items_xpath = "//div[contains(@class,'invest-table')]//div[contains(@class,'item')]"

        id_xpath = ".//a[@title]//@href"
        price_xpath = ".//li[contains(text(),'元')]//text()"
        date_xpath = ".//*[contains(text(),'发标日期')]//text()"

        for item in response.xpath(items_xpath):
            spider_items = BrandSpiderItem()
            spider_items['url'] = response.url
            spider_items['id'] = text(item.xpath(id_xpath).extract())
            spider_items['price'] = text(item.xpath(price_xpath).extract())
            spider_items['date'] = text(item.xpath(date_xpath).extract())

            yield spider_items

def text(string):
    # 定义complie用于匹配空白符
    replace_compile = re.compile("\s+|\\n+|\\t+")

    # 如果传入参数为可迭代类型，则将其转化为拼接字符串
    if isinstance(string, Iterable):
        string = " ".join(string)

    # 处理空白符
    if isinstance(string, str):
        result, number = re.subn(replace_compile, " ", string)
        return result.strip()
    else:
        return string