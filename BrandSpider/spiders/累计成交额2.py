import re
import time
import scrapy
from collections import Iterable
from scrapy_splash import SplashRequest
from BrandSpider.items import DailyTurnoverItem


# docker run -p 8050:8050 scrapinghub/splash
from BrandSpider.middlewares import SeleniumRequest


class MySpider(scrapy.Spider):
    name = "test"
    start_urls = [{
		"site": "人人贷",
		"url": "https://www.renrendai.com/about/operate/dataReveal",
		"turnover_xpath": "//*[contains(text(),'累计成交金额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计成交金额')]"
	},
	{
		"site": "拍拍贷",
		"url": "https://map.invest.ppdai.com/",
		"turnover_xpath": "//*[contains(text(),'累计成交总额')]/following-sibling::*[1]//text()",
		"until_xpath": "//*[contains(text(),'累计成交总额')]"
	},
	{
		"site": "微贷",
		"url": "https://www.weidai.com.cn/home/index/index.html",
		"turnover_xpath": "//*[contains(text(),'累计成交额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计成交额')]"
	},
	{
		"site": "点融",
		"url": "https://www.dianrong.com/market",
		"turnover_xpath": "//*[contains(text(),'当年成交金额')][contains(@class,'title')]/..//text()",
		"until_xpath": "//*[contains(text(),'当年成交金额')]"
	},
	{
		"site": "积木",
		"url": "https://www.jimu.com/Home/Security",
		"turnover_xpath": "//*[contains(text(),'累计交易量')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计交易量')]"
	},
	{
		"site": "投哪",
		"url": "https://www.touna.cn/",
		"turnover_xpath": "//*[contains(text(),'累计成交金额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计成交金额')]"
	},
	{
		"site": "有利",
		"url": "https://www.yooli.com/",
		"turnover_xpath": "//*[contains(text(),'交易总额')]/..//text()",
		"until_xpath": "//*[contains(text(),'交易总额')]"
	},
	{
		"site": "爱钱进",
		"url": "https://www.iqianjin.com/",
		"turnover_xpath": "//*[contains(text(),'已完成出借金额')]/..//text()",
		"until_xpath": "//*[contains(text(),'已完成出借金额')]"
	},
	{
		"site": "翼龙贷",
		"url": "https://www.eloancn.com/",
		"turnover_xpath": "//*[contains(text(),'成交额')]/..//text()",
		"until_xpath": "//*[contains(text(),'成交额')]"
	},
    {
		"site": "麻袋财富",
		"url": "https://www.madailicai.com/",
		"turnover_xpath": "//*[contains(text(),'累计投资金额 ')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计投资金额')]"
	},
	{
		"site": "和信贷",
		"url": "https://www.hexindai.com",
		"turnover_xpath": "//p[contains(text(),'累计成交额')]/..//text()",
		"until_xpath": "//p[contains(text(),'累计成交额')]"
	},
	{
		"site": "小赢理财",
		"url": "https://www.xiaoying.com/",
		"turnover_xpath": "//*[contains(text(),'为用户赚取')]//text()",
		"until_xpath": "//*[contains(text(),'为用户赚取')]"
	},
	{
		"site": "宜信贷",
		"url": "http://www.yidai.com/",
		"turnover_xpath": "//*[contains(text(),'累计交易总额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计交易总额')]"
	},
	{
		"site": "向上金服",
		"url": "https://www.xiangshang360.cn/xweb/index/",
		"turnover_xpath": "//*[contains(text(),'累计成交业务额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计成交业务额')]"
	},
	{
		"site": "PPMoney",
		"url": "https://www.ppmoney.com/",
		"turnover_xpath": "//*[contains(text(),'累计现金交易总额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计现金交易总额')]"
	},
	{
		"site": "理财农场",
		"url": "https://www.lcfarm.com/",
		"turnover_xpath": "//*[contains(text(),'累计成交额')]//text()",
		"until_xpath": "//*[contains(text(),'累计成交额')]"
	},
	{
		"site": "你我贷",
		"url": "http://www.niwodai.com/",
		"turnover_xpath": "//span[contains(text(),'累计交易金额')]/..//text()",
		"until_xpath": "//span[contains(text(),'累计交易金额')]"
	},
	{
		"site": "博金贷",
		"url": "https://www.bjdp2p.com/toDataInfo.page",
		"turnover_xpath": "//*[contains(text(),'累计借贷金额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计借贷金额')]"
	},
	{
		"site": "银湖网",
		"url": "https://www.yinhu.com/main.bl",
		"turnover_xpath": "//*[contains(text(),'累计出借金额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计出借金额')]"
	},
	{
		"site": "杉易贷",
		"url": "https://www.33lend.com",
		"turnover_xpath": "//*[contains(text(),'累计借贷金额')]/..//text()",
		"until_xpath": "//*[contains(text(),'累计借贷金额')]"
	},
]

    def start_requests(self):
        for url_dict in self.start_urls:
            yield SeleniumRequest(url_dict["url"], self.parse, meta=url_dict)

    def parse(self, response):
        local_time = time.localtime(time.time())
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        turnover_xpath = response.meta['turnover_xpath']

        spider_items = DailyTurnoverItem()
        spider_items['site'] = response.meta['site']
        spider_items['url'] = response.url
        spider_items['turnover'] = text(response.xpath(turnover_xpath).extract())
        spider_items['date'] = local_time

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