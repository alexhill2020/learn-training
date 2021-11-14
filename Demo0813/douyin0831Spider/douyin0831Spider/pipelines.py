# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo  #这是连接MongoDb数据库的模块。
from scrapy.utils.project import get_project_settings  #这是读取settings.py文件所需的模块。

settings = get_project_settings()  #读取settings.py文件的数据。


class Douyin0831SpiderMongoPipeline:

    def __init__(self):
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']  # 数据库名
        sheetname = settings['MONGODB_SHEETNAME']  #表名

        client = pymongo.MongoClient(host=host, port=port)  #连接MongoDb数据库并实体化为client。

        mydb = client[dbname]  #创建数据库。
        self.sheet = mydb[sheetname]  #在创建的数据库中创建表。

        #tdb = client[dbname]   #数据库名，没有则新建。
        #self.port = tdb[settings['MONGODB_COLLECTION']]  # 表名，没有则新建。

    def process_item(self, item, spider):
        try:
            love_info = dict(item)  #这里的item是从item.py中传过来的。
            self.sheet.insert(love_info)  #在上面创建的表中写入数据，字典格式的。
            return item
        except Exception as e:
            print('存入数据库时出错',e)

class Video0901SpiderMongoPipeline:

    def __init__(self):
        host = settings['MONGODB_SERVER']
        port = settings['MONGODB_PORT']
        dbname = 'video0901'  # 数据库名
        sheetname = '111'  #表名

        client = pymongo.MongoClient(host=host, port=port)  #连接MongoDb数据库并实体化为client。

        mydb = client[dbname]  #创建数据库。
        self.sheet = mydb[sheetname]  #在创建的数据库中创建表。

        #tdb = client[dbname]   #数据库名，没有则新建。
        #self.port = tdb[settings['MONGODB_COLLECTION']]  # 表名，没有则新建。

    def process_item(self, item, spider):
        try:
            love_info = dict(item)  #这里的item是从item.py中传过来的。
            self.sheet.insert(love_info)  #在上面创建的表中写入数据，字典格式的。
            return item
        except Exception as e:
            print('存入数据库时出错',e)
