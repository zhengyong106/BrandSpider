import json
import scrapy

from BrandSpider.items import BrandSpiderItem


class YilongdaiSpider(scrapy.Spider):
    name = "yilongdai"
    allowed_domains = ["eloancn.com"]
    headers = {"Accept": "application/json, text/plain, */*",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}

    # 该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request。
    def start_requests(self):
        return [scrapy.FormRequest("https://licai.eloancn.com/pcgway/app002/v1/01", headers=self.headers, formdata ={"pageNo": str(i), "pageSize": "10"}, callback=self.parse) for i in range(1, 3)]

    def parse(self, response):
        json_dict = json.loads(response.body)

        for item in json_dict["data"]["list"]:
            spider_items = BrandSpiderItem()
            spider_items['url'] = response.url
            spider_items['id'] = item["prodId"]
            spider_items['price'] = item["borrowAmountStr"]
            spider_items['date'] = item["pubdate"]
            yield spider_items
