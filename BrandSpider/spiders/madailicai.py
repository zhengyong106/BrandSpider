import re
import scrapy
from collections import Iterable

from BrandSpider.items import BrandSpiderItem


class MadailicaiSpider(scrapy.Spider):
    name = "madailicai"
    allowed_domains = ["madailicai.com"]
    start_urls = ["https://www.madailicai.com/product/list/" + str(i) for i in range(1, 10)]
    start_urls += ["https://www.madailicai.com/whiteCollar/list/" + str(i) for i in range(1, 10)]
    start_urls += ["https://www.madailicai.com/huaTuanBao/list/" + str(i) for i in range(1, 10)]
    start_urls += ["https://www.madailicai.com/huaTuanBao/transfers/" + str(i) for i in range(1, 10)]

    def parse(self, response):
        items_xpath = "//ul[contains(@class,'goods-list')]//li"

        id_xpath = ".//a/@href"
        price_xpath = ".//p[contains(text(), '元')]//text()"

        for item in response.xpath(items_xpath):
            spider_items = BrandSpiderItem()
            spider_items['url'] = response.url
            spider_items['id'] = text(item.xpath(id_xpath).extract())
            spider_items['price'] = text(item.xpath(price_xpath).extract())

            yield scrapy.Request(url(spider_items['id']), meta={"spider_items": spider_items}, callback=self.parse_date)

    def parse_date(self, response):
        date_xpath = "//li[contains(text(),'开售')]/text()"

        spider_items = response.meta['spider_items']
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
        return "https://www.madailicai.com" + string
    else:
        return "https://www.madailicai.com/" + string