# -*- coding: utf-8 -*-
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BrandSpiderPipeline(object):
    collection_name = 'brand_items'

    def __init__(self, url, username, password, db):
        self.url = url
        self.username = username
        self.password = password
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=crawler.settings.get("MYSQL_URL"),
            username=crawler.settings.get("MYSQL_USERNAME"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            db=crawler.settings.get("MYSQL_DB")
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.url, self.username, self.password, self.db)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        create_sql = '''CREATE TABLE IF NOT EXISTS Spider.leijichengjiao_v1 (
            site varchar(255) NOT NULL, 
            date datetime(0) NOT NULL, 
            turnover varchar(255) NULL, 
            url varchar(255) NULL,
            PRIMARY KEY (site, date)
        );'''

        delete_sql = '''DELETE FROM Spider.leijichengjiao_v1 
            WHERE site='%s' AND date(date) = CURRENT_DATE'''% item.get("site")

        insert_sql = '''INSERT INTO Spider.leijichengjiao_v1 ( site, date, url, turnover ) 
            VALUES ( '%s', '%s', '%s', '%s' )''' % (item.get("site"), item.get("date"), item.get("url"), item.get("turnover"))

        try:
            cursor.execute(create_sql)
            cursor.execute(delete_sql)
            cursor.execute(insert_sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        return item
