# @-*- coding = utf-8 _*_
# @Time : 2024/8/7 6:05
# @Author : 杨昌军
# @File : lpush_to_redis.py
# @Software : PyCharm

import redis
import os
import csv
import scrapy
from weibo_scrapy import settings
from scrapy.utils.request import request_fingerprint

# 注意，只能将待爬取网址推送到start_urls中，不能直接推送到requests中，否则会出错，已测试过。

# 从settings.py里获取redis连接信息
host = settings.REDIS_HOST
port = settings.REDIS_PORT
db = settings.REDIS_DB
bot_name = settings.redis_name

# 连接到Redis
redis_conn = redis.StrictRedis(host=host, port=port, db=db)
redis_key = f'{bot_name}:start_urls'  # 起始页面库
dupefilter_key = f"{bot_name}:dupefilter"  # 已爬页面库
queue_key = f'{bot_name}:requests' # 请求队列库

# 基础 URL 模板
url_template = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO'
continue_url_template = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&since_id={since_id}'

# 获取users_id.txt文件的相对路径
current_dir = os.path.dirname(__file__)  # 获取当前文件的目录
file_path = os.path.join(current_dir, 'users_id.csv')  # 构建 user_id.txt 文件的相对路径
file_path = os.path.abspath(file_path)  # 规范化路径

# 打开 CSV 文件
with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
    # 创建 CSV 读取器
    csvreader = csv.reader(csvfile)

    # 读取表头
    header = next(csvreader)
    # print(f"Header: {header}")

    # 循环读取每一行数据
    n = 0
    for row in csvreader:
        user_id = row[0]
        new_since_id = row[2]

        if new_since_id:
            url = continue_url_template.format(user_id=user_id, since_id=new_since_id)
        else:
            url = url_template.format(user_id=user_id)

        # 创建一个 Scrapy 请求对象
        request = scrapy.Request(url)
        # 计算请求的指纹，以查询网址是否已经被爬取
        request_fp = request_fingerprint(request)

        # 检查该网址的指纹是否已经存在于去重过滤器中
        if redis_conn.sismember(dupefilter_key, request_fp):
            print(f"链接 {url} 已经被爬取过，未注入。")
        else:
             redis_conn.lpush(redis_key, url)
             print(f"链接 {url} 还没有被爬取，已经注入start_urls中")
             n += 1

    print(f"成功推送 {n} 条url至Redis的 {redis_key} 库。")

