# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    since_id = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_description = scrapy.Field()
    user_follow_count = scrapy.Field()
    user_followers_count = scrapy.Field()
    user_statuses_count = scrapy.Field()
    user_verified = scrapy.Field()
    created_at = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
    source = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    reprint_cmt_count = scrapy.Field()
    attitudes_count = scrapy.Field()
