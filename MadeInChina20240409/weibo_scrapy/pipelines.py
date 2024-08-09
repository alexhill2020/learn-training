# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from pymongo import MongoClient
from scrapy.exceptions import CloseSpider
import logging
from weibo_scrapy import settings

# 获取自定义日志记录器
custom_logger = logging.getLogger('custom_logger')

class WeiboScrapyMongoPipeline:

    def __init__(self):
        host = settings.MONGODB_SERVER  # ip地址
        port = settings.MONGODB_PORT  # 端口
        username = settings.MONGODB_USER  # 用户名
        password = settings.MONGODB_PWD  # 密码
        audb = settings.MONGODB_AUDB  # 用于认证的数据库
        dbname = settings.MONGODB_DBNAME  # 数据库名
        sheetname = settings.MONGODB_SHEETNAME  #表名

        connection_string = f"mongodb://{username}:{password}@{host}:{port}/{audb}"  # 连接mongodb的地址字符串

        # 创建MongoDB客户端
        self.client = MongoClient(connection_string)

        self.mydb = self.client[dbname]  #连接数据库，如没有则创建。
        self.sheet = self.mydb[sheetname]  #连接数据库中的表，如没有则创建。

    def process_item(self, item, spider):
        try:
            main_info = dict(item)  #这里的item是从item.py中传过来的。
            self.sheet.insert(main_info)  #在上面创建的表中写入数据，字典格式的。
            return item
        except Exception as e:
            #print('存入数据库时出错',e)
            custom_logger.error(f"数据存储失败: {e}")
            spider.crawler.engine.close_spider(spider, reason="MongoDB 数据存储失败。")
            raise CloseSpider(reason="MongoDB 数据存储失败。")