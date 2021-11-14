import scrapy
import execjs

'''
注意：
1，视频搜索页面每次爬到x + 90就中止了，换了cookies后又可以重新爬，因此持续爬的话必须建cookies池和ip代理池，必须建。
2，每次重新爬取时，前一次的log文件必须要改名，否则数据太多就混淆了。
3，有start_requests，就没法用scrapy_redis进行断点续爬和增量爬取，要实现这些功能还要好要研究一下。
4，经实验，抖音网页版搜索大概能出420个（offset基本到465），手机app搜索大概能出340个。更多的出不了。
'''


class Video0901Spider(scrapy.Spider):
    name = 'video0901'
    allowed_domains = ['www.douyin.com']
    start_urls = ['http://www.douyin.com/','www.amemv.com']  #出现Filtered offsite request to 'www.amemv.com'的原因是因为这里没有加允许的域名。

    def start_requests(self):

        #以下为调用js文件来生成请求网址的签名。
        method = 'search_item'
        kw = '垃圾分类'
        offset = '0' #0 首页
        count = '30' #30 首页
        with open('E:\\PycharmProjects\\Demo0813\\douyin0831Spider\\douyin0831Spider\\signature.js', 'r', encoding='utf-8') as f:
            b = f.read()
        c = execjs.compile(b)
        d = c.call(method, kw, offset ,count)  #我将signature.js文件里的search_item做了改造，主要是将1383行的offset和count从固定值改成了从外部赋值。

        #cookies。headers已在setting中设置，故此处不带headers，下面用cookies进行传递。
        temp = 'ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; douyin.com; s_v_web_id=verify_kt1u0oai_pzWhoQxN_mTqH_40BW_9xys_VyL2IUFMwYYW; msToken=ImPjjhnIALtDbSz8rh3yhP5StfVxj8ezWMTgoZBk9JDP4RzOzu9mPmtIh2eawd1cb-CmYunqlePY3O0ujab1NJN9P-pPCZXd_YmdQxe3k8Dm2tVKVJL0cbaVBQ==; tt_scid=UjWvo02bYyqcKCKP4jfkEtteuxhfY6jwTwpv7h8L4Kjo1Fd8T6.8m0e9Ji9Qh3Eg5801'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        yield scrapy.Request(url=d, cookies=cookies,callback=self.parse,meta={'cookiejar':1})


    def parse(self, response):
        response_main = response.json()
        has_more = response_main['has_more']  # 是否还有下一页，有为1，无为0。
        offset = response_main['cursor']  # 下一个页面的offset值。

        #翻页。
        if has_more == 1:
            # 重新调用js文件来生成签名，每个网址的签名都不一样。
            method = 'search_item'
            kw = '垃圾分类'
            count = '15'  # 固定值，第一页为30，从第二页开始是15。
            with open('E:\\PycharmProjects\\Demo0813\\douyin0831Spider\\douyin0831Spider\\signature.js', 'r',
                      encoding='utf-8') as f:
                b = f.read()
            c = execjs.compile(b)
            d = c.call(method, kw, offset, count)

            yield scrapy.Request(url=d, callback=self.parse, meta={'cookiejar': response.meta['cookiejar']})

        # 解析当前页面。
        for data in response_main['data']:
            item = {}  # 注意，item空字典一定要在循环里面，否则会出错，因为每循环一次就要传递一次参数，所以必须在里面。排查了好久。
            item['video_id'] = data['aweme_info']['aweme_id']
            item['video_title'] = data['aweme_info']['desc']
            item['video_create_time'] = data['aweme_info']['create_time']
            item['video_digg_count'] = data['aweme_info']['statistics']['digg_count']
            item['author_uid'] = data['aweme_info']['author']['uid']
            item['author_nickname'] = data['aweme_info']['author']['nickname']
            item['author_sec_uid'] = data['aweme_info']['author']['sec_uid']
            item['video_duration'] = data['aweme_info']['video']['duration']

            sub_url = 'https://www.amemv.com/web/api/v2/user/info/?sec_uid={}'.format(item['author_sec_uid'])
            yield scrapy.Request(url=sub_url, callback=self.author_parse, meta={'item': item,'cookiejar':response.meta['cookiejar']},dont_filter=True)


    def author_parse(self, response):  #爬取作者页信息。

        au_response = response.json()
        item = response.meta['item']

        item['authour_favoriting_count'] = au_response['user_info']['favoriting_count']  #喜欢作品数。
        item['authour_aweme_count'] = au_response['user_info']['aweme_count']  #发布作品数。
        item['author_following_count'] = au_response['user_info']['following_count']  #关注数。
        item['author_follower_count'] = au_response['user_info']['follower_count']  #粉丝数。
        item['author_total_favorited'] = au_response['user_info']['total_favorited']  #获赞数。
        item['author_is_gov_media_vip'] = au_response['user_info']['is_gov_media_vip'] #是否蓝V认证政务号。
        item['author_custom_verify'] = au_response['user_info']['custom_verify'] #是否黄V认证。
        try:
            item['author_is_enterprise_vip'] = au_response['user_info']['is_enterprise_vip']  #是否蓝V认证为企业号。
        except KeyError:
            item['author_is_enterprise_vip'] = None

        #爬取评论需要重新设置cookies，需要视频详情页的cookies。
        temp = 'ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; douyin.com; s_v_web_id=verify_kt1u0oai_pzWhoQxN_mTqH_40BW_9xys_VyL2IUFMwYYW; tt_scid=EdNE96fCqPdv7CbIu5f48DQSnfWCM37OOUtJFIyRz4hBR4NHwVrKv2drNzqmGR-K2036; msToken=nB46sdFvYbdlNblkv7Z6dvdHcaKlA3NumH8xZMh_CA1HZZoSIO92TgZa0f98YCa2VoTVvN6BptOWZ_XGsLzBGPgmmZkcjt5hAi0Dnlh5jA2dLtStoLz2mvhe'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        #重新调用js文件来生成签名，每个网址的签名都不一样。
        method = 'cooment'
        kw = item['video_id']
        cursor = '0'
        count = '20'
        with open('E:\\PycharmProjects\\Demo0813\\douyin0831Spider\\douyin0831Spider\\signature.js', 'r', encoding='utf-8') as f:
            b = f.read()
        c = execjs.compile(b)
        d = c.call(method, kw, cursor ,count)

        yield scrapy.Request(url=d, callback=self.aweme_parse, cookies=cookies,meta={'item': item})


    def aweme_parse(self, response):

        response_aweme = response.json()
        item = response.meta['item']

        cursor = response_aweme['cursor']  # 下一个页面的offset值。
        has_more = response_aweme['has_more']  # 是否还有下一页，有为1，无为0。
        comments = response_aweme['comments']

        #'''  #如果只爬视频的信息，则将此注释掉。
        if has_more == 1:
            #爬取评论需要重新设置cookies。同上。
            temp = 'ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; douyin.com; s_v_web_id=verify_kt1u0oai_pzWhoQxN_mTqH_40BW_9xys_VyL2IUFMwYYW; tt_scid=EdNE96fCqPdv7CbIu5f48DQSnfWCM37OOUtJFIyRz4hBR4NHwVrKv2drNzqmGR-K2036; msToken=nB46sdFvYbdlNblkv7Z6dvdHcaKlA3NumH8xZMh_CA1HZZoSIO92TgZa0f98YCa2VoTVvN6BptOWZ_XGsLzBGPgmmZkcjt5hAi0Dnlh5jA2dLtStoLz2mvhe'
            cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

            #重新调用js文件来生成签名，每个网址的签名都不一样。
            method = 'cooment'
            kw = item['video_id']
            count = '20'
            with open('E:\\PycharmProjects\\Demo0813\\douyin0831Spider\\douyin0831Spider\\signature.js', 'r', encoding='utf-8') as f:
                b = f.read()
            c = execjs.compile(b)
            d = c.call(method, kw, cursor ,count)


            yield scrapy.Request(url=d, callback=self.aweme_parse, cookies=cookies,meta={'item': item})
        #'''

        #对此页面进行解析。
        if comments == None :
            print('----------{}_视频没有任何评论----------'.format(item['video_id']))
            item['video_comment_total'] = 0  # 评论总数。
            item['comment_text'] = '_____没有任何评论_____'
            yield item
        else:
            item['video_comment_total'] = response_aweme['total']  # 评论总数

            for comment in comments:
                item['comment_id'] = comment['cid']  # 评论id，主要用于抓取二级评论。
                item['comment_creat_time'] = comment['create_time']  # 评论创建时间。
                item['comment_digg_count'] = comment['digg_count']  # 评论点赞数。
                item['comment_is_author_digged'] = comment['is_author_digged']  # 评论是否被作者点赞。
                try:
                    item['comment_reply_comment_total'] = comment['reply_comment_total']  # 二级评论数。有些没有二级评论数，故抛出异常。
                except KeyError:
                    item['comment_reply_comment_total'] = 0
                item['comment_text'] = comment['text']  # 评论文本。
                item['comment_user_name'] = comment['user']['nickname']  # 评论用户昵称。
                item['comment_user_sec_uid'] = comment['user']['sec_uid']  # 评论用户秘密id，用于定位用户的主页。
                item['comment_user_secret'] = comment['user']['secret']  # 评论用户是否为私密用户。
                item['comment_user_unique_id'] = comment['user']['unique_id']  # 评论用户的抖音号。
                # item['comment_user_gender'] = comments['user']['gender']  #一级评论的用户都没有性别与生日，二级评论有。
                # item['comment_user_birthday'] = comments['user']['birthday']
                item['comment_user_uid'] = comment['user']['uid']  # 评论用户注册时生成的id。
                item['coment_user_short_id'] = comment['user']['short_id']  # 评论用户的短id。

                yield item


        print(item)  #是一个页面打印一次，如果要全部打印，就放到循环中。





