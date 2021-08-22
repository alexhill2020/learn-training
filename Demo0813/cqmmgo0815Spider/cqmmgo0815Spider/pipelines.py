# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import csv

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
