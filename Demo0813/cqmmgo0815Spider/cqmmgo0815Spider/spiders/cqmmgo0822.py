import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request


class Cqmmgo0822Spider(CrawlSpider):
    name = 'cqmmgo0822'
    allowed_domains = ['go.cqmmgo.com']
    #start_urls = ['https://go.cqmmgo.com/forum-222-{}.html' .format(page) for page in range(1,501)]
    #start_urls = ['https://go.cqmmgo.com/forum-222-1.html']  #爬虫起始页。
    start_urls = ['https://go.cqmmgo.com/forum-222-1.html?order=lastpost&appid=loveList']


    rules = (
        Rule(LinkExtractor(restrict_css=('.subject')), callback='parse_item', follow=True),
        #Rule

    )


    def parse_item(self, response):

        item = {}
        view_div = response.xpath('//*[@id="view-hd"]')  # 状态版块。
        item['title'] = view_div.xpath('./h1/a/span/text()').get()  # 标题。
        item['num_read'] = view_div.xpath('./ul/li[1]/i/text()').get()  # 阅读数。
        item['num_reply'] = view_div.xpath('./ul/li[2]/i/text()').get()  # 回复数。
        item['num_collect'] = view_div.xpath('./ul/li[3]/i/text()').get()  # 收藏数。
        # item['num_praise'] = response.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div/div[@class="cont-bd"]/div[@class="main-post-actions-message"]/ul/li/div/text()').get()  #点赞数。点赞数暂时获取不到，因为数字被包裹在<em></em>中，这里的获取不到，还待解决。
        user_sign = response.xpath(
            '//*[@id="view-bd"]/div[@itemprop="post"]/div/div[@class="cont-bd"]/div[@class="view-ft"]/div[@class="user-sign"]/text()').get()
        if user_sign:
            item['user_sign'] = user_sign.replace('\n', '').replace(' ', '')  # 发帖用户签名。
        else:
            item['user_sign'] = '--没有签名--'

        # 取主贴全部文本及全部图片链接。
        content_divs = response.xpath(
            '//*[@id="view-bd"]/div[@itemprop="post"]/div/div[@class="cont-bd"]/div/table/tbody/tr/td/div[@class="thread-cont"]'
            '/div[not(@class="view-fullmodle")]'  # 之所以分两段是因为太长了，不好阅读，其实是两段拼接在一起的。
        )  # div[not(@class="view-fullmodle")]，选取不包含属性值class="view-fullmodle"的div，避免有的帖子中会出现“只看楼主大图”的div。
        text_divs = content_divs.xpath('./div[not(div)]')  # 取主贴全部文本。#div[not(div)]，选取不包含div子节点的div。

        content_text_str = ''
        for sub_div in text_divs:  ##此时text_divs是个可迭代的选择器，因为不包含div子节点的div有很多个。因此可以用for循环逐一提取。
            content_text = sub_div.xpath('./text()').get()  # 选取sub_div的文本。
            if content_text:
                content_text_str += content_text
        if content_text_str:
            item['content_text_str'] = content_text_str
        else:
            item['content_text_str'] = '--没有写任何文字--'

        content_img_url = ''
        img_divs = content_divs.xpath('./div')  # 取主贴全部图片链接。
        for img_div in img_divs:  # 此时img_divs是个可迭代的选择器，因为包含div子节点的div有很多个。因此可以用for循环逐一提取。
            img_url = img_div.xpath('./img/@src').get()
            if img_url:
                content_img_url += img_url
                content_img_url += '  '
        if content_img_url:
            item['content_img_url'] = content_img_url
        else:
            item['content_img_url'] = '--没有任何照片--'

        # 取发帖用户信息。
        user_div = response.xpath('//*[@id="view-bd"]/div[@itemprop="post"]/div[@class="side 453"]')
        item['user_url'] = 'http:' + (user_div.xpath('./div/div/a/@href').get())
        item['user_name'] = (user_div.xpath('./div/div/a/span/text()').get()).replace('\n', '').replace(' ', '')
        item['user_id'] = user_div.xpath('./p/a/@userid').get()
        user_gender = user_div.xpath('./p/a[@ttname="bbs_followta"]/span/text()').get()
        item['user_gender'] = user_gender.replace('关注', '').replace('他', '男').replace('她', '女').replace('TA', '保密')
        item['user_tool'] = user_div.xpath('//*[@id="view-bd"]/div/div/div/p/a/text()').get()
        item['renew_time'] = (user_div.xpath('//*[@id="view-bd"]/div/div/div//ul/li/text()').get()).replace('更新于\xa0',
                                                                                                            '')
        item['user_social'] = user_div.xpath(
            './dl[@class="color9 uinfo clearall"]/dd[@class="usocial"]/span/text()').get()
        item['user_time'] = user_div.xpath('./dl[@class="color9 uinfo clearall"]/dd[@class="color6"]/text()').get()

        yield item
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item

    def start_requests(self):
        temp = '_DM_SID_=bad83ec19f5b52ef739f9847ff75bfcd; _Z3nY0d4C_=37XgPK9h; M_SMILEY_TIP_HIDE=1; _9755xjdesxxd_=32; __snaker__captcha=1lqyHepQARR7oXGB; gdxidpyhxdE=JoRsPg6SDKX%5CDSV67PdPhyXHKfk5%2Bw%5C6i6Y5xgm2SQoJHuumD243osDL22yCvqNu2%5CVU0NiVvd3OScM5jHQligiAB7EPOh6jz9%5CLVmAyx%2F%2FdS2iEY4%2FUYTBO1Ix79lv%2Bgrl8Z4Wx%2Ff%2FrNEO1mteE0iczASPUAvET%5CeUD87OZYyi0GB7z%3A1625140331690; pm_count=%7B%7D; JSESSIONID=50606A76EB4FF374005F42ECB2588533; f9big_cq=cq178; Hm_lvt_368b91c8b5ab4c95de73b2b9b158b9af=1628937734,1628999947,1629211209,1629268395; _DM_S_=595858f1199f65812eaedbd8520a3d5d; f39big=ip76; dayCount=%5B%5D; fr_adv=; f9bigsec=u105; f9big_read=bq134; screen=1351; f100big_read=bq134; cuid=rWHGkiEeqBAvC28todkfVs6M54xWGjcS; isAddHomeScreen=false; Hm_lvt_db68a43fedf04ba24c901edd34c74600=1629270021; Hm_lpvt_db68a43fedf04ba24c901edd34c74600=1629293981; fr_adv_last=login_entry_dengluye_dl; _dm_userinfo=%7B%22ext%22%3A%22%22%2C%22uid%22%3A%2250287966%22%2C%22stage%22%3A%22%22%2C%22city%22%3A%22%E9%87%8D%E5%BA%86%3A%E9%87%8D%E5%BA%86%22%2C%22ip%22%3A%22113.251.43.167%22%2C%22sex%22%3A%221%22%2C%22frontdomain%22%3A%22go.cqmmgo.com%22%2C%22category%22%3A%22%E6%83%85%E6%84%9F%2C%E6%97%B6%E5%B0%9A%22%7D; Hm_lpvt_368b91c8b5ab4c95de73b2b9b158b9af=1629297928; _dm_tagnames=%5B%7B%22k%22%3A%22%E7%9B%B8%E4%BA%B2%E6%B4%BB%E5%8A%A8%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%2290%E5%90%8E%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A27%7D%2C%7B%22k%22%3A%2280%E5%90%8E%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A4%7D%2C%7B%22k%22%3A%22%E6%95%B4%E5%AE%B9%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%8F%8C%E7%9C%BC%E7%9A%AE%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%BE%AE%E6%95%B4%E5%BD%A2%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E7%94%B7%E7%94%9F%E5%BE%81%E5%8F%8B%22%2C%22c%22%3A4%7D%2C%7B%22k%22%3A%22%E7%9B%B8%E4%BA%B2%E8%AF%9D%E9%A2%98%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E7%9B%B8%E4%BA%B2%E4%BA%A4%E5%8F%8B%E8%AE%BA%E5%9D%9B%22%2C%22c%22%3A109%7D%2C%7B%22k%22%3A%22%E9%87%8D%E5%BA%86%E5%90%8C%E5%9F%8E%E4%BA%A4%E5%8F%8B%22%2C%22c%22%3A109%7D%2C%7B%22k%22%3A%22%E4%B8%BB%E5%9F%8E%E7%9B%B8%E4%BA%B2%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%222021%E5%B9%B4%E5%BE%81%E5%A9%9A%E5%A4%A7%E8%B5%9B%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%8D%9A%E5%A3%AB%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%94%B7%E7%94%9F%E8%BA%AB%E9%AB%98170%E4%BB%A5%E4%B8%8B%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A5%B3%E7%94%9F%E5%BE%81%E5%8F%8B%22%2C%22c%22%3A30%7D%2C%7B%22k%22%3A%22%E7%A6%BB%E5%BC%82%E5%BE%81%E5%A9%9A%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%86%B2%E5%88%BA%E7%9A%84%E5%B0%8F%E9%BC%A0c688%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%A4%A7%E4%B8%93%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%A5%B3%E7%94%9F%E8%BA%AB%E9%AB%98155%E4%BB%A5%E4%B8%8A%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%BB%BA%E8%AE%AE%22%2C%22c%22%3A2%7D%5D'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}
        yield scrapy.Request(url=self.start_urls[0],
                             cookies=cookies,
                             dont_filter=True)