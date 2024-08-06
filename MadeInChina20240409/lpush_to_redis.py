# @-*- coding = utf-8 _*_
# @Time : 2024/8/7 6:05
# @Author : 杨昌军
# @File : lpush_to_redis.py
# @Software : PyCharm

import redis
import os

# 连接到 Redis
redis_conn = redis.StrictRedis(host='139.186.165.94', port=10001, db=0)

redis_key = 'weibo_search:start_urls'

# 基础 URL 模板
url_template = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}&containerid=100505{user_id}'

# 获取users_id.txt文件的相对路径
current_dir = os.path.dirname(__file__)  # 获取当前文件的目录
file_path = os.path.join(current_dir, 'users_id.txt')  # 构建 user_id.txt 文件的相对路径
file_path = os.path.abspath(file_path)  # 规范化路径

# 从文件中读取user_id
with open(file_path, 'r') as file:
    user_ids = file.readlines()

# 逐行读取微博用户ID
n = 0
for user_id in user_ids:
    user_id = user_id.strip()
    url = url_template.format(user_id=user_id)

    # 使用 lpush 推动多个 URL 到 Redis 列表
    redis_conn.lpush(redis_key, url)

    print(f"推送 {url} 至Redis。")

    n += 1

print(f"成功推送 {n} 条URL至Redis。")


