import scrapy
from scrapy_redis.spiders import RedisSpider
import redis
import json
import logging
import datetime
from scrapy.exceptions import CloseSpider
# from urllib.parse import urlparse, parse_qs
# import logging
# import requests

# 获取自定义日志记录器
custom_logger = logging.getLogger('custom_logger')

# 获取当前日期和时间
current_time = datetime.datetime.now()

# 获取具体的年、月、日、时、分、秒
year = current_time.year
month = current_time.month
day = current_time.day
hour = current_time.hour
minute = current_time.minute
second = current_time.second

# 打印当前日期和时间
custom_logger.info(f"----------开始爬虫，当前时间是：{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}----------")

class WeiboSearchSpider(RedisSpider):
    name = 'weibo_search'
    allowed_domains = ['m.weibo.cn']
    #start_urls = ['http://m.weibo.cn/']
    redis_key = 'weibo_search:start_urls'

    def __init__(self, *args, **kwargs):
        super(WeiboSearchSpider, self).__init__(*args, **kwargs)
        # 连接到 Redis
        self.redis_conn = redis.StrictRedis(host='139.186.165.94', port=10001, password='',
                                            decode_responses=True)

        # 检查 Redis 连接
        try:
            self.redis_conn.ping()
            custom_logger.info("成功连接到 Redis 服务器")
        except redis.ConnectionError:
            custom_logger.info("无法连接到 Redis 服务器")

    def start_requests(self):


        # user_id = '2050142347'
        # #已在settings.py中设置了默认Headers



        headers = {
            'Accept': 'application/json, text/plain, */*',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Referer': 'https://m.weibo.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'x-xsrf-token':'888ee4',   #观察要爬取的网址“https://m.weibo.cn/profile/info?uid=2050142347”的请求头，发现多了这个参数。那这个参数的值是从哪里来的呢？还要研究一下
           }

        # cookies时不时会变，上面的x-xsrf-token时不时也会变，一定要注意观察待爬取网址的请求头，做相应的修改。
        temp = '_T_WM=2a49f655949fe128a72e77d0c7660284; SCF=An88pjtFAEn9F8u7w53WMXvci1cCd8e6v5TeBL0pj8Sd2fbwpbIhzsSJc3W2b3cq4oS9GXXTNMzIqsZCniJ62ik.; SUB=_2A25Lo-RuDeRhGeNP6VMU8SjEwjSIHXVowXmmrDV6PUJbktAbLWunkW1NTr09mBSJmfd5HmmXxU1czGYJXgMXIqDR; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhKlxWT8Vs0ffppg0hdSMBY5NHD95QfeKzpSK2c1h.RWs4Dqcjsds_09sir; ALF=1724850494; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=888ee4; mweibo_short_token=230e6de4d7; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076032050142347%26fid%3D1005052050142347%26uicode%3D10000011'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        # UserInfoUrl = f'https://m.weibo.cn/profile/info?uid={user_id}'

        # 读取 user_id.txt 文件中的所有 user_id
        file = 'E:\\PycharmProjects\\MadeInChina20240409\\weibo_scrapy\\weibo_scrapy\\spiders\\user_id.txt'
        with open(file, 'r') as file:
            user_ids = file.readlines()

        # 统计成功注入的 URL 数量
        injected_count = 0
        for user_id in user_ids:
            user_id = user_id.strip()
            url = f'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO'
        #     meta = {'user_id': user_id,'url':url, 'cookiejar':1, 'headers':json.dumps(headers), 'scroll_count': 0}
        #     # 判断 URL 是否已存在于 Redis 中
        #     if not self.redis_conn.sismember('visited_urls', url):
        #         # 将生成的 URL 注入到 Redis 列表中
            self.redis_conn.lpush(self.redis_key, url)
        #         # 判断注入是否成功
        #         if result > 0:
        #             injected_count += 1
        #             custom_logger.info(f"成功注入用户 {user_id} 的URL。")
        #             # 将 URL 添加到已访问集合中
        #             self.redis_conn.sadd('visited_urls', url)
        #             # 将元数据注入到 Redis 哈希表中
        #             self.redis_conn.hmset(f'meta:{url}', meta)
        #     else:
        #         custom_logger.info(f"用户 {user_id} 的URL已存在，跳过注入Redis。")
        # # 检查 Redis 列表中的 URL 数量
        # queue_length = self.redis_conn.llen(self.redis_key)
        # custom_logger.info(f"成功注入了 {injected_count} 个 URL至Redis 队列 {self.redis_key} 中，还有 {queue_length} 个待处理的 URL。")
        #
        # if queue_length == 0:
        #     custom_logger.info("Redis 队列为空，关闭爬虫。")
        #     raise CloseSpider(reason='Redis 队列为空')
        # else:
        #     # 生成初始请求
        #     while True:
        #         url = self.redis_conn.lpop(self.redis_key)
        #         if url is None:
        #             break
        #         yield self.make_requests_from_url(url)



            yield scrapy.Request(url = url, headers=headers, cookies=cookies, callback=self.parse, meta={'user_id': user_id,'url':url, 'cookiejar':1, 'headers':headers, 'scroll_count': 0})

    # def make_requests_from_url(self, url):
    #     # 从 Redis 哈希表中获取元数据
    #     meta = self.redis_conn.hgetall(f'meta:{url}')
    #     headers = json.loads(meta.pop('headers'))
    #     return scrapy.Request(url, headers=headers, cookies=meta.get('cookies'), callback=self.parse, meta=meta)

    def parse(self, response):
        #print("响应的文本内容：" + response.text)
        response_data = response.json()
        user_id = response.meta['user_id']  # 获取原始搜索 URL
        scroll_count = response.meta['scroll_count']  # 获取下滚次数
        #meta_url = response.meta['url']
        #headers = response.meta['headers']

        if response_data.get('ok') == 1:
            cards = response_data.get('data', {}).get('cards', [])  #此时，cards是一个列表。

            for card in cards:
                #print(f'第{n}个card: {card}')
                item = {}
                item['since_id'] = response_data.get('data',{}).get('cardlistInfo', {}).get('since_id', None)
                item['user_id'] = user_id
                #print(item['since_id'])
                #print(str(card.get('card_type')) + 'and' + str(card.get('show_type')))
                if card.get('card_type') == 11:
                    #print("----11----")
                    if card.get('show_type') == 3:
                        #print("----3----")
                        for micro_card in card['card_group']:
                            #print(micro_card)
                            item['created_at'] = micro_card['mblog']['created_at']
                            item['id'] = micro_card['mblog']['id']
                            item['text'] = micro_card['mblog']['text']
                            item['source'] = micro_card['mblog'].get('source', '')
                            item['reposts_count'] = micro_card['mblog']['reposts_count']
                            item['comments_count'] = micro_card['mblog']['comments_count']
                            item['reprint_cmt_count'] = micro_card['mblog']['reprint_cmt_count']
                            item['attitudes_count'] = micro_card['mblog']['attitudes_count']
                            item['user_name'] = micro_card['mblog']['user']['screen_name']  #用户名
                            item['user_description'] = micro_card['mblog']['user']['description']  #用户描述
                            item['user_follow_count'] = micro_card['mblog']['user']['follow_count']  #关注者
                            item['user_followers_count'] = micro_card['mblog']['user']['followers_count']  #粉丝数
                            item['user_statuses_count'] = micro_card['mblog']['user']['statuses_count']  #所发微博问题
                            item['user_verified'] = micro_card['mblog']['user']['verified'] #是否认证
                            #print(str(card.get('card_type')) + item['text'])

                            # 检查 'text' 中是否包含特定子字符串，即是否还未显示完全文。
                            if f'''<a href="/status/{item['id']}">全文</a>''' in item['text']:
                                #print(item['text'])
                                status_url = f"https://m.weibo.cn/statuses/extend?id={item['id']}"
                                yield scrapy.Request(status_url,
                                                     callback=self.parse_status,
                                                     meta={'item': item, 'cookiejar': response.meta.get('cookiejar'),
                                                           'headers': response.meta.get('headers')})
                            else:
                                yield item
                elif card.get('card_type') == 9:
                    item['created_at'] = card['mblog']['created_at']
                    item['id'] = card['mblog']['id']
                    item['text'] = card['mblog']['text']
                    item['source'] = card['mblog'].get('source', '')
                    item['reposts_count'] = card['mblog']['reposts_count']
                    item['comments_count'] = card['mblog']['comments_count']
                    item['reprint_cmt_count'] = card['mblog']['reprint_cmt_count']
                    item['attitudes_count'] = card['mblog']['attitudes_count']
                    if 'user_name' not in item:
                        item['user_name'] = card['mblog']['user']['screen_name']  # 用户名
                        item['user_description'] = card['mblog']['user']['description']  # 用户描述
                        item['user_follow_count'] = card['mblog']['user']['follow_count']  # 关注者
                        item['user_followers_count'] = card['mblog']['user']['followers_count']  # 粉丝数
                        item['user_statuses_count'] = card['mblog']['user']['statuses_count']  # 所发微博总数
                        item['user_verified'] = card['mblog']['user']['verified']  # 是否认证
                    #print(str(card.get('card_type')) + item['text'])

                    # 检查 'text' 中是否包含特定子字符串，即是否还未显示完全文。
                    if f'''<a href="/status/{item['id']}">全文</a>''' in item['text']:
                        status_url = f"https://m.weibo.cn/statuses/extend?id={item['id']}"
                        yield scrapy.Request(status_url,
                                             callback=self.parse_status,
                                             meta={'item': item, 'cookiejar': response.meta.get('cookiejar'),
                                                   'headers': response.meta.get('headers')})
                    else:
                        yield item

        # 增加下滚次数
        n = item['user_statuses_count'] // 10
        custom_logger.info(f"id为 {item['user_id']} 的用户总共发了 {item['user_statuses_count']} 条微博，已下滚次数:  {scroll_count} （每次约10条）,预计还会滚动 {n} 次。下一页id为 {item['since_id']} ")
        scroll_count += 1

        if item['since_id']:
            new_url = f"https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&since_id={item['since_id']}"
            yield scrapy.Request(new_url, callback=self.parse,
                                 meta={'cookiejar': response.meta['cookiejar'],
                                       'headers': response.meta['headers'], 'scroll_count': scroll_count, 'user_id': user_id})

    # 显示全文
    def parse_status(self, response):
        response_data = response.json()
        item = response.meta['item']
        #print(item['id'])

        if response_data.get('ok') == 1:
            item['text'] = response_data.get('data',{}).get('longTextContent',{})
            #print(item['text'])
        yield item

    def close(self, reason):
        queue_length = self.redis_conn.llen(self.redis_key)
        if queue_length == 0:
            custom_logger.info("目前 Redis 库中已经没有要爬取的网址，因此结束爬取。")
            self.crawler.engine.close_spider(self, reason="Redis 队列为空")
