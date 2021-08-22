# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Cqmmgo0815SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title=scrapy.Field()
    num_read=scrapy.Field()
    num_reply=scrapy.Field()
    num_collect=scrapy.Field()
    user_name=scrapy.Field()
    user_url=scrapy.Field()
    user_tool=scrapy.Field()
    user_social=scrapy.Field()
    user_time=scrapy.Field()
    content_text_str=scrapy.Field()
    content_img_url=scrapy.Field()
    user_sign=scrapy.Field()
    title_url_full=scrapy.Field()
    renew_time=scrapy.Field()
    publish_time=scrapy.Field()
    user_id=scrapy.Field()
    user_post_num=scrapy.Field()
    user_attends_num=scrapy.Field()
    user_fans_num=scrapy.Field()
    user_gender=scrapy.Field()
    #user_city=scrapy.Field()
