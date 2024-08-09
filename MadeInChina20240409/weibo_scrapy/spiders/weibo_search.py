import scrapy
import re
import logging
import redis
import time
from datetime import datetime, timezone
from weibo_scrapy.items import WeiboScrapyItem
from scrapy_redis.spiders import RedisSpider
from redis.exceptions import ConnectionError, TimeoutError
from weibo_scrapy import settings


# 事实证明在断点续爬的时候只要redis的weibo_search:request里有网址，则会继续爬，没有网址，或者是只有爬完就结束的网址，则不会继续爬。
# 因此实现断点续爬的关键点就是如何确保其request里一直有网址，没有网址的原因是URL处理速度快于URL的生成速度，导致Redis队列中的URL被迅速处理完，从而无法维持持续的抓取。
# 研究了一晚上，断点续爬没有更好的方式了，主要是不能确保weibo_search:request里一定会有可以延伸的网址，目前只能是这个样子了。
# 要解决此问题主要有两种方式：确保有足够的初始URL、并发请求数减少（settings.py中设置），本来想动态生态url再手工推送到requests列，但细想+试验证明并不行，因此本来产生的url就全部都要推送过去，手工推送只是白用工。
# 注意要多看日志，不运行了肯定就是出问题了。
# 同时推送到start_urls里才能同时抓取，如果分批次推送的话，则只有第一批推送的才抓取，后面推送的会在start_urls里等着，直到爬虫下一次启动。因此尽量一次多推送一点，然后等爬等差不多了再等集中启动下一批的。

# 获取自定义日志记录器
custom_logger = logging.getLogger('custom_logger')  #已在setting.py中设置好

# 获取当前日期和时间
current_time = datetime.now()

# 打印当前日期和时间
custom_logger.info(f"----------开始爬虫，当前时间是：{current_time}----------")

# 定义爬取微博的时间范围
start_date = datetime(2017, 10, 18, tzinfo=timezone.utc)  #后面是添加时区信息
end_date = datetime(2024, 7, 31, tzinfo=timezone.utc)

class WeiboSearchSpider(RedisSpider):
    name = 'weibo_search'
    # allowed_domains = ['m.weibo.cn']  # 利用redis进行分布式爬虫需注销掉这个
    redis_key = f'{name}start_urls' # 用Redis进行分布式爬虫时用于存储初始URL的 Redis key

    # 以下为全局抓取中要用到的url，这里先定义了，方便在一个地方统一管理要用到的网址。
    new_url = "https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&since_id={since_id}"
    status_url = "https://m.weibo.cn/statuses/extend?id={id}"

    dupefilter_key = f"{name}:dupefilter"  # 已爬页面库
    queue_key = f'{name}:requests'  # 请求队列库
    since_key = f'{name}:since_id'  # since_id队列
    item_key = f'{name}:itemcount'
    scroll_key = f'{name}:scrollcount'


    # 项目初始化函数
    def __init__(self, *args, **kwargs):
        super(WeiboSearchSpider, self).__init__(*args, **kwargs)

         # 初始化各微博用户（user_id）抓取item数量计数器
        self.user_item_count = {}

        # 获取redis连接，调用了redis连接函数connect_to_redis()
        self.redis_conn = self.connect_to_redis()

        # 最setting中设置的headers和cookies
        self.headers = settings.headers
        self.cookies = settings.cookies

    # redis连接函数
    def connect_to_redis(self):
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        db = settings.REDIS_DB
        while True:
            try:
                redis_conn = redis.StrictRedis(host=host, port=port, db=db, socket_timeout=10)
                redis_conn.ping()
                return redis_conn
            except (ConnectionError, TimeoutError):
                custom_logger.info("连接到 Redis 服务器失败，正在重试...")
                time.sleep(5)

    # 确保redis正常连接的函数
    def ensure_redis_connection(self):
        try:
            self.redis_conn.ping()
        except (ConnectionError, TimeoutError):
            custom_logger.info("爬取时 Redis 连接丢失，正在重新连接...")
            self.redis_conn = self.connect_to_redis()

    # 重写make_requests_from_url方法，加入自定义的headers和cookies
    def make_requests_from_url(self, url):
        return scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)  # 每次重新启动的时候，滚动次数在这里就重置为0了。meta={'scroll_count': 0}

     # 全部发表微博的滚动提取
    def parse(self, response):

        # # 用于检查是否连接成功，测试用，如果cookies过期，则这里会显示出来
        # custom_logger.info(f"响应网址: {response.url}")
        # custom_logger.info(f"响应状态码: {response.status}")
        # custom_logger.info(f"响应的内容：{response.text}")

        response_data = response.json()

        pattern = r"containerid=230413(\d+)_-_WEIBO_SECOND_PROFILE_WEIBO"
        match = re.search(pattern, response.url)
        user_id = match.group(1)

        # 在每次操作 Redis 前确保连接有效，涉及两个操作，获取scroll_count和item_count
        self.ensure_redis_connection()
        # 1.检查redis里存储的的滚动次数
        if not self.redis_conn.exists(self.scroll_key):
            self.redis_conn.hset(self.scroll_key, user_id, 0)
            scroll_count = 0
        else:
            scroll_count = int(self.redis_conn.hget(self.scroll_key, user_id) or 0)

        # 2.检查redis里存储的item抓取个数
        if not self.redis_conn.exists(self.item_key):
            self.redis_conn.hset(self.item_key, user_id, 0)
            item_count = 0
        else:
            item_count = int(self.redis_conn.hget(self.item_key, user_id) or 0)

        if response_data.get('ok') == 1:
            since_id = response_data.get('data', {}).get('cardlistInfo', {}).get('since_id', "无")  # 获取下一页的since_id。

            item = WeiboScrapyItem()  # 直接引入item.py中的，比自己定义item={}更安全更稳健，注意要from weibo_scrapy.items import WeiboScrapyItem。

            cards = response_data.get('data', {}).get('cards', [])  # 此时，cards是一个列表。
            count = 0  # 初始化每页面爬取微博数的计数器，符合要求即加1，否则不加。
            item['since_id'] = since_id
            item['user_id'] = user_id
            for card in cards:

                if card.get('card_type') == 11 and card.get('show_type') == 3:  # 置顶微博模块，不是每个用户都有置顶微博，要注意。
                    for micro_card in card['card_group']:

                        # 解析微博发布时间
                        created_at_str = micro_card['mblog']['created_at']
                        try:
                            created_at = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
                        except ValueError:
                            continue  # 如果解析失败，跳过该微博

                        # 检查发布时间是否在指定范围内
                        if start_date <= created_at <= end_date:
                            item = self.crawl_parse(micro_card, item, created_at_str)  #引入crawl_parse函数，更新item。

                            # 如果微博太长未显示完整，则进入全文页爬取全文。请注意，这里爬取被转发微博的全文，因为用途不大。
                            if f'''<a href="/status/{item['id']}">全文</a>''' in item['text']:
                                self.ensure_redis_connection()  # 在每次操作 Redis 前确保连接有效，以避免redis连接错误，通过错误检查，发现多在此步骤失去redis连接，故先检查
                                yield scrapy.Request(self.status_url.format(id=item['id']),
                                                     callback=self.parse_status,
                                                     meta={'item': item,
                                                           'cookiejar': response.meta.get('cookiejar'),
                                                           'headers': response.meta.get('headers')})
                            else:
                                yield item

                            count += 1  # 只有符合条件时才更新计数器，证明此微博已收集到item
                            item_count += 1 # 收集到的item数量+1

                        else:
                            item['user_id'] = micro_card['mblog']['user'].get('id')
                            item['user_name'] = micro_card['mblog']['user'].get('screen_name')  #这里取出的是元组，故显示有问题
                            item['user_statuses_count'] = micro_card['mblog']['user'].get('statuses_count')

                elif card.get('card_type') == 9:  # 非置顶微博模块

                    # 解析微博发布时间
                    created_at_str = card['mblog']['created_at']
                    try:
                        created_at = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
                    except ValueError:
                        continue  # 如果解析失败，跳过该微博

                    # 检查发布时间是否在指定范围内
                    if start_date <= created_at <= end_date:

                        item = self.crawl_parse(card, item, created_at_str)  # 引入crawl_parse函数，更新item。
                        count += 1  # 只有符合条件时才更新计数器

                        if f'''<a href="/status/{item['id']}">全文</a>''' in item['text']:
                            self.ensure_redis_connection()  # 在每次操作 Redis 前确保连接有效，以避免redis连接错误，通过错误检查，发现多在此步骤失去redis连接，故先检查
                            yield scrapy.Request(self.status_url.format(id=item['id']),
                                                 callback=self.parse_status,
                                                 meta={'item': item,
                                                       'cookiejar': response.meta.get('cookiejar'),
                                                       'headers': response.meta.get('headers')})
                        else:
                            yield item

                        item_count += 1

                    else:
                        item['user_id'] = card['mblog']['user'].get('id')
                        item['user_name'] = card['mblog']['user'].get('screen_name') #这里取出的是元组，故显示有问题
                        item['user_statuses_count'] = card['mblog']['user'].get('statuses_count', 0)

                        # 修改item['user_name']和item['user_statuses_count']的格式
                        item['user_name'] = item['user_name'] if isinstance(
                            item['user_name'], str) else str(item['user_name'][0])
                        item['user_statuses_count'] = item['user_statuses_count'] if isinstance(
                            item['user_statuses_count'], int) else int(
                            item['user_statuses_count'][0])  # 确保 user_statuses_count 是整数

            # 增加下滚次数，增加判断是到最后一页了就找不到statuses_count了。
            if item.get('user_statuses_count') and item['user_statuses_count'] != 0:
                n = item['user_statuses_count'] // 10 - scroll_count
                custom_logger.info(f"{item['user_name']}({user_id}) 共发表{item['user_statuses_count']}条微博，已下滚{scroll_count}页。本页抓取{count}个符合要求的item，总共已抓取{item_count}个。还可滚动{n}次，下一页id为{since_id}。")

            # 在每次操作 Redis 前确保连接有效，以使存储数据更准确，接下来有三个数据需存储，分别为item_count、scroll_count、since_id。
            self.ensure_redis_connection()  # 在每次操作 Redis 前确保连接有效，以使存储数据更准确

            # 1.将这次总共爬取的 item 个数存入redis。
            self.redis_conn.hset(self.item_key, user_id, str(item_count))  #存储item_count

            # 检查 since_id 是否为默认值
            if since_id == "无":   # 在这里处理未获取到 since_id 的情况，即基本到最后一页了。
                user_url = f"https://weibo.com/u/{user_id}"
                custom_logger.info(f"用户 {user_id}) 未获取到下一页的since_id，此用户可能爬取结束，或请求了错误页面，请检查一下。总共已滚动{scroll_count}次，共抓取{item_count}个item。检查网址为 {user_url} 。")
            else:
                # 2.滚动次数+1，并将变动后的 scroll_count 存入Redis
                scroll_count += 1
                self.redis_conn.hset(self.scroll_key, user_id, str(scroll_count))  # 存储scroll_count
                # 3.将 since_id 存入redis
                since_id_key = 'weibo_search:since_id'
                self.redis_conn.hset(since_id_key, f"{user_id}:{item['user_name']}", since_id)  # 存储since_id

                yield scrapy.Request(self.new_url.format(user_id=user_id, since_id=since_id), callback=self.parse, headers=self.headers, cookies=self.cookies,
                                     meta={'scroll_count': scroll_count, 'user_id': user_id,})

    # 微博内容提取函数
    def crawl_parse(self, card, item, created_at_str):
        item.update({
            'crawl_time': datetime.now(),
            'created_at': created_at_str,
            'id': card['mblog'].get('id'),
            'text': card['mblog'].get('text'),
            'source': card['mblog'].get('source', ''),
            'reposts_count': card['mblog'].get('reposts_count', 0),
            'comments_count': card['mblog'].get('comments_count', 0),
            'reprint_cmt_count': card['mblog'].get('reprint_cmt_count', 0),
            'attitudes_count': card['mblog'].get('attitudes_count', 0),
            'user_name': card['mblog']['user'].get('screen_name'),
            'user_description': card['mblog']['user'].get('description', ''),
            'user_follow_count': card['mblog']['user'].get('follow_count', 0),
            'user_followers_count': card['mblog']['user'].get('followers_count', 0),
            'user_statuses_count': card['mblog']['user'].get('statuses_count', 0),
            'user_verified': card['mblog']['user'].get('verified', False),
            'user_verified_reason': card.get('user', {}).get(
                'verified_reason', ''),
        })

        retweeted_status = card['mblog'].get('retweeted_status', {})  # 获取 retweeted_status，如果不存在则使用空字典
        # 确保retweeted_status存在时才去获取值，否则直接设为默认值
        if retweeted_status:
            user_info = retweeted_status.get('user') or {}  # 获取 user 信息，如果 user 不存在或为 None，则使用空字典
            item.update({
                'retweet': 1,
                'retweet_text': retweeted_status.get('text', ''),
                'retweet_created_at': retweeted_status.get('created_at', ''),
                'retweet_id': retweeted_status.get('id', ''),
                'retweet_source': retweeted_status.get('source', ''),
                'retweet_reposts_count': retweeted_status.get('reposts_count', 0),
                'retweet_comments_count': retweeted_status.get('comments_count', 0),
                'retweet_reprint_cmt_count': retweeted_status.get('reprint_cmt_count', 0),
                'retweet_attitudes_count': retweeted_status.get('attitudes_count', 0),
                'retweet_user_name': user_info.get('user', {}).get('screen_name', ''),
                'retweet_user_id': user_info.get('user', {}).get('id', ''),
                'retweet_user_description': user_info.get('user', {}).get('description', ''),
                'retweet_user_follow_count': user_info.get('user', {}).get('follow_count', 0),
                'retweet_user_followers_count': user_info.get('user', {}).get('followers_count', 0),
                'retweet_user_statuses_count': user_info.get('user', {}).get('statuses_count', 0),
                'retweet_user_verified': user_info.get('user', {}).get('verified', False),
                'retweet_user_verified_reason': user_info.get('user', {}).get('verified_reason', ''),
            })
        else:
            item.update({
                'retweet': 0,
                'retweet_text': '',
                'retweet_created_at': '',
                'retweet_id': '',
                'retweet_source': '',
                'retweet_reposts_count': 0,
                'retweet_comments_count': 0,
                'retweet_reprint_cmt_count': 0,
                'retweet_attitudes_count': 0,
                'retweet_user_name': '',
                'retweet_user_id': '',
                'retweet_user_description': '',
                'retweet_user_follow_count': 0,
                'retweet_user_followers_count': 0,
                'retweet_user_statuses_count': 0,
                'retweet_user_verified': False,
                'retweet_user_verified_reason': '',
            })

        return item

    # 爬取长微博的全文
    def parse_status(self, response):
        response_data = response.json()
        item = response.meta['item']

        if response_data.get('ok') == 1:
            item['text'] = response_data.get('data',{}).get('longTextContent',{})
        yield item
