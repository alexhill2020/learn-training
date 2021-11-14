# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Douyin0831SpiderItem(scrapy.Item):
    video_id = scrapy.Field()
    video_title = scrapy.Field()
    video_create_time = scrapy.Field()
    video_comment_total = scrapy.Field()
    video_digg_count = scrapy.Field()
    video_duration = scrapy.Field()
    author_uid = scrapy.Field()
    author_nickname = scrapy.Field()
    author_sec_uid = scrapy.Field()
    comment_id = scrapy.Field()
    comment_creat_time = scrapy.Field()
    comment_digg_count = scrapy.Field()
    comment_is_author_digged = scrapy.Field()
    comment_reply_comment_total = scrapy.Field()
    comment_text = scrapy.Field()
    comment_user_name = scrapy.Field()
    comment_user_sec_uid = scrapy.Field()
    comment_user_secret = scrapy.Field()
    comment_user_unique_id = scrapy.Field()
    #comment_user_gender = scrapy.Field()
    #comment_user_birthday = scrapy.Field()
    comment_user_uid = scrapy.Field()
    coment_user_short_id = scrapy.Field()

class Douyin0831SpiderItem(scrapy.Item):
    video_id = scrapy.Field()
    video_title = scrapy.Field()
    video_create_time = scrapy.Field()
    video_digg_count = scrapy.Field()
    video_duration = scrapy.Field()
    video_comment_total = scrapy.Field()
    author_uid = scrapy.Field()
    author_nickname = scrapy.Field()
    author_sec_uid = scrapy.Field()
    authour_favoriting_count = scrapy.Field()
    authour_aweme_count = scrapy.Field()
    author_following_count = scrapy.Field()
    author_follower_count = scrapy.Field()
    author_total_favorited = scrapy.Field()
    author_is_gov_media_vip = scrapy.Field()
    author_is_enterprise_vip = scrapy.Field()
    author_custom_verify = scrapy.Field()
    comment_id = scrapy.Field()
    comment_creat_time = scrapy.Field()
    comment_digg_count = scrapy.Field()
    comment_is_author_digged = scrapy.Field()
    comment_reply_comment_total = scrapy.Field()
    comment_text = scrapy.Field()
    comment_user_name = scrapy.Field()
    comment_user_sec_uid = scrapy.Field()
    comment_user_secret = scrapy.Field()
    comment_user_unique_id = scrapy.Field()
    #comment_user_gender = scrapy.Field()
    #comment_user_birthday = scrapy.Field()
    comment_user_uid = scrapy.Field()
    coment_user_short_id = scrapy.Field()


