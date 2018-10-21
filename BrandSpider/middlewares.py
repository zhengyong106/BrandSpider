import re
import time
import scrapy
from scrapy.middleware import logger
from selenium import webdriver
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self):
        self.browser = webdriver.Chrome()

    def process_request(self, request, spider):
        # 依靠meta中的标记，来决定是否需要使用selenium来爬取
        use_selenium = request.meta.get('use_selenium', False)
        element_text = None
        if use_selenium:
            try:
                # 设置脚本加载超时为5秒
                self.browser.set_script_timeout(5)
                # 打开请求链接
                self.browser.get(request.url)
                # 获取请求元数据
                element_js = request.meta.get("element_js")
                element_xpath = request.meta.get("element_xpath")
                element_regex = request.meta.get("element_regex")

                if element_js:
                    self.browser.execute_script(element_js)

                # 依靠Xpath表达式作为预期条件，等待直到元素加载完成
                if element_xpath:
                    locator = (By.XPATH, element_xpath)
                    element = WebDriverWait(self.browser, 2).until(EC.presence_of_element_located(locator), "预期条件[%s] 等待加载超时：URL %s" %(element_xpath, request.url))
                    element_text = element.text
                    # 依靠正则表达式作为预期条件，等待直到元素加载完成
                    if element_regex:
                        element_compile = re.compile(element_regex)
                        WebDriverWait(self.browser, 10).until(lambda driver: element_compile.search(element.text), "预期条件[%s] 等待加载超时：URL %s" %(element_xpath, request.url))
                        # 休息两秒后再获取元素值
                        time.sleep(2)
                        element_text = element_compile.search(element.text).group(1)

            except TimeoutException as e:
                logger.error(e.msg)
                return HtmlResponse(url=request.url, request=request, status=500)
            else:
                request.meta["element_text"] = element_text
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)

    def spider_opened(self, spider):
        pass

class SeleniumRequest(scrapy.Request):

    def __init__(self, url, callback=None, method='GET', headers=None, body=None,
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None, flags=None):
        meta = meta if meta else dict()
        meta["use_selenium"] = True
        super(SeleniumRequest, self).__init__(url, callback=callback, method=method, headers=headers, body=body, cookies=cookies, meta=meta, encoding=encoding, priority=priority, dont_filter=dont_filter, errback=errback, flags=flags)