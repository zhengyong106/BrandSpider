import re
import json
import scrapy
from collections import Iterable

from BrandSpider.items import BrandSpiderItem


class YingzongtongSpider(scrapy.Spider):
    name = "yingzongtong"
    allowed_domains = ["yingzt.com"]
    start_urls = ["https://www.yingzt.com/invest/list"]

    def parse(self, response):
        items_xpath = "//li[contains(@class,'invalid-project')]"

        id_xpath = ".//a[contains(@class,'weak-fontc')]/@href"
        price_xpath = ".//*[contains(text(),'项目总额')]/..//text()"

        for item in response.xpath(items_xpath):
            spider_items = BrandSpiderItem()
            spider_items['url'] = response.url
            spider_items['id'] = text(item.xpath(id_xpath).extract())
            spider_items['price'] = text(item.xpath(price_xpath).extract())

            id_compile = re.compile("id=([0-9a-zA-Z]+)")
            id = id_compile.search(spider_items['id']).group(1)
            yield scrapy.FormRequest("https://www.yingzt.com/invest/apiUserInvests?app_ver=2", headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}, formdata={"id": id}, meta={"spider_items": spider_items}, callback=self.parse_date)

    def parse_date(self, response):
        spider_items = response.meta['spider_items']


        date_xpath = "//td[3]/text()"
        spider_items['date'] = text(response.xpath(date_xpath).extract())

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

def url(string):
    string = str(string)
    if string.startswith("http"):
        return string
    elif string.startswith("/"):
        return "https://www.yingzt.com" + string
    else:
        return "https://www.yingzt.com/" + string