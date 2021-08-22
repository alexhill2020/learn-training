
import scrapy

class Cqmmgo0815Spider(scrapy.Spider):   #继承Spider中的类。
    name = 'cqmmgo0815'
    allowed_domains = ['go.cqmmgo.com']
    start_urls = ['https://go.cqmmgo.com/forum-222-{}.html' .format(page) for page in range(1,501)]
    #start_urls = ['https://go.cqmmgo.com/forum-222-1.html']  #爬虫起始页。


    def start_requests(self):   #这是重写start_requests，以携带cookies。

        #这里是带上cookies，重写此start_requests就是为了携带cookies，否则无需重写。
        #而且也只有在start_request里写了cookies，才能实现cookies传递，在parse里写的cookies不能传递，传递用meta的cookiejar参数，具体可百度。
        #cookies会失效，还要研究如何才能自动生成并切换cookies。
        #下面的temp为从浏览器的Network-->XHR中复制的cookie地址,需要将其变成字典格式。
        temp = '_DM_SID_=bad83ec19f5b52ef739f9847ff75bfcd; _Z3nY0d4C_=37XgPK9h; M_SMILEY_TIP_HIDE=1; _9755xjdesxxd_=32; __snaker__captcha=1lqyHepQARR7oXGB; gdxidpyhxdE=JoRsPg6SDKX%5CDSV67PdPhyXHKfk5%2Bw%5C6i6Y5xgm2SQoJHuumD243osDL22yCvqNu2%5CVU0NiVvd3OScM5jHQligiAB7EPOh6jz9%5CLVmAyx%2F%2FdS2iEY4%2FUYTBO1Ix79lv%2Bgrl8Z4Wx%2Ff%2FrNEO1mteE0iczASPUAvET%5CeUD87OZYyi0GB7z%3A1625140331690; pm_count=%7B%7D; JSESSIONID=50606A76EB4FF374005F42ECB2588533; f9big_cq=cq178; Hm_lvt_368b91c8b5ab4c95de73b2b9b158b9af=1628937734,1628999947,1629211209,1629268395; _DM_S_=595858f1199f65812eaedbd8520a3d5d; f39big=ip76; dayCount=%5B%5D; fr_adv=; f9bigsec=u105; f9big_read=bq134; screen=1351; f100big_read=bq134; cuid=rWHGkiEeqBAvC28todkfVs6M54xWGjcS; isAddHomeScreen=false; Hm_lvt_db68a43fedf04ba24c901edd34c74600=1629270021; Hm_lpvt_db68a43fedf04ba24c901edd34c74600=1629293981; fr_adv_last=login_entry_dengluye_dl; _dm_userinfo=%7B%22ext%22%3A%22%22%2C%22uid%22%3A%2250287966%22%2C%22stage%22%3A%22%22%2C%22city%22%3A%22%E9%87%8D%E5%BA%86%3A%E9%87%8D%E5%BA%86%22%2C%22ip%22%3A%22113.251.43.167%22%2C%22sex%22%3A%221%22%2C%22frontdomain%22%3A%22go.cqmmgo.com%22%2C%22category%22%3A%22%E6%83%85%E6%84%9F%2C%E6%97%B6%E5%B0%9A%22%7D; Hm_lpvt_368b91c8b5ab4c95de73b2b9b158b9af=1629297928; _dm_tagnames=%5B%7B%22k%22%3A%22%E7%9B%B8%E4%BA%B2%E6%B4%BB%E5%8A%A8%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%2290%E5%90%8E%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A27%7D%2C%7B%22k%22%3A%2280%E5%90%8E%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A4%7D%2C%7B%22k%22%3A%22%E6%95%B4%E5%AE%B9%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%8F%8C%E7%9C%BC%E7%9A%AE%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%BE%AE%E6%95%B4%E5%BD%A2%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E7%94%B7%E7%94%9F%E5%BE%81%E5%8F%8B%22%2C%22c%22%3A4%7D%2C%7B%22k%22%3A%22%E7%9B%B8%E4%BA%B2%E8%AF%9D%E9%A2%98%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E7%9B%B8%E4%BA%B2%E4%BA%A4%E5%8F%8B%E8%AE%BA%E5%9D%9B%22%2C%22c%22%3A109%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E5%90%8C%E5%9F%8E%E4%BA%A4%E5%8F%8B%22%2C%22c%22%3A109%7D%2C%7B%22k%22%3A%22%E4%B8%BB%E5%9F%8E%E7%9B%B8%E4%BA%B2%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%222021%E5%B9%B4%E5%BE%81%E5%A9%9A%E5%A4%A7%E8%B5%9B%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%8D%9A%E5%A3%AB%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%94%B7%E7%94%9F%E8%BA%AB%E9%AB%98170%E4%BB%A5%E4%B8%8B%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A5%B3%E7%94%9F%E5%BE%81%E5%8F%8B%22%2C%22c%22%3A30%7D%2C%7B%22k%22%3A%22%E7%A6%BB%E5%BC%82%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%86%B2%E5%88%BA%E7%9A%84%E5%B0%8F%E9%BC%A0c688%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%A4%A7%E4%B8%93%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A5%B3%E7%94%9F%E8%BA%AB%E9%AB%98155%E4%BB%A5%E4%B8%8A%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%BB%BA%E8%AE%AE%22%2C%22c%22%3A2%7D%5D'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        for url in self.start_urls:    #因为上面的start_urls是一个列表，所以这里要遍历，以对每一个url发起请求。
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'cookiejar':1},  #meta={'cookiejar':1}表示传递此函数中构建的cookies。
                                 cookies=cookies,  #这里必须要带cookies访问，即使此start_url可以不带cookies访问，不然cookies无法传递给下一个函数。
                                 dont_filter=True) #dont_filter=True表示在高度器中不过滤此地址。


    def parse(self,response):

        #key = response.meta['cookiejar']
        #上面是接收上面传下来的cookies，start_request函数中的'cookiejar':1是给cookies做标记，一个cookie表示一个会话(session)，如果需要经多个会话对某网站进行爬取，可以对cookie做标记1,2,3,4......这样scrapy就维持了多个会话。
        #如果需要做标记的cookies，下面的yield的meat则写'cookiejar'：key，否则写'cookiejar':response.meta['cookiejar']，可参考网页：https://www.zhihu.com/question/54773510。

        divs = response.xpath('//div[@class="new-data-item"]')  #这里是用xpath获取爬虫起始页里的某些元素。要提取的数据所在的div，这一页总共有37个div。
        for div in divs:   #遍历前面获得的divs，再在单独的div里提取需要的元素。
            #print(div)

            title_url = div.xpath('./div[@class="title"]/div/a/@href').get()   #获取每个详情页的url，以在一下步中对每个详情页进行爬虫。
            publish_time = div.xpath('./div[@class="author"]/span/text()').get()  #获取发帖时间。

            title_url_full = 'http:'+title_url  #补全详情页。如果不测试，则启用这个。注意，这个网页必须带cookies才能访问，因此必须传cookies。
            #title_url_full = 'https://go.cqmmgo.com/forum-222-thread-95631629017726773-1-1.html'  #测试用的，只固定抓取一个url免得循环太多。

            item = {}
            item['title_url_full'] = title_url_full
            item['publish_time'] = publish_time

            #注意，yield是传递，scrapy.Request就是在爬取，因此下面这行语句就是在爬取。
            yield scrapy.Request(url=title_url_full,
                                 meta={'item':item,'cookiejar':response.meta['cookiejar']},  #'cookiejar':response.meta['cookiejar']，如果启用上面传参数的start_request(self)，则这里必须加到meta中。
                                 callback=self.parse_title,  #callback=self.parse_title是将爬取结果交给下面的函数解析。
                                 )

    def parse_title(self,response):   #此函数解析爬取到的详情页。

        item = response.meta['item']

        # 取帖子阅读、回复状态等。
        view_div = response.xpath('//*[@id="view-hd"]')   #状态版块。
        item['title'] = view_div.xpath('./h1/a/span/text()').get()   #标题。
        item['num_read'] = view_div.xpath('./ul/li[1]/i/text()').get()  #阅读数。
        item['num_reply'] = view_div.xpath('./ul/li[2]/i/text()').get()  #回复数。
        item['num_collect'] = view_div.xpath('./ul/li[3]/i/text()').get()  #收藏数。
        #item['num_praise'] = response.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div/div[@class="cont-bd"]/div[@class="main-post-actions-message"]/ul/li/div/text()').get()  #点赞数。点赞数暂时获取不到，因为数字被包裹在<em></em>中，这里的获取不到，还待解决。
        user_sign = response.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div/div[@class="cont-bd"]/div[@class="view-ft"]/div[@class="user-sign"]/text()').get()
        if user_sign:
            item['user_sign'] = user_sign.replace('\n','').replace(' ','')  #发帖用户签名。
        else:
            item['user_sign'] = '--没有签名--'

        #取主贴全部文本及全部图片链接。
        content_divs = response.xpath(
            '//*[@id="view-bd"]/div[@itemprop="post"]/div/div[@class="cont-bd"]/div/table/tbody/tr/td/div[@class="thread-cont"]'
            '/div[not(@class="view-fullmodle")]'  #之所以分两段是因为太长了，不好阅读，其实是两段拼接在一起的。
        )  #div[not(@class="view-fullmodle")]，选取不包含属性值class="view-fullmodle"的div，避免有的帖子中会出现“只看楼主大图”的div。
        text_divs = content_divs.xpath('./div[not(div)]')  #取主贴全部文本。#div[not(div)]，选取不包含div子节点的div。

        content_text_str = ''
        for sub_div in text_divs:  ##此时text_divs是个可迭代的选择器，因为不包含div子节点的div有很多个。因此可以用for循环逐一提取。
            content_text = sub_div.xpath('./text()').get()   #选取sub_div的文本。
            if content_text:
                content_text_str += content_text
        if content_text_str:
            item['content_text_str'] = content_text_str
        else:
            item['content_text_str'] = '--没有写任何文字--'

        content_img_url = ''
        img_divs = content_divs.xpath('./div')  #取主贴全部图片链接。
        for img_div in img_divs:  #此时img_divs是个可迭代的选择器，因为包含div子节点的div有很多个。因此可以用for循环逐一提取。
            img_url = img_div.xpath('./img/@src').get()
            if img_url:
                content_img_url += img_url
                content_img_url += '  '
        if content_img_url:
            item['content_img_url'] = content_img_url
        else:
            item['content_img_url'] = '--没有任何照片--'

        #取发帖用户信息。
        user_div = response.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div[@class="side 453"]')
        item['user_url'] = 'http:' + (user_div.xpath('./div/div/a/@href').get())
        item['user_name'] = (user_div.xpath('./div/div/a/span/text()').get()).replace('\n','').replace(' ','')
        item['user_id'] = user_div.xpath('./p/a/@userid').get()
        user_gender = user_div.xpath('./p/a[@ttname="bbs_followta"]/span/text()').get()
        item['user_gender'] = user_gender.replace('关注','').replace('他','男').replace('她','女').replace('TA','保密')
        item['user_tool'] = user_div.xpath('//*[@id="view-bd"]/div/div/div/p/a/text()').get()
        item['renew_time'] = (user_div.xpath('//*[@id="view-bd"]/div/div/div//ul/li/text()').get()).replace('更新于\xa0','')
        item['user_social'] = user_div.xpath('./dl[@class="color9 uinfo clearall"]/dd[@class="usocial"]/span/text()').get()
        item['user_time'] = user_div.xpath('./dl[@class="color9 uinfo clearall"]/dd[@class="color6"]/text()').get()

        #print(item)
        #yield item   #以下为爬取用户页数据，如需继续爬取就将'''注释掉，否则将此yield item注释掉，将'''释放。

#'''

        user_id = item['user_id']

        # 注意，以下为用户详情页，只能登录后查看，因此爬取以下页面时必须要有cookies，否则是未登录状态。2021-08-18 22:40不需要详情页，帮取消。
        # 如何判断是已登录，还是未登录？这里还要研究研究。如果未登录好像会返回一个网址：https://go.cqmmgo.com/login?r=aHR0cDovL2dvLmNxbW1nby5jb20vdXNlci9wcm9maWxlLTQ1NDIwMjA5LTEuaHRtbA==&P_ATTENTION=false&P_ATTENTION_COUNT=9&isBlogLog=0&P_THREAD_COUNT=0&P_USER_TOTAL_SCORE=12010&P_BRAND_FEED_COUNT=0&hisskin=default&P_PICTURE_COUNT=0&P_BIND_UID=&P_FANS_COUNT=175&P_USER_GROUP=%CE%C2%DC%B0%D7%AF%D4%B0&P_BRAND_ADOPT=0&isBanUser=false
        #user_url = 'https://go.cqmmgo.com/user/profile-{}-1.html'.format(user_id)  # 电脑浏览器页面，用于爬取用户名称、性别、城市

        user_af_num_url = 'https://go.cqmmgo.com/u/ajaxApi/user/otherInfo/getInfo?uid={}'.format(user_id)  # 电脑wap端页面，用于爬取用户关注数和粉丝数。
        #注意，此网址不登录也可以访问，因此不用继续传cookies。

        yield scrapy.Request(url=user_af_num_url,
                             meta={'item': item},  #爬取user页面时必须要有cookies，否则是未登录状态。
                             callback=self.parse_user_af,
                             )  # dont_filter=True


        #下面本想一次传递多个，结果发现这样item没法完整yield，因此采取依次传递的方式。
        #yield scrapy.Request(url=user_af_num_url,
        #                     meta={'item': item},
        #                     callback=self.parse_user_af,
        #                     headers=headers,
        #                     cookies=cookies,)

        #yield scrapy.Request(url=user_post_url,
        #                     callback=self.parse_user_post,
        #                     meta={'item': item},
        #                     headers=headers,
        #                     cookies=cookies,)


    '''
    def parse_user(self,response):   #此函数用于爬user页面，主要为取性别和城市，但这个页面需登录，为尽可能减少登录的影响，不启动这个。性别可从“关注她/他/Ta”中取，城市基本空着，不取。

        item = response.meta['item']

        item['user_name'] = response.xpath('//div[@id="head-wrap"]/div[@class="user-mod"]/h1[@class="ta-home"]/a/text()').get()
        item['user_gender'] = response.xpath(
            '//div[@id="cont-wrap"]/div[@id="main-wrap"]/div[@id="home-wrap"]/div[@class="main-mod"]/div[@class="main-bd"]/table/tr[@class="f12 color6"]/td[@width="115"]/text()').get()
        item['user_city'] = response.xpath(
            '//div[@id="cont-wrap"]/div[@id="main-wrap"]/div[@id="home-wrap"]/div[@class="main-mod"]/div[@class="main-bd"]/table/tr/td[@width="275"]/text()').get()


        user_id = item['user_id']
        user_af_num_url = 'https://go.cqmmgo.com/u/ajaxApi/user/otherInfo/getInfo?uid={}'.format(user_id)  # 电脑wap端页面，用于爬取用户关注数和粉丝数。
        #注意，上面的网址不登录也可以访问，因此不用继续传cookies。

        yield scrapy.Request(url=user_af_num_url,
                             meta={'item': item},
                             callback=self.parse_user_af,
                             )  # dont_filter=True
    '''

    def parse_user_af(self, response):
        response_af = response.json()
        item = response.meta['item']
        user_attends_num = response_af['data']['attendsNum']
        user_fans_num = response_af['data']['fansCount']
        item['user_attends_num'] = user_attends_num
        item['user_fans_num'] = user_fans_num

        user_id = item['user_id']
        user_post_url = 'https://go.cqmmgo.com/u/util/user/info?uid={}'.format(user_id)  # 电脑wap端页面，用于爬取用户发帖数。

        yield scrapy.Request(url=user_post_url,
                             meta={'item': item},
                             callback=self.parse_user_post,
                             )  # dont_filter=True


    def parse_user_post(self, response):
        item = response.meta['item']
        response_json = response.json()
        user_post_num = response_json['data']['threads']
        item['user_post_num'] = user_post_num

        #print('2222',item)

        yield item


#'''



