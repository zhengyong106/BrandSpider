# coding=utf-8
import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://news.baidu.com')
time.sleep(1)

news_link = driver.find_element_by_xpath("//*[@id='pane-news']/div/ul/li[1]/strong/a")
page1_title_string = news_link.text  # 得到页面A新闻标题
news_link.click()  # 点击新闻链接
time.sleep(1)
handles = driver.window_handles

for handle in handles:  # 切换窗口（切换到搜狗）
    if handle != driver.current_window_handle:
        print
        'switch to second window', handle
        driver.close()  # 关闭第一个窗口
        driver.switch_to.window(handle)  # 切换到第二个窗口
page2_title_string = driver.find_element_by_xpath("//*[@id='yc_con_txt']/p[1]").text  # 详情页有一个原标题

try:
    assert page1_title_string in page2_title_string  # 判断页面B标题是否包含页面A标题
    print('Test Pass.')
except Exception as e:
    print('Test Fail')