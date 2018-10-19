# -*- coding:utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
'''
在爬虫文件夹下面自定义一个main.py的文件
__file__指的是当前main.py文件
os.path.abspath(__file__)获取当前main.py文件所在路径
os.path.dirname(os.path.abspath(__file__))获取的是当前文件夹的父目录的路径,也就是爬虫文件的目录
execute里面的参数是要调试的爬虫
执行main.py就可以在PyCharm中调试程序了

'''
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'test', '-o', 'leijichengjiao.csv'])
