import logging
import time

import scrapy

from BrandSpider.items import DailyTurnoverItem
from BrandSpider.middlewares import SeleniumRequest

logger = logging.getLogger(__name__)
class MySpider(scrapy.Spider):
    name = "leijichengjiao"
    start_urls = [
        {
            "site": "人人贷",
            "url": "https://www.renrendai.com/about/operate/dataReveal",
            "element_xpath": "//*[contains(text(),'累计成交金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "拍拍贷",
            "url": "https://map.invest.ppdai.com",
            "element_xpath": "//*[contains(text(),'累计成交总额')]/following-sibling::*[1]",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "微贷",
            "url": "https://www.weidai.com.cn/home/index/index.html",
            "element_xpath": "//*[contains(text(),'累计成交额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "点融",
            "url": "https://www.dianrong.com/market",
            "element_xpath": "//*[contains(text(),'当年成交金额')][contains(@class,'title')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "积木",
            "url": "https://www.jimu.com/Home/Security",
            "element_xpath": "//*[contains(text(),'累计交易量')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "投哪",
            "url": "https://www.touna.cn/",
            "element_xpath": "//*[contains(text(),'累计成交金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "有利",
            "url": "https://www.yooli.com/",
            "element_xpath": "//*[contains(text(),'交易总额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "爱钱进",
            "url": "https://www.iqianjin.com/",
            "element_xpath": "//*[contains(text(),'已完成出借金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "翼龙贷",
            "url": "https://www.eloancn.com/",
            "element_js": 'var el = document.getElementById("volumenum")\n'\
                          'el.setAttribute("id", "new_volumenum")\n'\
                          'el.innerHTML = nowmoneys',
            "element_xpath": "//*[contains(text(),'成交额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "麻袋财富",
            "url": "https://www.madailicai.com/",
            "element_xpath": "//*[contains(text(),'累计投资金额 ')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "和信贷",
            "url": "https://www.hexindai.com",
            "element_xpath": "//p[contains(text(),'累计成交额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "小赢理财",
            "url": "https://www.xiaoying.com/",
            "element_xpath": "//*[contains(text(),'为用户赚取')]",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "宜信贷",
            "url": "http://www.yidai.com/",
            "element_xpath": "//*[contains(text(),'累计交易总额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "向上金服",
            "url": "https://www.xiangshang360.cn/xweb/index/",
            "element_xpath": "//*[contains(text(),'累计成交业务额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "PPMoney",
            "url": "https://www.ppmoney.com/",
            "element_xpath": "//*[contains(text(),'累计现金交易总额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "理财农场",
            "url": "https://www.lcfarm.com/",
            "element_xpath": "//*[contains(text(),'累计成交额')]",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "你我贷",
            "url": "http://www.niwodai.com/",
            "element_xpath": "//span[contains(text(),'累计交易金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "博金贷",
            "url": "https://www.bjdp2p.com/toDataInfo.page",
            "element_xpath": "//*[contains(text(),'累计借贷金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "银湖网",
            "url": "https://www.yinhu.com/main.bl",
            "element_xpath": "//*[contains(text(),'累计出借金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        },
        {
            "site": "杉易贷",
            "url": "https://www.33lend.com",
            "element_xpath": "//*[contains(text(),'累计借贷金额')]/..",
            "element_regex": "((?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?(?:[\d.,\s]+(?:[(（]?(?:万元|万|亿元|亿|元)[）)]?)?)+)"
        }
    ]

    def start_requests(self):
        for url_dict in self.start_urls:
            yield SeleniumRequest(url_dict["url"], self.parse, meta=url_dict)

    def parse(self, response):
        local_time = time.localtime(time.time())
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        spider_items = DailyTurnoverItem()
        spider_items['site'] = response.meta['site']
        spider_items['url'] = response.url
        spider_items['turnover'] = response.meta["element_text"].strip()
        spider_items['date'] = local_time

        yield spider_items