import scrapy
import json
import datetime
from urllib.parse import urlparse, parse_qs
import logging

class WeiboSearchSpider(scrapy.Spider):
    name = 'weibo_search'
    allowed_domains = ['m.weibo.cn','weibo.com']
    start_urls = ['http://m.weibo.cn/','https://weibo.com/']

    def start_requests(self):

        #已在settings.py中设置了默认Headers

        search_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E4%B8%AD%E5%9B%BD%E5%88%B6%E9%80%A0&page_type=searchall&page=1'


        yield scrapy.Request(url = search_url, callback=self.parse, meta={'search_url': search_url})

    def parse(self, response):

        response_data = response.json()
        search_url = response.meta['search_url']  # 获取原始搜索 URL
        print("搜索网址为：" + search_url)

        query = urlparse(response.url).query
        params = parse_qs(query)
        current_page = int(params['page'][0]) if 'page' in params else 1

        print(f"当前为第{current_page}页，此页面的OK码为{response_data['ok']}。")

        #打印响应状态码
        if response.status == 200:
            print(f"搜索主页面第{current_page}页HTTP响应成功，长度为{len(response.text)}。响应状态码为：", response.status)
        else:
            print(f"搜索主页面第{current_page}页请求失败，HTTP状态码:", response.status)


        #ok_info = response_data.get('ok',0)
        # 正确地访问cards列表，这假设cards是在data键下的

        if response_data.get('ok') == 1:
            cards = response_data.get('data', {}).get('cards', [])
            remaining_cards = len(cards)  # 设置剩余卡片的数量



            # 打印cards列表的长度
            print(f'第{current_page}页总共有{len(cards)}个列表数据。')
            for i in range(5):
                card = cards[i]
                remaining_cards -= 1
                print(remaining_cards)
                item = {} #这个放在循环中，以确保每次循环的时候item都为空，可填入新的数据。
                item['expected_parts'] = 2  # 假设我们需要两部分数据：全文和评论
                # 确保card_type的类型匹配，这里假设card_type是整数
                if card.get('card_type') == 9 and 'mblog' in card:
                    #item['mblog_text'] = card['mblog'].get('text', '未找到文本')  #微博文本
                    item['attitudes_count'] = card['mblog'].get('attitudes_count', 0)  #点赞数
                    item['comments_count'] = card['mblog'].get('comments_count', 0)  #评论数
                    item['reposts_count'] = card['mblog'].get('reposts_count', 0)  #转发数
                    created_at = card['mblog'].get('created_at', 0)
                    date_obj = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                    item['created_at'] = formatted_date  #发布时间
                    item['mblog_id'] = card['mblog'].get('id', '无微博详情页')  #详情页ID。
                    mblog = card['mblog']
                    user = mblog.get('user', {})  # 使用默认空字典以防 'user' 键不存在
                    user_id = user.get('id', '无用户详情页')  # 如果 'user' 字典中没有 'id'，返回 '无详情页'
                    item['user_id'] = user_id  # 将获取的 user_id 存入 item
                    item['current_page'] = current_page

                    full_text_url = f"https://m.weibo.cn/statuses/extend?id={item['mblog_id']}"
                    #comments_url = f"https://m.weibo.cn/comments/hotflow?id={item['mblog_id']}&mid={item['mblog_id']}"
                    #user_url = f"https://weibo.com/ajax/profile/info?uid={item['user_id']}"

                    user_url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={item['user_id']}&containerid = 100505{item['user_id']}"
                    #user_detail_url = f"https://weibo.com/ajax/profile/detail?uid={item['user_id']}"



                    yield scrapy.Request(url=full_text_url, callback=self.full_text_parse,
                                         meta={'item': item, 'remaining_cards': remaining_cards, 'search_url': search_url}, dont_filter=True)

                    # yield scrapy.Request(url=comments_url, callback=self.comments_parse,
                    #                      meta={'item': item}, dont_filter=True)

                    yield scrapy.Request(url=user_url, callback=self.user_parse,
                                         meta={'item': item, 'remaining_cards': remaining_cards, 'search_url': search_url}, dont_filter=True)

                    # yield scrapy.Request(url=user_detail_url, callback=self.user_detail_parse,
                    #                      meta={'item': item}, dont_filter=True)

                    #yield item
                    #print('card为9的文本为：', item)

                elif card.get('card_type') == 11:
                    # 安全访问card_group列表并检查它是否非空
                    if card.get('card_group') and card['card_group']:
                        # 遍历card_group中的每一个sub_card
                        for sub_card in card['card_group']:
                            # 确保sub_card中的card_type是9，并且存在mblog字典
                            #print(sub_card)
                            if sub_card.get('card_type') == 9 and 'mblog' in sub_card:
                                #mblog = sub_card['mblog']
                                #item['mblog_text'] = sub_card['mblog'].get('text', '未找到文本')
                                # item['attitudes_count'] = card['mblog'].get('attitudes_count', 0)  #点赞数
                                # item['comments_count'] = card['mblog'].get('comments_count', 0)  #评论数
                                # item['reposts_count'] = card['mblog'].get('reposts_count', 0)  #转发数
                                #print('card为11且内部card_type为9的文本为：', item['mblog_text'])
                                created_at = sub_card['mblog'].get('created_at', 0)
                                date_obj = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                                formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                                item['created_at'] = formatted_date  # 发布时间
                                item['mblog_id'] = sub_card['mblog'].get('id', '无微博详情页')  # 详情页ID。
                                mblog = sub_card['mblog']
                                user = mblog.get('user', {})  # 使用默认空字典以防 'user' 键不存在
                                user_id = user.get('id', '无用户详情页')  # 如果 'user' 字典中没有 'id'，返回 '无详情页'
                                item['user_id'] = user_id  # 将获取的 user_id 存入 item
                                item['current_page'] = current_page

                                full_text_url = f"https://m.weibo.cn/statuses/extend?id={item['mblog_id']}"
                                #comments_url = f"https://m.weibo.cn/comments/hotflow?id={item['mblog_id']}&mid={item['mblog_id']}"
                                user_url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={item['user_id']}&containerid = 100505{item['user_id']}"
                                #user_detail_url = f"https://weibo.com/ajax/profile/detail?uid={item['user_id']}"

                                # mheaders = {
                                #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                                #     'Referer': 'https://m.weibo.cn/',
                                #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                                # }
                                #
                                # wheaders = {
                                #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
                                #     'Cookie': 'SINAGLOBAL=3946552063838.196.1679919372048; UOR=,,www.baidu.com; __gpi=UID=00000c75c35d83c8:T=1698416420:RT=1698416420:S=ALNI_MZ9r_xc11QotMM_xD07CgdeCpn1IA; _ga=GA1.1.806990726.1698416421; __gads=ID=6c95397c004a1d1f-225cd0bb28e5004a:T=1698416420:RT=1698416423:S=ALNI_MacDe6x1io7IW02xntTFu8Kwk4jbw; _ga_QZXMWYY4QK=GS1.1.1698416422.1.1.1698416453.29.0.0; _ga_7WMZ8XEWGJ=GS1.1.1698416422.1.1.1698416453.0.0.0; _ga_B61YQPGY9T=GS1.1.1698416422.1.1.1698416453.0.0.0; _ga_DL2CM4NHWS=GS1.1.1698416422.1.1.1698416453.0.0.0; SCF=AnNXfFfJaLhO0QDML_mivRnTemXvyYw46veOreh0S3c-9e0hvMQP53eP3voY0yn8J691UpUwJJuwdywnrha-fwU.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhKlxWT8Vs0ffppg0hdSMBY5JpX5KMhUgL.Fo-peo2feKqR1Kn2dJLoI79jINS.qJMt; ALF=1715558686; SUB=_2A25LHbxODeRhGeNP6VMU8SjEwjSIHXVoUrGGrDV8PUJbkNB-LVPbkW1NTr09mFwL61SV8-uzmSy0Zsnm5Shpg_hH; XSRF-TOKEN=WiP8OdXQACoRc6CZcfp2UvXP; _s_tentry=weibo.com; Apache=9403379620132.895.1713090304723; ULV=1713090304734:79:6:1:9403379620132.895.1713090304723:1712592279364; WBPSESS=qVtvXfM6Pp6_zHT86UWMDXy0WdGu8OU_iInSPZg-SBLJJW-buC3Dec3Cm-Rnq1ZW8Mo1cXv_he7UfMERZoFYvgAE3wCX1cAzD6cWZzD-ZC-Tj5jRS-VGGCwFVkY68Rb89LhqoOTXrUGX2qpTthSVgw==',
                                #     'Referer': 'https://weibo.com/',
                                #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                                # }



                                yield scrapy.Request(url=full_text_url, callback=self.full_text_parse,
                                                     meta={'item': item, 'remaining_cards': remaining_cards, 'search_url': search_url}, dont_filter=True)

                                # yield scrapy.Request(url=comments_url, callback=self.comments_parse,
                                #                      meta={'item': item}, dont_filter=True)

                                yield scrapy.Request(url=user_url, callback=self.user_parse,
                                                     meta={'item': item, 'remaining_cards': remaining_cards, 'search_url': search_url}, dont_filter=True)
                #break

        # next_page = response.url.split('page=')[0] + 'page=' + str(
        #     int(response.url.split('page=')[1]) + 1)
        # yield scrapy.Request(url=next_page, callback=self.parse)

                                # yield scrapy.Request(url=user_detail_url, callback=self.user_detail_parse,
                                #                      meta={'item': item}, dont_filter=True)



    def full_text_parse(self, response):
        remaining_cards = response.meta['remaining_cards']
        print(f"111:{remaining_cards}")
        full_text_response = response.json()
        item = response.meta['item']
        search_url = response.meta['search_url']  # 获取原始搜索 URL

        #打印响应状态码
        if response.status == 200:
            print(f"第{item['current_page']}页微博全文{item['mblog_id']}页面HTTP响应成功，长度为{len(response.text)}。响应状态码为：", response.status)
        else:
            print(f"第{item['current_page']}页微博全文{item['mblog_id']}页面请求失败，HTTP状态码:", response.status)



        item['text'] = full_text_response.get('data',{}).get('longTextContent','无全文信息')
        item['attitudes_count'] = full_text_response.get('data', {}).get('attitudes_count', 0)
        item['comments_count'] = full_text_response.get('data', {}).get('comments_count', 0)
        item['reposts_count'] = full_text_response.get('data', {}).get('reposts_count', 0)

        #comments_url = f"https://m.weibo.cn/comments/hotflow?id={item['mblog_id']}&mid={item['mblog_id']}"

        # 更新完成的部分计数器
        #item['expected_parts'] -= 1

        # 检查是否所有部分都已完成
        if item['expected_parts'] <= 0:
            yield item
            print(f"第{item['current_page']}页{item['mblog_id']}的微博全文及{item['user_id']}的用户信息已存储。")
            #print("111" + search_url)
        else:
            # 将更新后的 item 放回 meta 传递到另一个请求
            response.meta['item'] = item

        # 更新计数器
        remaining_cards -= 1
        if remaining_cards <= 0:
            # 检查所有的卡片是否都已处理完成
            next_page = search_url.split('page=')[0] + 'page=' + str(
                int(search_url.split('page=')[1]) + 1)
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'search_url': search_url})
        else:
            # 更新meta信息，传递到可能的其他请求
            response.meta['remaining_cards'] = remaining_cards



    # def comments_parse(self, response):
    #
    #     #打印响应状态码
    #     if response.status == 200:
    #         print(f"评论页面HTTP响应成功，长度为{len(response.text)}。响应状态码为：", response.status)
    #     else:
    #         print("评论页面请求失败，HTTP状态码:", response.status)
    #
    #     comments_response = response.json()
    #     item = response.meta['item']
    #
    #     comments_dates = comments_response.get('data',{}).get('data',[])
    #     max_id = comments_response.get('data',{}).get('max_id', 0)
    #     for comments_data in comments_dates:
    #         comments_data.get('created_at',0)
    #
    #
    #     item['attitudes_count'] = comments_response.get('data', {}).get('attitudes_count', 0)
    #     item['comments_count'] = comments_response.get('data', {}).get('comments_count', 0)
    #     item['reposts_count'] = comments_response.get('data', {}).get('reposts_count', 0)
    #
    #     #comments_url = f"https://m.weibo.cn/comments/hotflow?id={item['mblog_id']}&mid={item['mblog_id']}"
    #
    #     yield item

    def user_parse(self, response):
        #print(f"user_parse的response为：{response}")
        remaining_cards = response.meta['remaining_cards']
        print(f"222:{remaining_cards}")
        user_response = response.json()
        item = response.meta['item']
        search_url = response.meta['search_url']  # 获取原始搜索 URL

        #打印响应状态码
        if response.status == 200:
            print(f"第{item['current_page']}页微博{item['mblog_id']}发布者{item['user_id']}页面HTTP响应成功，长度为{len(response.text)}。响应状态码为：", response.status)
        else:
            print(f"第{item['current_page']}页微博{item['mblog_id']}发布者{item['user_id']}页面请求失败，HTTP状态码:", response.status)


        user_info = user_response.get('data',{}).get('userInfo',{})
        item['user_name'] = user_info.get('screen_name',"未获取到名字信息")  #用户名
        item['verified'] = user_info.get('verified',"未获取到认证信息")  #是否认证
        if item.get('verified'):
            item['verified_reason'] = user_info.get('verified_reason',"未获取到认证原因")  #认证原因
        else:
            item['verified_reason'] = "未验证"
        item['description'] = user_info.get('description', "未获取到简介信息")  # 是否认证
        item['location'] = user_info.get('location', "未获取到地区信息")  # 是否认证
        item['gender'] = user_info.get('gender', "未获取到性别信息")  # 是否认证
        item['followers_count'] = user_info.get('followers_count', "未获取到粉丝数")  # 是否认证
        item['follow_count'] = user_info.get('follow_count', "未获取到关注数")  # 是否认证
        item['statuses_count'] = user_info.get('statuses_count', "未获取到statuses_count")  # 是否认证

        # 更新完成的部分计数器
        #item['expected_parts'] -= 1

        # 检查是否所有部分都已完成
        if item['expected_parts'] <= 0:
            yield item
            print(f"第{item['current_page']}页{item['mblog_id']}的微博全文及{item['user_id']}的用户信息已存储。")
            #print("222" + search_url)
        else:
            # 将更新后的 item 放回 meta 传递到另一个请求
            response.meta['item'] = item

        # 更新计数器
        remaining_cards -= 1
        if remaining_cards <= 0:
            # 检查所有的卡片是否都已处理完成
            next_page = search_url.split('page=')[0] + 'page=' + str(
                int(search_url.split('page=')[1]) + 1)
            yield scrapy.Request(url=next_page, callback=self.parse, meta={'search_url': search_url})
        else:
            # 更新meta信息，传递到可能的其他请求
            response.meta['remaining_cards'] = remaining_cards


    # def user_detail_parse(self, response):
    #
    #     #打印响应状态码
    #     if response.status == 200:
    #         print(f"用户详情（Ajax）页面HTTP响应成功，长度为{len(response.text)}。响应状态码为：", response.status)
    #     else:
    #         print("用户详情（Ajax）页面请求失败，HTTP状态码:", response.status)
    #
    #     try:
    #         return response.json()
    #         user_detail_response = response.json()
    #         item = response.meta['item']
    #
    #         item['user_detail'] = user_detail_response.get('detail',{})
    #
    #         # 更新完成的部分计数器
    #         item['expected_parts'] -= 1
    #
    #         # 检查是否所有部分都已完成
    #         if item['expected_parts'] <= 0:
    #             yield item
    #         else:
    #             # 将更新后的 item 放回 meta 传递到另一个请求
    #             response.meta['item'] = item
    #
    #     except json.JSONDecodeError:
    #         self.logger.error('解析JSON失败，URL：{}'.format(response.url))
    #
    #         item['user_detail'] = '解析错误'
    #
    #         # 检查是否所有部分都已完成
    #         if item['expected_parts'] <= 0:
    #             yield item
    #         else:
    #             # 将更新后的 item 放回 meta 传递到另一个请求
    #             response.meta['item'] = item
    #
    #         return None

        # user_detail_response = response.json()
        # item = response.meta['item']
        # 
        # item['user_detail'] = user_detail_response.get('detail',{})
        # 
        # # 更新完成的部分计数器
        # item['expected_parts'] -= 1
        # 
        # # 检查是否所有部分都已完成
        # if item['expected_parts'] <= 0:
        #     yield item
        # else:
        #     # 将更新后的 item 放回 meta 传递到另一个请求
        #     response.meta['item'] = item