import scrapy
import re


class Weibo0823Spider(scrapy.Spider):
    name = 'weibo0823'
    allowed_domains = ['weibo.cn']
    #start_urls = ['https://weibo.cn/u/2970452952']
    start_urls = ['https://m.weibo.cn/comments/hotflow?id=4353796790279702&mid=4353796790279702&max_id_type=0']

    def start_requests(self):  # 这是重写start_requests，以携带并传递cookies，如果不传递则可以直接在setting中设置。

        # 这里是带上cookies，重写此start_requests就是为了携带cookies，否则无需重写。
        # 而且也只有在start_request里写了cookies，才能实现cookies传递，在parse里写的cookies不能传递，传递用meta的cookiejar参数，具体可百度。
        # cookies会失效，还要研究如何才能自动生成并切换cookies。
        # 下面的temp为从浏览器的Network-->XHR中复制的cookie地址,需要将其变成字典格式。
        temp = 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWwuWXU8YuIimVP6JSElkZ25NHD95QpS0MfeKnXSoe7Ws4Dqcj_i--RiKn0i-2pi--Xi-z4i-zpi--Ri-8si-82i--Xi-z4iKyFi--ciKLhi-8W; _T_WM=42857180007; SUB=_2A25MIATtDeRhGedJ7FcQ-CrKyDyIHXVv6qylrDV6PUJbkdCOLUnFkW1NUbjvqCzcbmgfzBCDo11o3lLvJFOMOlmd; SCF=Aj00dJCaIsig6Qf6v4yl_BbuKBykvPfT7mpawafN1e6cgoq0ZP2-LvXlPMA8HGGBEqHDp6qkMhU4nScVR2SQ9I0.; SSOLoginState=1629779134; MLOGIN=1; WEIBOCN_FROM=1110106030; XSRF-TOKEN=1aedb5; M_WEIBOCN_PARAMS=oid%3D4353796790279702%26luicode%3D20000061%26lfid%3D4353796790279702%26uicode%3D20000061%26fid%3D4353796790279702'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            ':authority': 'm.weibo.cn',
            ':method': 'GET',
            ':path': '/ comments / hotflow?id = 4353796790279702 & mid = 4353796790279702 & max_id_type = 0',
            ':scheme': 'https',
            'accept': 'application / json, text / plain, * / *',
            'accept - encoding': 'gzip, deflate, br',
            'accept - language': 'zh - CN, zh; q = 0.9',
            'mweibo - pwa': '1',
            'referer': 'https: // m.weibo.cn / detail / 4353796790279702',
            'sec - ch - ua': '"Chromium"; v = "92", " Not A;Brand"; v = "99", "Google Chrome"; v = "92"',
            'sec - ch - ua - mobile': '?0',
            'sec - fetch - dest': 'empty',
            'sec - fetch - mode': 'cors',
            'sec - fetch - site': 'same - origin',
            'x - requested - with': 'XMLHttpRequest',
            'x - xsrf - token': '1aedb5',
        }

        for url in self.start_urls:  # 因为上面的start_urls是一个列表，所以这里要遍历，以对每一个url发起请求。
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 headers=headers,
                                 meta={'cookiejar': 1},  # meta={'cookiejar':1}表示传递此函数中构建的cookies。
                                 cookies=cookies,  # 这里必须要带cookies访问，即使此start_url可以不带cookies访问，不然cookies无法传递给下一个函数。
                                 dont_filter=True)  # dont_filter=True表示在调度器中不过滤此地址。


    def parse(self, response):

        #print(response.text)
        response_json = response.json()
        max_id = response_json['data']['max_id']

        sub_url = 'https://m.weibo.cn/comments/hotflow?id=4353796790279702&mid=4353796790279702&max_id={}&max_id_type=0'.format(max_id)

        print(max_id)

        yield scrapy.Request(url=sub_url,callback=self.parse,meta={'cookiejar':response.meta['cookiejar']},dont_filter=True)







    '''
        def start_requests(self):  # 这是重写start_requests，以携带并传递cookies，如果不传递则可以直接在setting中设置。

            # 这里是带上cookies，重写此start_requests就是为了携带cookies，否则无需重写。
            # 而且也只有在start_request里写了cookies，才能实现cookies传递，在parse里写的cookies不能传递，传递用meta的cookiejar参数，具体可百度。
            # cookies会失效，还要研究如何才能自动生成并切换cookies。
            # 下面的temp为从浏览器的Network-->XHR中复制的cookie地址,需要将其变成字典格式。
            temp = 'SUB=_2A25MJ7A9DeRhGedJ7FcQ-CrKyDyIHXVv69B1rDV6PUJbktAKLWfVkW1NUbjvqIVxmCj__3gE4XhiXTBMhyUDCqH6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWwuWXU8YuIimVP6JSElkZ25NHD95QpS0MfeKnXSoe7Ws4Dqcj_i--RiKn0i-2pi--Xi-z4i-zpi--Ri-8si-82i--Xi-z4iKyFi--ciKLhi-8W; SSOLoginState=1629732973; MLOGIN=1; _T_WM=42857180007; M_WEIBOCN_PARAMS=oid%3D4673430056077523%26luicode%3D20000061%26lfid%3D4673430056077523'
            cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}  # 通过此步骤将直接复制的cookie转换成字典。

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            }

            for url in self.start_urls:  # 因为上面的start_urls是一个列表，所以这里要遍历，以对每一个url发起请求。
                yield scrapy.Request(url=url,
                                     callback=self.parse,
                                     headers=headers,
                                     meta={'cookiejar': 1},  # meta={'cookiejar':1}表示传递此函数中构建的cookies。
                                     cookies=cookies,  # 这里必须要带cookies访问，即使此start_url可以不带cookies访问，不然cookies无法传递给下一个函数。
                                     dont_filter=True)  # dont_filter=True表示在调度器中不过滤此地址。

    
    
    
    def parse(self, response):

        #print(response.text)
        divs = response.xpath('.//body/div[@class="c" and @id]')
        item = {}
        for div in divs:
            text = div.xpath('./div/span[@class="ctt"]/text()').extract()
            item['weibo_text'] = ''.join(i.replace(' ','') for i in text)  #微博正文。
            comments_url = div.xpath('./div/a[@class = "cc"]/@href').extract()  # 此时comments_url为一个list。
            item['comments_url'] = (comments_url[0]).replace('#cmtfrm', '')  #微博详情页网址。
            weibo_time = div.xpath('./div/span[@class="ct"]/text()').get()
            item['weibo_time'] = weibo_time


            #print(weibo_time)


            if len(div.xpath('./div')) == 2:  #如果微博中有图片。
                if len(div.xpath('./div[2]/a')) == 3:  #如果已赞。
                    thumb_num = div.xpath('./div[2]/span[@class="cmt"]/text()').get()
                    item['thumb_num'] = (re.search(r'\d+', thumb_num)).group(0)  # 正则表达式\d+表示匹配数字。
                    trans_num = div.xpath('./div[2]/a[1]/text()').get()
                    item['trans_num'] = (re.search(r'\d+', trans_num)).group(0)
                    comment_num = div.xpath('./div[2]/a[@class = "cc"]/text()').get()
                    item['comment_num'] = (re.search(r'\d+', comment_num)).group(0)
                else:  #如果还未赞。
                    thumb_num = div.xpath('./div[2]/a[3]/text()').get()
                    item['thumb_num'] = (re.search(r'\d+', thumb_num)).group(0)
                    trans_num = div.xpath('./div[2]/a[4]/text()').get()
                    item['trans_num'] = (re.search(r'\d+',trans_num)).group(0)
                    comment_num = div.xpath('./div[2]/a[@class = "cc"]/text()').get()
                    item['comment_num'] = (re.search(r'\d+',comment_num)).group(0)
            else:  #如果微博中没有图片。
                if len(div.xpath('./div/a')) == 3:  #如果已赞。
                    thumb_num = div.xpath('./div/span[@class="cmt"]/text()').get()
                    item['thumb_num'] = (re.search(r'\d+', thumb_num)).group(0)
                    trans_num = div.xpath('./div/a[1]/text()').get()
                    item['trans_num'] = (re.search(r'\d+',trans_num)).group(0)
                    comment_num = div.xpath('./div/a[@class = "cc"]/text()').get()
                    item['comment_num'] = (re.search(r'\d+',comment_num)).group(0)
                else:  #如果还未赞。
                    thumb_num = div.xpath('./div/a[1]/text()').get()
                    item['thumb_num'] = (re.search(r'\d+', thumb_num)).group(0)
                    trans_num = div.xpath('./div/a[2]/text()').get()
                    item['trans_num'] = (re.search(r'\d+',trans_num)).group(0)
                    comment_num = div.xpath('./div/a[@class = "cc"]/text()').get()
                    item['comment_num'] = (re.search(r'\d+',comment_num)).group(0)


            #print(thumb_num,trans_num,comment_num)
            #print(item)

            page_num = (int(item['comment_num']) // 10) + 2 #评论总页数。 //为整除，%为取模（余数）。

            comments_page_url = [item['comments_url'] + '&&page={}'.format(i) for i in range(1,page_num)]
            print(item['comment_num'],page_num,comments_page_url[-1])

            #yield scrapy.Request
            break
        '''



