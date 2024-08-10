# @-*- coding = utf-8 _*_
# @Time : 2024/8/7 6:05
# @Author : 杨昌军
# @File : lpush_to_redis.py
# @Software : PyCharm

import redis
import time
from weibo_scrapy import settings
import os
import requests
import scrapy
from scrapy.utils.request import request_fingerprint

# 注意，只能将待爬取网址推送到start_urls中，不能直接推送到requests中，否则会出错，已测试过。

# 从settings.py里获取redis连接信息
host = settings.REDIS_HOST
port = settings.REDIS_PORT
db = settings.REDIS_DB
bot_name = settings.redis_name

# 从seeting.py里获取请求头和cookies
headers = settings.headers
cookies = settings.cookies

# 基础 URL 模板
url_template = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO'
continue_url_template = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&since_id={since_id}'

redis_key = f'{bot_name}:start_urls'  # 起始页面库
dupefilter_key = f"{bot_name}:dupefilter"  # 已爬页面库
queue_key = f'{bot_name}:requests' # 请求队列库
since_key = f'{bot_name}:since_id' # since_id队列

while True:
    try:
        redis_conn = redis.StrictRedis(host=host, port=port, db=db, socket_timeout=10)
        redis_conn.ping()
        print("Redis 连接成功")
        break
    except (ConnectionError, TimeoutError):
        print("连接到 Redis 服务器失败，正在重试...")
        time.sleep(5)

# ----------调试----------

# user_id = '2050142347'
# since_id = '4929583138217713'
#
#
# url  = continue_url_template.format(user_id=user_id, since_id=since_id)
#
# redis_conn.lpush(redis_key, url)
# print(f'推送 {url} 成功。')

#----------调试结束----------

# 获取users_id.txt文件的相对路径
current_dir = os.path.dirname(__file__)  # 获取当前文件的目录
file_path = os.path.join(current_dir, 'users_id.txt')  # 构建 user_id.txt 文件的相对路径
file_path = os.path.abspath(file_path)  # 规范化路径

# 打开 TXT 文件
with open(file_path, 'r', encoding='utf-8') as txtfile:
    # 读取所有行，并去除换行符
    lines = [line.strip() for line in txtfile.readlines()]

# 循环读取每一行数据
n = 0
for user_id in lines:
    # 确保 user_id 没有多余的空格或换行符
    user_id = user_id.strip()

    # 从 weibo_search:since_id 哈希表中获取与 user_id 相关的键
    matching_keys = [key for key in redis_conn.hkeys(since_key) if key.decode('utf-8').startswith(f'{user_id}:')]

    if matching_keys:
        for key in matching_keys:
            key_str = key.decode('utf-8')
            old_since_id = redis_conn.hget(since_key, key).decode('utf-8')
            old_url = continue_url_template.format(user_id=user_id, since_id=old_since_id)
            response = requests.get(old_url, headers=headers, cookies=cookies)
            json_data = response.json()
            new_since_id = json_data.get('data', {}).get('cardlistInfo', {}).get('since_id')
            if new_since_id:
                url = continue_url_template.format(user_id=user_id, since_id=new_since_id)
                request = scrapy.Request(url)
                request_fp = request_fingerprint(request)
                if redis_conn.sismember(dupefilter_key, request_fp):
                    print(f"未注入：已被爬取过，有重复。链接：{url}")
                else:
                    redis_conn.lpush(redis_key, url)
                    print(f"注入：未被爬取。链接: {url}")
                    n += 1
            else:
                user_url = f"https://weibo.com/u/{user_id}"
                print(f"未注入：用户 {user_id} 可能已爬取完毕。检查一下。用户主页：{user_url}。爬取链接：{old_url}")
    else:
        url = url_template.format(user_id=user_id)
        redis_conn.lpush(redis_key, url)
        print(f"注入：新用户 {user_id} 的起始页。链接：{url}")
        n += 1

print(f"成功推送 {n} 条url至Redis的 {redis_key} 库。")