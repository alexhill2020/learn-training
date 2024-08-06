# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WeiboScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 用户所发微博
    since_id = scrapy.Field()
    crawl_time = scrapy.Field()
    created_at = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    reprint_cmt_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_description = scrapy.Field()
    user_follow_count = scrapy.Field()
    user_followers_count = scrapy.Field()
    user_statuses_count = scrapy.Field()
    user_verified = scrapy.Field()
    user_verified_reason = scrapy.Field()
    # 被转发微博
    retweet = scrapy.Field()  # 是否转发
    retweet_text = scrapy.Field()  # 转发微博内容
    retweet_created_at = scrapy.Field()  # 创建时间
    retweet_id = scrapy.Field()  # 转发微博ID
    retweet_source = scrapy.Field()  # 转发微博来源
    retweet_reposts_count = scrapy.Field()  # 转发次数
    retweet_comments_count = scrapy.Field()  # 评论次数
    retweet_reprint_cmt_count = scrapy.Field()  # 再次评论次数
    retweet_attitudes_count = scrapy.Field()  # 点赞次数
    retweet_user_name = scrapy.Field()  # 转发微博用户名称
    retweet_user_id = scrapy.Field()  # 转发微博用户ID
    retweet_user_description = scrapy.Field()  # 转发微博用户描述
    retweet_user_follow_count = scrapy.Field()  # 转发微博用户关注数
    retweet_user_followers_count = scrapy.Field()  # 转发微博用户粉丝数
    retweet_user_statuses_count = scrapy.Field()  # 转发微博用户微博数
    retweet_user_verified = scrapy.Field()  # 转发微博用户是否认证
    retweet_user_verified_reason = scrapy.Field()  # 转发微博用户认证原因
