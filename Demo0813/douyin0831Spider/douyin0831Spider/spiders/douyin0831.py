import scrapy
import re
import execjs
#import run


class Douyin0831Spider(scrapy.Spider):
    name = 'douyin0831'
    allowed_domains = ['www.douyin.com']
    start_urls = ['http://www.douyin.com/']

    def start_requests(self):

        method = 'search_item'
        kw = '垃圾分类'

        with open('E:\\PycharmProjects\\Demo0813\\douyin0831Spider\\douyin0831Spider\\signature.js', 'r', encoding='utf-8') as f:
            b = f.read()
        c = execjs.compile(b)
        d = c.call(method, kw)

        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Referer": "https://www.douyin.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            #"cookie": "ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; douyin.com; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; s_v_web_id=verify_77d2f7f2c1b8ef088a81ca21bbff2728; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; tt_scid=U5.m0tKDH9h8UpMYOyP3N6uy.GUIPTcZAtY12Tn08E0GLviAbmzv-4KBiW1lf1OE6198; msToken=I90XBXppnx5-PgCZUqUIiqfofOcU_WPBkpgebtSlx9_YyziV6BeReDnO5cDawdv5Mc_KqgNknvmanPpGYoXACUNLKBGDN1FIjhtvrx088TBTTgTHsqKN7uHhHg=="
        }

        temp = 'ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; douyin.com; s_v_web_id=verify_kt0y33p7_MRjRY2fE_2Ab8_4wHx_8Kdi_kSdmzrYg1nRt; tt_scid=xPE2txLzoRrsHEF0X2nVgcVELwTVEiWNV7aCXUeJidxRllOkqZD-o2p8qrKz22r08e75; msToken=OfswzENTbspWw7Jz8B_nHfgYCMFuyoDcaXMcMF1-F97gA6SvXC2lYsPpx23c9tW5-J4EI9khHsmiuy7JpOhWwqzGqssxjIOqjaGdl_oUHMYdXiyZu7ZBLsz9NA=='
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        yield scrapy.Request(url=d,headers=headers,cookies=cookies,callback=self.parse,meta={'cookiejar':1})



    def parse(self, response):
        response_main = response.json()
        print(response_main)

        cursor = response_main['cursor']  #下一个页面的offset值。
        has_more = response_main['has_more']  # 是否还有下一页，有为1，无为0。

        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Referer": "https://www.douyin.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            #"cookie": "ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; douyin.com; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; s_v_web_id=verify_77d2f7f2c1b8ef088a81ca21bbff2728; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; tt_scid=U5.m0tKDH9h8UpMYOyP3N6uy.GUIPTcZAtY12Tn08E0GLviAbmzv-4KBiW1lf1OE6198; msToken=I90XBXppnx5-PgCZUqUIiqfofOcU_WPBkpgebtSlx9_YyziV6BeReDnO5cDawdv5Mc_KqgNknvmanPpGYoXACUNLKBGDN1FIjhtvrx088TBTTgTHsqKN7uHhHg=="
        }

        temp = 'ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; douyin.com; s_v_web_id=verify_kt0y33p7_MRjRY2fE_2Ab8_4wHx_8Kdi_kSdmzrYg1nRt; tt_scid=xPE2txLzoRrsHEF0X2nVgcVELwTVEiWNV7aCXUeJidxRllOkqZD-o2p8qrKz22r08e75; msToken=OfswzENTbspWw7Jz8B_nHfgYCMFuyoDcaXMcMF1-F97gA6SvXC2lYsPpx23c9tW5-J4EI9khHsmiuy7JpOhWwqzGqssxjIOqjaGdl_oUHMYdXiyZu7ZBLsz9NA=='
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        #解析当前页面。
        for data in response_main['data']:
            item = {}   #注意，item空字典一定要在循环里面，否则会出错，因为每循环一次就要传递一次参数，所以必须在里面。排查了好久。
            item['video_id'] = data['aweme_info']['aweme_id']
            item['video_title'] = data['aweme_info']['desc']
            item['video_create_time'] = data['aweme_info']['create_time']
            item['video_digg_count'] = data['aweme_info']['statistics']['digg_count']
            item['author_uid'] = data['aweme_info']['author']['uid']
            item['author_nickname'] = data['aweme_info']['author']['nickname']
            item['author_sec_uid'] = data['aweme_info']['author']['sec_uid']
            item['video_duration'] = data['aweme_info']['video']['duration']

            sub_url = 'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={}&cursor=0&count=20'.format(str(item['video_id']))
            #sub_url = 'https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=6980246507567992100&cursor=0&count=20'
            yield scrapy.Request(url=sub_url,callback=self.aweme_parse,headers=headers,cookies=cookies,meta={'item':item})

        #爬取下一页。
        url = response.url
        f_url = re.findall('https://.*?offset=', url)  # 匹配从https://到offset=的字符。
        l_url = re.findall('&count=.*', url)  # 匹配&count=之后的所有字符。

        if has_more == 1:
            full_url = f_url[0] + str(cursor) + l_url[0]  #拼接网址，cursor为下一页的offset值。一定要找到定位下一页的标志，不然就从当前网址中来，用正则表达式提取，不要想着去搞什么while循环。
            yield scrapy.Request(url=full_url, callback=self.parse, headers=headers, cookies=cookies)


    def aweme_parse(self, response):  #抓取一级评论及用户信息。

        headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Referer": "https://www.douyin.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            # "cookie": "ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; douyin.com; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; s_v_web_id=verify_77d2f7f2c1b8ef088a81ca21bbff2728; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; tt_scid=U5.m0tKDH9h8UpMYOyP3N6uy.GUIPTcZAtY12Tn08E0GLviAbmzv-4KBiW1lf1OE6198; msToken=I90XBXppnx5-PgCZUqUIiqfofOcU_WPBkpgebtSlx9_YyziV6BeReDnO5cDawdv5Mc_KqgNknvmanPpGYoXACUNLKBGDN1FIjhtvrx088TBTTgTHsqKN7uHhHg=="
        }

        temp = 'ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; douyin.com; s_v_web_id=verify_kt0y33p7_MRjRY2fE_2Ab8_4wHx_8Kdi_kSdmzrYg1nRt; tt_scid=xPE2txLzoRrsHEF0X2nVgcVELwTVEiWNV7aCXUeJidxRllOkqZD-o2p8qrKz22r08e75; msToken=OfswzENTbspWw7Jz8B_nHfgYCMFuyoDcaXMcMF1-F97gA6SvXC2lYsPpx23c9tW5-J4EI9khHsmiuy7JpOhWwqzGqssxjIOqjaGdl_oUHMYdXiyZu7ZBLsz9NA=='
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        response_aweme = response.json()
        #print(response_aweme)
        item = response.meta['item']
        #print(item,response.url)
        cursor = response_aweme['cursor']  # 下一个页面的offset值。
        has_more = response_aweme['has_more']  # 是否还有下一页，有为1，无为0。
        comments = response_aweme['comments']

        if comments == None :
            print('当前视频没有任何评论')
            item['video_comment_total'] = 0  # 评论总数。
            item['comment_text'] = '_____没有任何评论_____'
            #yield item
        else:
            item['video_comment_total'] = response_aweme['total']  # 评论总数

            for comment in comments:
                item['comment_id'] = comment['cid']  # 评论id，主要用于抓取二级评论。
                item['comment_creat_time'] = comment['create_time']  # 评论创建时间。
                item['comment_digg_count'] = comment['digg_count']  # 评论点赞数。
                item['comment_is_author_digged'] = comment['is_author_digged']  # 评论是否被作者点赞。
                item['comment_reply_comment_total'] = comment['reply_comment_total']  # 二级评论数。
                item['comment_text'] = comment['text']  # 评论文本。
                item['comment_user_name'] = comment['user']['nickname']  # 评论用户昵称。
                item['comment_user_sec_uid'] = comment['user']['sec_uid']  # 评论用户秘密id，用于定位用户的主页。
                item['comment_user_secret'] = comment['user']['secret']  # 评论用户是否为私密用户。
                item['comment_user_unique_id'] = comment['user']['unique_id']  # 评论用户的抖音号。
                # item['comment_user_gender'] = comments['user']['gender']  #一级评论的用户都没有性别与生日，二级评论有。
                # item['comment_user_birthday'] = comments['user']['birthday']
                item['comment_user_uid'] = comment['user']['uid']  # 评论用户注册时生成的id。
                item['coment_user_short_id'] = comment['user']['short_id']  # 评论用户的短id。

                #yield item

                # 爬取下一页。
                url = response.url
                f_url = re.findall('https://.*?cursor=', url)  # 匹配从https://到offset=的字符。
                l_url = re.findall('&count=.*', url)  # 匹配&count=之后的所有字符。

                if has_more == 1:
                    full_url = f_url[0] + str(cursor) + l_url[
                        0]  # 拼接网址，cursor为下一页的offset值。一定要找到定位下一页的标志，不然就从当前网址中来，用正则表达式提取，不要想着去搞什么while循环。
                    yield scrapy.Request(url=full_url, callback=self.aweme_parse, headers=headers, cookies=cookies,
                                         meta={'item': item})



'''        
        #try:  #如果视频有评论，即返回的response有内容。
        response_aweme = response.json()
        print(response_aweme)
        item = response.meta['item']
        try:
            cursor = response_aweme['cursor']  #下一个页面的offset值。
            has_more = response_aweme['has_more']  # 是否还有下一页，有为1，无为0。
            item['video_comment_total'] = response_aweme['total']  #评论总数。

            comments = response_aweme['comments']
            for comment in comments:
                item['comment_id'] = comment['cid']  #评论id，主要用于抓取二级评论。
                item['comment_creat_time'] = comment['create_time']  #评论创建时间。
                item['comment_digg_count'] = comment['digg_count']  #评论点赞数。
                item['comment_is_author_digged'] = comment['is_author_digged']  #评论是否被作者点赞。
                item['comment_reply_comment_total'] = comment['reply_comment_total']  #二级评论数。
                item['comment_text'] = comment['text'] #评论文本。
                item['comment_user_name'] = comment['user']['nickname'] #评论用户昵称。
                item['comment_user_sec_uid'] = comment['user']['sec_uid']  #评论用户秘密id，用于定位用户的主页。
                item['comment_user_secret'] = comment['user']['secret']  #评论用户是否为私密用户。
                item['comment_user_unique_id'] = comment['user']['unique_id']  #评论用户的抖音号。
                #item['comment_user_gender'] = comments['user']['gender']  #一级评论的用户都没有性别与生日，二级评论有。
                #item['comment_user_birthday'] = comments['user']['birthday']
                item['comment_user_uid'] = comment['user']['uid'] #评论用户注册时生成的id。
                item['coment_user_short_id'] = comment['user']['short_id']  #评论用户的短id。

                yield item


                # 爬取下一页。
                url = response.url
                f_url = re.findall('https://.*?cursor=', url)  # 匹配从https://到offset=的字符。
                l_url = re.findall('&count=.*', url)  # 匹配&count=之后的所有字符。

                if has_more == 1:
                    full_url = f_url[0] + str(cursor) + l_url[
                        0]  # 拼接网址，cursor为下一页的offset值。一定要找到定位下一页的标志，不然就从当前网址中来，用正则表达式提取，不要想着去搞什么while循环。
                    yield scrapy.Request(url=full_url, callback=self.aweme_parse, headers=headers, cookies=cookies,
                                         meta={'item': item})
        except TypeError:
            print('当前视频没有任何评论')
            item['video_comment_total'] = 0  # 评论总数。
            item['comment_text'] = '_____没有任何评论_____'

        yield item
'''

        #暂不爬取二级评论。二级评论的网址为‘https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=6711962289865575692&cursor=0&count=20’








