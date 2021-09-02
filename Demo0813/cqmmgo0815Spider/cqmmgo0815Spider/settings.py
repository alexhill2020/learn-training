# Scrapy settings for cqmmgo0815Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cqmmgo0815Spider'

SPIDER_MODULES = ['cqmmgo0815Spider.spiders']
NEWSPIDER_MODULE = 'cqmmgo0815Spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73'
#这里是设置UA，反爬措施之一。

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True   #注释掉表示不遵守网站的robots协议。

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1  #下载延迟时间。
RANDOMIZE_DOWNLOAD_DELAY=True   #启用后，当从相同的网站获取数据时，Scrapy将会等待一个随机的值，延迟时间为0.5到1.5之间的一个随机值乘以DOWNLOAD_DELAY
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False  #这里注释掉，表示带cookies访问，因为基本所有网站都要登录，所以一般都注释掉。

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#   'cookies':'_DM_SID_=bad83ec19f5b52ef739f9847ff75bfcd; _Z3nY0d4C_=37XgPK9h; M_SMILEY_TIP_HIDE=1; _9755xjdesxxd_=32; __snaker__captcha=1lqyHepQARR7oXGB; gdxidpyhxdE=JoRsPg6SDKX%5CDSV67PdPhyXHKfk5%2Bw%5C6i6Y5xgm2SQoJHuumD243osDL22yCvqNu2%5CVU0NiVvd3OScM5jHQligiAB7EPOh6jz9%5CLVmAyx%2F%2FdS2iEY4%2FUYTBO1Ix79lv%2Bgrl8Z4Wx%2Ff%2FrNEO1mteE0iczASPUAvET%5CeUD87OZYyi0GB7z%3A1625140331690; cuid=rWHGkiEeqBAvC28todkfVs6M54xWGjcS; Hm_lvt_db68a43fedf04ba24c901edd34c74600=1629270021; JSESSIONID=3B7D9830CF7715FD6D0218B592F1DA8C; f9big_cq=cq173; Hm_lvt_368b91c8b5ab4c95de73b2b9b158b9af=1629463077,1629509441,1629509661,1629616177; _DM_S_=d9cae098fc1f4b211b80e2f8dbdfaa13; screen=1351; f39big=ip57; f100big_read=bq133; dayCount=%5B%5D; pm_count=%7B%7D; fr_adv=; 19lou_love_pop_daohang=19loucookie; f9bigsec=u105; fr_adv_last=merry_thread_pc; Hm_lpvt_368b91c8b5ab4c95de73b2b9b158b9af=1629629248; _dm_tagnames=%5B%7B%22k%22%3A%22%E6%83%85%E6%84%9F%E6%9D%82%E8%B0%88%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A9%9A%E6%81%8B%E6%9D%82%E8%B0%88%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E7%9B%B8%E4%BA%B2%E4%BA%A4%E5%8F%8B%E8%AE%BA%E5%9D%9B%22%2C%22c%22%3A132%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E5%90%8C%E5%9F%8E%E4%BA%A4%E5%8F%8B%22%2C%22c%22%3A132%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E5%A5%B3%E6%80%A7%E6%83%85%E6%84%9F%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E6%83%85%E6%84%9F%E8%AE%BA%E5%9D%9B%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A9%9A%E5%A7%BB%E6%81%8B%E7%88%B1%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%AE%B6%E5%BA%AD%E5%A9%86%E5%AA%B3%E5%85%B3%E7%B3%BB%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A5%B3%E7%94%9F%E5%BE%81%E5%8F%8B%22%2C%22c%22%3A37%7D%2C%7B%22k%22%3A%222021%E5%B9%B4%E5%BE%81%E5%A9%9A%E5%A4%A7%E8%B5%9B%22%2C%22c%22%3A3%7D%2C%7B%22k%22%3A%22%E5%8D%95%E8%BA%AB%E6%97%A5%E8%AE%B0%22%2C%22c%22%3A3%7D%2C%7B%22k%22%3A%2290%E5%90%8E%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A33%7D%2C%7B%22k%22%3A%22%E7%94%B7%E7%94%9F%E5%BE%81%E5%8F%8B%22%2C%22c%22%3A10%7D%2C%7B%22k%22%3A%22%E7%9B%B8%E4%BA%B2%E8%AF%9D%E9%A2%98%22%2C%22c%22%3A18%7D%2C%7B%22k%22%3A%22%E5%86%B2%E5%88%BA%E7%9A%84%E5%B0%8F%E9%BC%A0c688%22%2C%22c%22%3A3%7D%2C%7B%22k%22%3A%2280%E5%90%8E%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A7%7D%2C%7B%22k%22%3A%222021%E5%B9%B4%E7%9B%B8%E4%BA%B2%E8%AE%B0%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%9B%B8%E4%BA%B2%E6%B4%BB%E5%8A%A8%22%2C%22c%22%3A14%7D%2C%7B%22k%22%3A%22%E6%95%B4%E5%AE%B9%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%8F%8C%E7%9C%BC%E7%9A%AE%22%2C%22c%22%3A2%7D%5D; _dm_userinfo=%7B%22uid%22%3A0%2C%22stage%22%3A%22%22%2C%22city%22%3A%22%E9%87%8D%E5%BA%86%3A%E9%87%8D%E5%BA%86%22%2C%22ip%22%3A%22113.251.43.157%22%2C%22sex%22%3A%221%22%2C%22frontdomain%22%3A%22go.cqmmgo.com%22%2C%22category%22%3A%22%E6%83%85%E6%84%9F%2C%E6%97%B6%E5%B0%9A%22%7D',
#   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'cqmmgo0815Spider.middlewares.Cqmmgo0815SpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'cqmmgo0815Spider.middlewares.Cqmmgo0815SpiderDownloaderMiddleware': 543,
    'cqmmgo0815Spider.middlewares.RandomUserAgent': 543,  #随机获取请求头的中间件。
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

#DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#SCHEDULER_PERSIST = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    #'cqmmgo0815Spider.pipelines.Cqmmgo0815SpiderPipeline': 300,  #CSV存储的管道。
    'cqmmgo0815Spider.pipelines.Cqmmgo0815SpiderMongoPipeline': 300,  #MongoDb存储的管道。

#    'scrapy_redis.pipelines.RedisPipeline': 400,  #断点续爬的管道。
}

#连接MongoDB数据库的配置。
MONGODB_SERVER = "localhost"  #默认本地数据库IP。
# MONGODB_SERVER = "169.254.56.94"
MONGODB_PORT = 27017  #默认端口。
MONGODB_DBNAME = "cqmmgo-love"  #数据库名。
MONGODB_SHEETNAME = "thread-and-user"  #表名。
#MONGODB_SHEETNAME='weibo_comments'  #表2。

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

USER_AGENT_LIST =  [  #这些请求头都是在网上复制的。
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