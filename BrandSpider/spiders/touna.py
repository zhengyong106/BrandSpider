import json
import time
import scrapy

from BrandSpider.items import BrandSpiderItem


class TounaSpider(scrapy.Spider):
    name = "touna"
    allowed_domains = ["touna.cn"]
    start_urls = ["https://www.touna.cn/borrow.do?method=list&status=-2&borrowType=-1&creditType=&timeLimit=&keyType=0&keyWord=&page=" + str(i) + "&size=10&subtime=" + str(int(time.time() * 1000)) for i in range(100)]

    def parse(self, response):
        json_dict = json.loads(response.body)

        for item in json_dict["result"]["list"]:
            spider_items = BrandSpiderItem()
            spider_items['url'] = response.url
            spider_items['id'] = item["user_id"]
            spider_items['price'] = item["account"]
            spider_items['date'] = item["pubtime"]
            yield spider_items
