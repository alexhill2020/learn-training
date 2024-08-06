import scrapy
from scrapy_redis.spiders import RedisSpider
import logging
from datetime import datetime, timezone
from weibo_scrapy.items import WeiboScrapyItem

# 事实证明在断点续爬的时候只要redis的weibo_search:request里有网址，则会继续爬，没有网址，或者是只有爬完就结束的网址，则不会继续爬。
# 因此实现断点续爬的关键点就是如何确保其request里一直有网址。
# 研究了一晚上，断点续爬没有更好的方式了，主要是不能确保weibo_search:request里一定会有可以延伸的网址，目前只能是这个样子了。
# 所以最好的方式还是不要让其断掉，这只是救急之策。
# 经验证，必须三个dont_filter=True都必须有。但是三个都有的话，每重新启动一次，就要重新发一次，要从0开始，如果重新启动2次，就要从0开始2次，这怎么办？

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
    allowed_domains = ['m.weibo.cn']

    # Redis key to use for starting URLs
    redis_key = 'weibo_search:start_urls'

    # 以下为全局抓取中要用到的url，这里先定义了，主要是为了redis，不然不会被注入redis中。
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO'
    new_url = "https://m.weibo.cn/api/container/getIndex?containerid=230413{user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&since_id={since_id}"
    status_url = "https://m.weibo.cn/statuses/extend?id={id}"
    user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={user_id}&containerid=100505{user_id}'

    def __init__(self, *args, **kwargs):
        super(WeiboSearchSpider, self).__init__(*args, **kwargs)
        self.user_item_count = {}  # 初始化各微博用户（user_id）抓取item数量计数器

    def start_requests(self):

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

        # 从文件中读取user_id
        file = 'user_id.txt'
        with open(file, 'r') as file:
            user_ids = file.readlines()

        # 逐行读取微博用户ID
        for user_id in user_ids:
            user_id = user_id.strip()

            self.user_item_count[user_id] = 0   #先在user_item_count字典中存入user_id键（赋值为0），否则后面在这个字典找不到以user_id为键名的键会同问题。

            # 先爬取用户信息页，提取用户名字和发表微博数量等信息，以在爬取具体微博时使用（主要是避免一页中没有任务符合要求的微博，否则可以不用先爬这个页面而直接到微博中去取用户信息）。
            yield scrapy.Request(url = self.user_url.format(user_id=user_id), headers=headers, cookies=cookies, callback=self.parse, meta={'user_id': user_id, 'cookiejar':1, 'headers':headers})

    #用户信息页提取
    def parse(self, response):
        response_data = response.json()
        user_id = response.meta['user_id']  # 继承user_id
        user_name = response_data.get('data',{}).get('userInfo',{}).get('screen_name',None) # 获取用户名
        statuses_count = response_data.get('data', {}).get('userInfo', {}).get('statuses_count',None) #获取发微博数量

        yield scrapy.Request(url=self.url.format(user_id=user_id), callback=self.weibo_parse,
                             meta={'user_id': user_id, 'user_name': user_name,'statuses_count': statuses_count, 'cookiejar': response.meta.get('cookiejar'),
                                                               'headers': response.meta.get('headers'),'scroll_count': 0})  # 'scroll_count': 0为设置滚动次数为0
    # 全部发表微博的滚动提取
    def weibo_parse(self, response):

        response_data = response.json()
        user_id = response.meta['user_id']
        user_name = response.meta['user_name']
        statuses_count = response.meta['statuses_count']
        scroll_count = response.meta['scroll_count']  # 获取下滚次数

        if response_data.get('ok') == 1:
            since_id = response_data.get('data', {}).get('cardlistInfo', {}).get('since_id', None)  # 获取下一页的since_id。

            cards = response_data.get('data', {}).get('cards', [])  # 此时，cards是一个列表。

            count = 0  # 初始化每页面爬取微博数的计数器，符合要求即加1，否则不加。
            for card in cards:

                item = WeiboScrapyItem()  # 直接引入item.py中的，比自己定义item={}更安全更稳健，注意要from weibo_scrapy.items import WeiboScrapyItem。

                item['since_id'] = since_id
                item['user_id'] = user_id
                if card.get('card_type') == 11:  # 置顶微博模块，不是每个用户都有置顶微博，要注意。
                    if card.get('show_type') == 3:
                        for micro_card in card['card_group']:

                            # 解析微博发布时间
                            created_at_str = micro_card['mblog']['created_at']
                            try:
                                created_at = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
                            except ValueError:
                                continue  # 如果解析失败，跳过该微博

                            # 检查发布时间是否在指定范围内
                            if start_date <= created_at <= end_date:

                                item['crawl_time'] = time
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
                                item['user_verified_reason'] = micro_card['mblog']['user']['verified_reason']  # 是否认证

                                # 上面的为原创微博，这里是判断是否为转发，如是转发微博则同时提取被转发微博的信息
                                retweeted_status_microcard = micro_card['mblog'].get('retweeted_status')
                                if retweeted_status_microcard:
                                    item['retweet'] = 1  #如果为转发，则转发为1
                                    item['retweet_text'] = micro_card['mblog']['retweeted_status']['text']
                                    item['retweet_created_at'] = micro_card['mblog']['retweeted_status']['created_at']
                                    item['retweet_id'] = micro_card['mblog']['retweeted_status']['id']
                                    item['retweet_source'] = micro_card['mblog']['retweeted_status'].get('source', '')
                                    item['retweet_reposts_count'] = micro_card['mblog']['retweeted_status']['reposts_count']
                                    item['retweet_comments_count'] = micro_card['mblog']['retweeted_status']['comments_count']
                                    item['retweet_reprint_cmt_count'] = micro_card['mblog']['retweeted_status']['reprint_cmt_count']
                                    item['retweet_attitudes_count'] = micro_card['mblog']['retweeted_status']['attitudes_count']
                                    item['retweet_user_name'] = micro_card['mblog']['retweeted_status']['user'][
                                        'screen_name']  # 用户名
                                    item['retweet_user_id'] = micro_card['mblog']['retweeted_status']['user'][
                                        'id']  # 用户描述
                                    item['retweet_user_description'] = micro_card['mblog']['retweeted_status']['user'][
                                        'description']  # 用户描述
                                    item['retweet_user_follow_count'] = micro_card['mblog']['retweeted_status']['user'][
                                        'follow_count']  # 关注者
                                    item['retweet_user_followers_count'] = micro_card['mblog']['retweeted_status']['user'][
                                        'followers_count']  # 粉丝数
                                    item['retweet_user_statuses_count'] = micro_card['mblog']['retweeted_status']['user'][
                                        'statuses_count']  # 所发微博数
                                    item['retweet_user_verified'] = micro_card['mblog']['retweeted_status']['user'][
                                        'verified']  # 是否认证
                                    item['retweet_user_verified_reason'] = micro_card['mblog']['retweeted_status']['user'][
                                        'verified_reason']  # 是否认证

                                else:   # 如果有转发即为已有的值，否则设默认值，主要是为了数据格式统一
                                    item['retweet'] = 0
                                    item['retweet_text'] = ''
                                    item['retweet_created_at'] = ''
                                    item['retweet_id'] = ''
                                    item['retweet_source'] = ''
                                    item['retweet_reposts_count'] = 0
                                    item['retweet_comments_count'] = 0
                                    item['retweet_reprint_cmt_count'] = 0
                                    item['retweet_attitudes_count'] = 0
                                    item['retweet_user_name'] = ''
                                    item['retweet_user_id'] = ''
                                    item['retweet_user_description'] = ''
                                    item['retweet_user_follow_count'] = 0
                                    item['retweet_user_followers_count'] = 0
                                    item['retweet_user_statuses_count'] = 0
                                    item['retweet_user_verified'] = False
                                    item['retweet_user_verified_reason'] = ''

                                count += 1  # 只有符合条件时才更新计数器，证明此微博已收集到item

                                # 更新每个用户总计抓取的item的计数器
                                if user_id in self.user_item_count:
                                    self.user_item_count[user_id] += 1
                                else:
                                    self.user_item_count[user_id] = 1

                                # 检查 'text' 中是否包含特定子字符串，即是否还未显示完全文。
                                if f'''<a href="/status/{item['id']}">全文</a>''' in item['text']:
                                    yield scrapy.Request(self.status_url.format(id=item['id']),
                                                         callback=self.parse_status,
                                                         meta={'item': item, 'cookiejar': response.meta.get('cookiejar'),
                                                               'headers': response.meta.get('headers')})
                                else:
                                    yield item
                elif card.get('card_type') == 9:  # 非置顶微博模块

                    # 解析微博发布时间
                    created_at_str = card['mblog']['created_at']
                    #print(f"第{scroll_count}次滚动的since_id为{since_id}，user_id为{user_id}，微博发布时间为{created_at_str}。")
                    try:
                        created_at = datetime.strptime(created_at_str, '%a %b %d %H:%M:%S %z %Y')
                    except ValueError:
                        #print('那就跳过了')
                        continue  # 如果解析失败，跳过该微博

                    # 检查发布时间是否在指定范围内
                    if start_date <= created_at <= end_date:
                        count += 1  # 只有符合条件时才更新计数器

                        item['crawl_time'] = time
                        item['created_at'] = card['mblog']['created_at']
                        item['id'] = card['mblog']['id']
                        item['text'] = card['mblog']['text']
                        item['source'] = card['mblog'].get('source', '')
                        item['reposts_count'] = card['mblog']['reposts_count']
                        item['comments_count'] = card['mblog']['comments_count']
                        item['reprint_cmt_count'] = card['mblog']['reprint_cmt_count']
                        item['attitudes_count'] = card['mblog']['attitudes_count']
                        item['user_name'] = card['mblog']['user']['screen_name']  # 用户名
                        item['user_description'] = card['mblog']['user']['description']  # 用户描述
                        item['user_follow_count'] = card['mblog']['user']['follow_count']  # 关注者
                        item['user_followers_count'] = card['mblog']['user']['followers_count']  # 粉丝数
                        item['user_statuses_count'] = card['mblog']['user']['statuses_count']  # 所发微博总数
                        item['user_verified'] = card['mblog']['user']['verified']  # 是否认证

                        retweeted_status = card['mblog'].get('retweeted_status')
                        if retweeted_status:
                            item['retweet'] = 1  # 如果为转发，则转发为1
                            item['retweet_text'] = card['mblog']['retweeted_status']['text']
                            item['retweet_created_at'] = card['mblog']['retweeted_status']['created_at']
                            item['retweet_id'] = card['mblog']['retweeted_status']['id']
                            item['retweet_source'] = card['mblog']['retweeted_status'].get('source', '')
                            item['retweet_reposts_count'] = card['mblog']['retweeted_status']['reposts_count']
                            item['retweet_comments_count'] = card['mblog']['retweeted_status']['comments_count']
                            item['retweet_reprint_cmt_count'] = card['mblog']['retweeted_status']['reprint_cmt_count']
                            item['retweet_attitudes_count'] = card['mblog']['retweeted_status']['attitudes_count']
                            item['retweet_user_name'] = card['mblog']['retweeted_status']['user'][
                                'screen_name']  # 用户名
                            item['retweet_user_id'] = card['mblog']['retweeted_status']['user'][
                                'id']  # 用户描述
                            item['retweet_user_description'] = card['mblog']['retweeted_status']['user'][
                                'description']  # 用户描述
                            item['retweet_user_follow_count'] = card['mblog']['retweeted_status']['user'][
                                'follow_count']  # 关注者
                            item['retweet_user_followers_count'] = card['mblog']['retweeted_status']['user'][
                                'followers_count']  # 粉丝数
                            item['retweet_user_statuses_count'] = card['mblog']['retweeted_status']['user'][
                                'statuses_count']  # 所发微博数
                            item['retweet_user_verified'] = card['mblog']['retweeted_status']['user'][
                                'verified']  # 是否认证
                            item['retweet_user_verified_reason'] = card['mblog']['retweeted_status']['user'][
                                'verified_reason']  # 是否认证

                        else:
                            item['retweet'] = 0
                            item['retweet_text'] = ''
                            item['retweet_created_at'] = ''  # 原始微博的创建时间
                            item['retweet_id'] = ''
                            item['retweet_source'] = ''
                            item['retweet_reposts_count'] = 0
                            item['retweet_comments_count'] = 0
                            item['retweet_reprint_cmt_count'] = 0
                            item['retweet_attitudes_count'] = 0
                            item['retweet_user_name'] = ''
                            item['retweet_user_id'] = ''
                            item['retweet_user_description'] = ''
                            item['retweet_user_follow_count'] = 0
                            item['retweet_user_followers_count'] = 0
                            item['retweet_user_statuses_count'] = 0
                            item['retweet_user_verified'] = False
                            item['retweet_user_verified_reason'] = ''

                        # 更新用户抓取计数器
                        if user_id in self.user_item_count:
                            self.user_item_count[user_id] += 1
                        else:
                            self.user_item_count[user_id] = 1

                        # 检查 'text' 中是否包含特定子字符串，即是否还未显示完全文。
                        if f'''<a href="/status/{item['id']}">全文</a>''' in item['text']:
                            yield scrapy.Request(self.status_url.format(id=item['id']),
                                                 callback=self.parse_status,
                                                 meta={'item': item, 'cookiejar': response.meta.get('cookiejar'),
                                                       'headers': response.meta.get('headers')})
                        else:
                            yield item

            # 增加下滚次数
            n = statuses_count // 10 - scroll_count
            custom_logger.info(f"{user_name}({user_id}) 共发表{statuses_count}条微博，本页抓取{count}个符合要求的item。已下滚{scroll_count}页，总共已抓取{self.user_item_count[user_id]}个。还可滚动{n}次，下一页id为{since_id}。")

            scroll_count += 1
            if since_id:
                yield scrapy.Request(self.new_url.format(user_id=user_id, since_id=since_id), callback=self.weibo_parse,
                                     meta={'cookiejar': response.meta['cookiejar'],
                                           'headers': response.meta['headers'], 'scroll_count': scroll_count, 'user_id': user_id, 'user_name':user_name, 'statuses_count': statuses_count})

    # 显示全文
    def parse_status(self, response):
        response_data = response.json()
        item = response.meta['item']

        if response_data.get('ok') == 1:
            item['text'] = response_data.get('data',{}).get('longTextContent',{})
        yield item

