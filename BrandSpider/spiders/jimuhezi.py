import re
import scrapy
from collections import Iterable

from BrandSpider.items import BrandSpiderItem


class JimuheziSpider(scrapy.Spider):
    name = "jimuhezi"
    allowed_domains = ["jimu.com"]
    start_urls = ["https://box.jimu.com/Project/List?rate=&guarantee=&range=&page=" + str(i) + "&category=&status=" for i in range(1, 50)]

    def parse(self, response):
        items_xpath = "//div[@class='row']/div[@class='span3']"

        id_xpath = "./a/@href"
        price_xpath = ".//p[@class='project-info']//text()"
        date_xpath = ".//div[@class='subtitle']/text()"

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
        return result.strip().encode("utf-8")
    else:
        return string
