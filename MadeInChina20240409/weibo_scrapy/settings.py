# Scrapy settings for weibo_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# import datetime

BOT_NAME = 'weibo_scrapy'

SPIDER_MODULES = ['weibo_scrapy.spiders']
NEWSPIDER_MODULE = 'weibo_scrapy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibo_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32 #允许发起的最大并发数量，默认为16，如果启用蜻蜓ip隧道代理，则设置为5，因为隧道代理最大并发数为5

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2 #一般设置为3，如果反爬较严格可设置下载延迟为5秒
RANDOMIZE_DOWNLOAD_DELAY=True #随机下载延迟，避免反爬
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    'Accept': 'application/json, text/plain, */*',
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
#    'Referer': 'https://m.weibo.cn/',
#    'Accept-Language': 'zh-CN,zh;q=0.9',
# }

# --------自定义请求头headers和cookies，以在爬虫文件和其它地方使用--------
headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://m.weibo.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'x-xsrf-token': '9d791e',
        # 观察要爬取的网址“https://m.weibo.cn/profile/info?uid=2050142347”的请求头，发现多了这个参数。那这个参数的值是从哪里来的呢？还要研究一下
}
# cookies时不时会变，上面的x-xsrf-token时不时也会变，一定要注意观察待爬取网址的请求头，做相应的修改。
temp = '_T_WM=2a49f655949fe128a72e77d0c7660284; ALF=1725462747; SCF=An88pjtFAEn9F8u7w53WMXvci1cCd8e6v5TeBL0pj8SdyGg3hz-97aumDxPtglPhGyHMKt_cfdEM9Q0r-lqjM4w.; SUB=_2A25LtJuLDeRhGeNP6VMU8SjEwjSIHXVoy5FDrDV6PUJbktAGLWvHkW1NTr09mF_33IpP3AoNkWC1oBIu1-AOnT3U; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhKlxWT8Vs0ffppg0hdSMBY5JpX5K-hUgL.Fo-peo2feKqR1Kn2dJLoI79jINS.qJMt; WEIBOCN_FROM=1110006030; XSRF-TOKEN=9d791e; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231583%26fid%3D1005052050142347%26uicode%3D10000011; mweibo_short_token=93dc2207e0'
cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。


# HTTPERROR_ALLOWED_CODES = [403]

# --------连接MongoDB数据库的配置--------
MONGODB_SERVER = '139.186.165.94'  #MongoDB数据库所在云服务器IP。
MONGODB_PORT = 27017  #默认端口。
MONGODB_USER = 'admin'  # 用户名
MONGODB_PWD = 'admin123'  # 密码
MONGODB_AUDB = 'admin'  # 用于认证的数据库名称
MONGODB_DBNAME = 'weibo_search_20240805'  # 数据库名
MONGODB_SHEETNAME = 'weibo_search_main_20240805'  # 表名


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'weibo_scrapy.middlewares.WeiboScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'weibo_scrapy.middlewares.WeiboScrapyDownloaderMiddleware': 543,
    'weibo_scrapy.middlewares.RandomUserAgent': 300, # 启用随机请求头中间件
    #'weibo_scrapy.middlewares.ProxyDownloaderMiddleware': 350,  # 启用ip代理中间件，代理设置在middlewares.py里设置
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'weibo_scrapy.pipelines.WeiboScrapyPipeline': 300,
     'weibo_scrapy.pipelines.WeiboScrapyMongoPipeline': 300,  # 存储的Mongo管道
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# --------Scrapy会在遇到这些状态码时自动重试请求，并按以下要求增加重试次数和等待时间---------
RETRY_HTTP_CODES = [401, 403, 408, 414, 429, 500, 502, 503, 504, 522, 524]  # 当 Scrapy 收到这些状态码时，将认为请求失败，并触发重试机制
RETRY_TIMES = 5  # 最大重试次数（次），默认为2次
RETRY_DELAY = 5  # 每次重试之间的延迟时间（秒），默认为0秒
DOWNLOAD_TIMEOUT = 15 # 每个下载请求的最大等待时间（秒），默认为180秒

# 401 - Unauthorized：未授权，表示请求需要身份验证。通常需要提供有效的身份验证凭证才能访问请求的资源。
# 403 - Forbidden：禁止访问，表示服务器理解请求但拒绝执行。通常是因为权限问题，客户端没有访问资源的权限。
# 408 - Request Timeout：请求超时，表示服务器在等待客户端发送的请求时超时。通常是因为网络问题或客户端响应缓慢。
# 414 - URI Too Long：URI 太长，表示请求的 URI 过长，服务器无法处理。通常是因为 GET 请求的查询字符串过长。
# 429 - Too Many Requests：请求过多，表示客户端发送了太多请求，服务器限制了请求速率。通常需要等待一段时间再重新发送请求。
# 500 - Internal Server Error：服务器内部错误，表示服务器遇到意外情况而无法完成请求。通常是服务器端的问题，需要服务器管理员检查日志。
# 502 - Bad Gateway：错误网关，表示服务器作为网关或代理时收到无效响应。通常是上游服务器的问题。
# 503 - Service Unavailable：服务不可用，表示服务器当前无法处理请求。通常是因为服务器过载或正在进行维护。
# 504 - Gateway Timeout：网关超时，表示服务器作为网关或代理时未能及时从上游服务器收到响应。通常是上游服务器的问题。
# 522 - Connection Timed Out：连接超时，表示 Cloudflare 等代理服务器未能及时从上游服务器收到响应。通常是上游服务器的问题或网络问题。
# 524 - A Timeout Occurred：超时错误，表示 Cloudflare 等代理服务器等待上游服务器响应超时。通常是上游服务器响应缓慢或无法访问。

# --------使用 scrapy-redis 进行分布式爬虫所要设置的项--------
# 使用 scrapy-redis 的调度器和去重类
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 持久化调度队列，即使关闭也不会清空
SCHEDULER_PERSIST = True

# 使用 scrapy-redis 的请求队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# 配置重爬，每次启动时都会清空redis，方便调试，调试一定要关掉，否则不能断点续爬
#SCHEDULER_FLUSH_ON_START = True

# Redis 数据库的连接配置
REDIS_HOST = '139.186.165.94'
REDIS_PORT = 10001
REDIS_PARAMS = {
    'password': '',
}
REDIS_DB = 0  # 数据库号
redis_name = 'weibo_search' # 数据库中的项目名。自己设置的变量，非官方的，故小写。

# # 可选：将抓取到的数据存储到 Redis 中
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }

# # 可选：配置 Redis 存储抓取数据的键
# REDIS_ITEMS_KEY = 'scrapy:items'

# 是否清理已完成任务
# CLOSESPIDER_TIMEOUT = 3600  # 一小时后清理


# --------自定义记录日志构造--------

import datetime
import logging
from logging.handlers import RotatingFileHandler

# 获取当前日期时间
to_day = datetime.datetime.now()
log_file_path = 'log/weibo_search_{}_{}_{}_{}{}{}.log'.format(to_day.year, to_day.month, to_day.day, to_day.hour, to_day.minute, to_day.second)

# Scrapy 的默认日志配置
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
LOG_FILE = log_file_path
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 自定义日志配置
custom_log_file = 'custom_output.log'
CUSTOM_LOG_LEVEL = 'INFO'
CUSTOM_LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
CUSTOM_LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 自定义日志处理程序
def setup_custom_logging():
        handler = RotatingFileHandler(custom_log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
        handler.setFormatter(logging.Formatter(CUSTOM_LOG_FORMAT, datefmt=CUSTOM_LOG_DATEFORMAT))

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(CUSTOM_LOG_FORMAT, datefmt=CUSTOM_LOG_DATEFORMAT))

        custom_logger = logging.getLogger('custom_logger')
        custom_logger.setLevel(CUSTOM_LOG_LEVEL)
        custom_logger.addHandler(handler)
        custom_logger.addHandler(console_handler)

setup_custom_logging()

# --------请求头列表，用于构造随机请求头，这些请求头都是在网上复制的--------
USER_AGENT_LIST =  [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
        "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
]

# settings.py


