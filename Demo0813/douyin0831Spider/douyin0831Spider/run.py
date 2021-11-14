import requests
import execjs
import re


def dy_sign_search(method,kw=None):
    with open('signature.js','r',encoding='utf-8') as f:
        b = f.read()
    c = execjs.compile(b)
    d = c.call(method,kw)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Referer": "https://www.douyin.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cookie": "ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; douyin.com; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; s_v_web_id=verify_77d2f7f2c1b8ef088a81ca21bbff2728; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; tt_scid=U5.m0tKDH9h8UpMYOyP3N6uy.GUIPTcZAtY12Tn08E0GLviAbmzv-4KBiW1lf1OE6198; msToken=I90XBXppnx5-PgCZUqUIiqfofOcU_WPBkpgebtSlx9_YyziV6BeReDnO5cDawdv5Mc_KqgNknvmanPpGYoXACUNLKBGDN1FIjhtvrx088TBTTgTHsqKN7uHhHg=="
    }

    #以下为实现翻页。
    f_url = re.findall('https://.*?offset=',d)  #匹配从https://到offset=的字符。
    l_url = re.findall('&count=.*',d) #匹配&count=之后的所有字符。

    responses = []
    i = 0
    while True:
        url = f_url[0] + str(i) + l_url[0]  #拼接url，以实现循环翻页功能。
        #print(url)

        e = requests.get(url=url, headers=headers)

        if len(e.text) < 500:  #返回的内容如小于500个字符，则表示无内容，直接退出。
            break
        i += 24

        responses.append(e.text)
        break

    return responses

def dy_sign_comment(method,kw=None):
    with open('signature.js','r',encoding='utf-8') as f:
        b = f.read()
    c = execjs.compile(b)
    d = c.call(method,kw)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Referer": "https://www.douyin.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cookie": "ttwid=1%7C9r7P4cfoIWDVRmkxcjCDP9H-n00OMleusK8vZXGe0Js%7C1630395910%7Cc4a8817da965ad1f57db7c5d88e113ed94711bb88d1431ab8237b9e76b362621; douyin.com; MONITOR_WEB_ID=b5d3a373-d457-4b10-ac25-35a1c47b8202; passport_csrf_token_default=23ec9cce92523054ed8b26c9d5cc4668; passport_csrf_token=23ec9cce92523054ed8b26c9d5cc4668; ttcid=c3d35b652f754bccb9a30e171d921fe413; s_v_web_id=verify_77d2f7f2c1b8ef088a81ca21bbff2728; odin_tt=16a40f2435f3b082963e16fb12ac5717f0b9f88858363e7f519778c9701d5ddb6a0dd641dd018b710879a0395092c70ddbbdf7a3265b4ded51b12b0766f95ddb; n_mh=Qwo8iNZvgETnzJxMIimO8EpI2tc5V2FecvoqZGqWB-o; sso_auth_status=9fb1cfd3f060de24b887070518cf5457; sso_auth_status_ss=9fb1cfd3f060de24b887070518cf5457; sso_uid_tt=0b0c13ee44dd1d669c4787e1fbcd59d4; sso_uid_tt_ss=0b0c13ee44dd1d669c4787e1fbcd59d4; toutiao_sso_user=ede088a6eb8061001cab4a94d90291b4; toutiao_sso_user_ss=ede088a6eb8061001cab4a94d90291b4; d_ticket=c1cfb67b0240e290999c08d07ef1cb166d5e6; passport_auth_status_ss=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; sid_guard=af5f57d750233aaacc3535e04983f5f7%7C1630395971%7C5184000%7CSat%2C+30-Oct-2021+07%3A46%3A11+GMT; uid_tt=c1e04973a22240dc5338ed3da87d1aca; uid_tt_ss=c1e04973a22240dc5338ed3da87d1aca; sid_tt=af5f57d750233aaacc3535e04983f5f7; sessionid=af5f57d750233aaacc3535e04983f5f7; sessionid_ss=af5f57d750233aaacc3535e04983f5f7; sid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; ssid_ucp_v1=1.0.0-KDE5NjJmOTVmNTJiMTU1Y2I3MzhlMTAwNDZjZDkxY2VjZDY4M2I5N2IKFQj8nIuJmgMQw7y3iQYY7zE4AkDxBxoCbGYiIGFmNWY1N2Q3NTAyMzNhYWFjYzM1MzVlMDQ5ODNmNWY3; passport_auth_status=ef3b01c95a68c24b486740c4a6849e4b%2C3e930b7168d50ea555fff750f1339b5e; tt_scid=U5.m0tKDH9h8UpMYOyP3N6uy.GUIPTcZAtY12Tn08E0GLviAbmzv-4KBiW1lf1OE6198; msToken=I90XBXppnx5-PgCZUqUIiqfofOcU_WPBkpgebtSlx9_YyziV6BeReDnO5cDawdv5Mc_KqgNknvmanPpGYoXACUNLKBGDN1FIjhtvrx088TBTTgTHsqKN7uHhHg=="
    }

    #以下为实现翻页。
    f_url = re.findall('https://.*?offset=',d)  #匹配从https://到offset=的字符。
    l_url = re.findall('&count=.*',d) #匹配&count=之后的所有字符。

    responses = []
    i = 0
    while True:

        i = 260
        url = f_url[0] + str(i) + l_url[0]  #拼接url，以实现循环翻页功能。
        print(url)

        e = requests.get(url=url, headers=headers)

        print(len(e.text))
        if len(e.text) < 500:  #返回的内容如小于500个字符，则表示无内容，直接退出。
            break
        i += 20

        responses.append(e.text)
        break

    return responses


if __name__ == '__main__':
    # 首页推荐视频
    #print(dy_sign(method='feed'))
    # 搜索视频
    #print(len((dy_sign_search(method='search_item',kw='垃圾分类'))))
    # 评论
    print(len(dy_sign_comment(method='cooment',kw='6711962289865575692')))
    #print('111')
    # 作品
    #print(dy_sign(method='aweme_post',kw='MS4wLjABAAAAIWFmTfNJmRajbViR_rK6iGgQMIq0lAWdFmQ5z6iU9Vd4uo9KXOgcJE0o5Dn0JAmW'))
    # TODO 其他的自行补充吧
    ...
