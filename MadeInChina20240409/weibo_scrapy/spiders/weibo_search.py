import scrapy
import re
import logging
from datetime import datetime, timezone
from weibo_scrapy.items import WeiboScrapyItem
from scrapy_redis.spiders import RedisSpider

# 事实证明在断点续爬的时候只要redis的weibo_search:request里有网址，则会继续爬，没有网址，或者是只有爬完就结束的网址，则不会继续爬。
# 因此实现断点续爬的关键点就是如何确保其request里一直有网址，没有网址的原因是URL处理速度快于URL的生成速度，导致Redis队列中的URL被迅速处理完，从而无法维持持续的抓取。
# 研究了一晚上，断点续爬没有更好的方式了，主要是不能确保weibo_search:request里一定会有可以延伸的网址，目前只能是这个样子了。
# 要解决此问题主要有两种方式：确保有足够的初始URL、并发请求数减少（settings.py中设置），本来想动态生态url再手工推送到requests列，但细想+试验证明并不行，因此本来产生的url就全部都要推送过去，手工推送只是白用工。

# 获取自定义日志记录器
custom_logger = logging.getLogger('custom_logger')  #已在setting.py中设置好

# 获取当前日期和时间
time = datetime.now()

# 打印当前日期和时间
custom_logger.info(f"----------开始爬虫，当前时间是：{time}----------")

# 定义爬取微博的时间范围
start_date = datetime(2017, 10, 18, tzinfo=timezone.utc)  #后面是添加时区信息
end_date = datetime(2024, 7, 31, tzinfo=timezone.utc)


class WeiboSearchSpider(RedisSpider):
    name = 'weibo_search'
    # allowed_domains = ['m.weibo.cn']  # 利用redis进行分布式爬虫需注销掉这个
    redis_key = 'weibo_search:start_urls' # 用Redis进行分布式爬虫时用于存储初始URL的 Redis key

    # 以下为全局抓取中要用到的url，这里先定义了，方便在一个地方统一管理要用到的网址。
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO'
    new_url = "https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&since_id={since_id}"
    status_url = "https://m.weibo.cn/statuses/extend?id={id}"
    user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}&containerid=100505{user_id}'

    def __init__(self, *args, **kwargs):
        super(WeiboSearchSpider, self).__init__(*args, **kwargs)

        # 初始化各微博用户（user_id）抓取item数量计数器
        self.user_item_count = {}

        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://m.weibo.cn/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'x-xsrf-token':'9d791e',   #观察要爬取的网址“https://m.weibo.cn/profile/info?uid=2050142347”的请求头，发现多了这个参数。那这个参数的值是从哪里来的呢？还要研究一下
           }

        # cookies时不时会变，上面的x-xsrf-token时不时也会变，一定要注意观察待爬取网址的请求头，做相应的修改。
        temp = '_T_WM=2a49f655949fe128a72e77d0c7660284; ALF=1725462747; SCF=An88pjtFAEn9F8u7w53WMXvci1cCd8e6v5TeBL0pj8SdyGg3hz-97aumDxPtglPhGyHMKt_cfdEM9Q0r-lqjM4w.; SUB=_2A25LtJuLDeRhGeNP6VMU8SjEwjSIHXVoy5FDrDV6PUJbktAGLWvHkW1NTr09mF_33IpP3AoNkWC1oBIu1-AOnT3U; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhKlxWT8Vs0ffppg0hdSMBY5JpX5K-hUgL.Fo-peo2feKqR1Kn2dJLoI79jINS.qJMt; WEIBOCN_FROM=1110006030; XSRF-TOKEN=9d791e; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583%26fid%3D1005052050142347%26uicode%3D10000011; mweibo_short_token=93dc2207e0'
        self.cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

    # 重写make_requests_from_url方法，加入自定义的headers和cookies
    def make_requests_from_url(self, url):
        return scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    #用户信息页提取
    def parse(self, response):

        # 用于检查是否连接成功，测试用，如果cookies过期，则这里会显示出来
        # custom_logger.info(f"响应网址: {response.url}")
        # custom_logger.info(f"响应状态码: {response.status}")
        # custom_logger.info(f"响应的内容：{response.text}")

        response_data = response.json()
        user_name = response_data.get('data', {}).get('userInfo', {}).get('screen_name', None)  # 获取用户名
        statuses_count = response_data.get('data', {}).get('userInfo', {}).get('statuses_count', None)  # 获取发微博数量
        if "type=uid&value=" in response.url and "containerid=100505" in response.url:
            pattern = r"value=(\d+)&containerid"
            match = re.search(pattern, response.url)
            user_id = match.group(1)
            self.user_item_count[user_id] = 0
            yield scrapy.Request(url=self.url.format(user_id=user_id), callback=self.weibo_parse,
                                 meta={'user_id': user_id, 'user_name': user_name, 'statuses_count': statuses_count,
                                       'cookiejar': response.meta.get('cookiejar'),
                                       'headers': response.meta.get('headers'),
                                       'scroll_count': 0})  # 'scroll_count': 0为设置滚动次数为0

    # 全部发表微博的滚动提取
    def weibo_parse(self, response):

        response_data = response.json()
        user_id = response.meta['user_id']
        user_name = response.meta['user_name']
        statuses_count = response.meta['statuses_count']
        scroll_count = response.meta['scroll_count']  # 获取下滚次数

        if response_data.get('ok') == 1:
            since_id = response_data.get('data', {}).get('cardlistInfo', {}).get('since_id', "未获取到下一页的since_id")  # 获取下一页的since_id。

            cards = response_data.get('data', {}).get('cards', [])  # 此时，cards是一个列表。

            count = 0  # 初始化每页面爬取微博数的计数器，符合要求即加1，否则不加。
            for card in cards:

                item = WeiboScrapyItem()  # 直接引入item.py中的，比自己定义item={}更安全更稳健，注意要from weibo_scrapy.items import WeiboScrapyItem。

                item['since_id'] = since_id
                item['user_id'] = user_id
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
                                yield scrapy.Request(self.status_url.format(id=item['id']),
                                                     callback=self.parse_status,
                                                     meta={'item': item,
                                                           'cookiejar': response.meta.get('cookiejar'),
                                                           'headers': response.meta.get('headers')})
                            else:
                                yield item

                            count += 1  # 只有符合条件时才更新计数器，证明此微博已收集到item

                            # 更新每个用户总计抓取的item的计数器
                            if user_id in self.user_item_count:
                                self.user_item_count[user_id] += 1
                            else:
                                self.user_item_count[user_id] = 1

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
                            yield scrapy.Request(self.status_url.format(id=item['id']),
                                                 callback=self.parse_status,
                                                 meta={'item': item,
                                                       'cookiejar': response.meta.get('cookiejar'),
                                                       'headers': response.meta.get('headers')})
                        else:
                            yield item

                        # 更新用户抓取计数器
                        if user_id in self.user_item_count:
                            self.user_item_count[user_id] += 1
                        else:
                            self.user_item_count[user_id] = 1


            # 增加下滚次数
            n = statuses_count // 10 - scroll_count
            custom_logger.info(f"{user_name}({user_id}) 共发表{statuses_count}条微博，已下滚{scroll_count}页。本页抓取{count}个符合要求的item，总共已抓取{self.user_item_count[user_id]}个。还可滚动{n}次，下一页id为{since_id}。")

            scroll_count += 1
            if since_id:
                yield scrapy.Request(self.new_url.format(user_id=user_id, since_id=since_id), callback=self.weibo_parse,
                                     meta={'cookiejar': response.meta['cookiejar'],
                                           'headers': response.meta['headers'], 'scroll_count': scroll_count, 'user_id': user_id, 'user_name':user_name, 'statuses_count': statuses_count})

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

        retweeted_status = card['mblog'].get('retweeted_status', {})
        # 确保retweeted_status存在时才去获取值，否则直接设为默认值
        if retweeted_status:
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
                'retweet_user_name': retweeted_status.get('user', {}).get('screen_name', ''),
                'retweet_user_id': retweeted_status.get('user', {}).get('id', ''),
                'retweet_user_description': retweeted_status.get('user', {}).get('description', ''),
                'retweet_user_follow_count': retweeted_status.get('user', {}).get('follow_count', 0),
                'retweet_user_followers_count': retweeted_status.get('user', {}).get('followers_count', 0),
                'retweet_user_statuses_count': retweeted_status.get('user', {}).get('statuses_count', 0),
                'retweet_user_verified': retweeted_status.get('user', {}).get('verified', False),
                'retweet_user_verified_reason': retweeted_status.get('user', {}).get('verified_reason', ''),
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

