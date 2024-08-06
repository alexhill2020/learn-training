# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo  #这是连接MongoDb数据库的模块。
from scrapy.utils.project import get_project_settings  #这是读取settings.py文件所需的模块。
from scrapy.exceptions import CloseSpider
import logging

# 获取自定义日志记录器
custom_logger = logging.getLogger('custom_logger')

settings = get_project_settings()  #读取settings.py文件的数据。

class WeiboScrapyMongoPipeline:

    def __init__(self):
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        dbname = 'weibo_search_20240805'  # 数据库名
        sheetname = 'weibo_search_main_20240805'  #表名

        client = pymongo.MongoClient(host=host, port=port)  #连接MongoDb数据库并实体化为client。

        mydb = client[dbname]  #创建数据库。
        self.sheet = mydb[sheetname]  #在创建的数据库中创建表。

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