# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import csv
import pymongo  #这是连接MongoDb数据库的模块。
from scrapy.utils.project import get_project_settings  #这是读取settings.py文件所需的模块。

settings = get_project_settings()  #读取settings.py文件的数据。

class Cqmmgo0815SpiderMongoPipeline:

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


#'''
'''
class Cqmmgo0815SpiderPipeline:

    def __init__(self):
        self.f = open('cqmmgo_data.csv',mode='a',encoding='utf-8',newline='')
        self.csv_write = csv.DictWriter(self.f,fieldnames=['title_url_full',
                                                           'title',
                                                           'num_read',
                                                           'num_reply',
                                                           'num_collect',
                                                           'publish_time',
                                                           'renew_time',
                                                           'user_name',
                                                           'user_id',
                                                           'user_gender',
                                                           'user_time',
                                                           'user_post_num',
                                                           'user_social',
                                                           'user_fans_num',
                                                           'user_attends_num',
                                                           'user_tool',
                                                           'user_sign',
                                                           'user_url',
                                                           'content_text_str',
                                                           'content_img_url',
                                                           #'user_city',
                                                           ])
        self.csv_write.writeheader()

    def process_item(self, item, spider):
        # 按行写入字典。
        self.csv_write.writerow(dict(item))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.f.close()
'''