import re
import time
import json
import scrapy
from collections import Iterable

from BrandSpider.items import BrandSpiderItem


class XiangshangjinfuSpider(scrapy.Spider):
    name = "xiangshangjinfu"
    allowed_domains = ["xiangshang360.cn"]
    start_urls = ["https://www.xiangshang360.cn/xweb/actProduct/list?planIds=init&pageNum=" + str(i) + "&_=" + str(int(time.time() * 1000)) for i in range(1, 940)] #940

    def parse(self, response):
        json_dict = json.loads(response.body)

        for item in json_dict["data"]["biddingList"]:
            spider_items = BrandSpiderItem()
            spider_items['url'] = response.url
            spider_items['id'] = item["plnKey"]
            spider_items['price'] = item["totalAmount"]

            yield scrapy.Request("https://www.xiangshang360.cn/xweb/actProduct/actProductInfo?plnKey=" + spider_items['id'], meta={"spider_items": spider_items}, callback=self.parse_date)

    def parse_date(self, response):
        date_xpath = "//span[contains(text(),'申请日期')]/..//text()"

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