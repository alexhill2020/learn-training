# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
import requests

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

'''#利用selenium自动登录模板。
class LoginMiddle(object):
    def process_request(self,request,spider):
        if spider.name=='cqmmgo815':#判断是哪个爬虫名
            if request.url.find('signup')!=-1:#这里signup是在链接中的signup，-1表示未登陆
                spider.broswer=webdriver.Chrome()
                spider.broswer.get(request.url)#获取url，myzhihu中的start_url
                time.sleep(1)
                spider.broswer.find_element_by_xpath('//div[@class="SignContainer-switch"]/span').click()
                time.sleep(1)
                #获取输入框
                username=spider.broswer.find_element_by_name('username')#
                password=spider.broswer.find_element_by_name('password')
                #传值
                username.send_keys("188775729")
                password.send_keys("changeme_123")
                time.sleep(5)
                spider.broswer.find_element_by_xpath('//button[@class="Button SignFlow-submitButton Button--primary Button--blue"]').click()
                time.sleep(2)
                #获取登录后cookie
                spider.cookies=spider.broswer.get_cookies()
                return HtmlResponse(url=spider.broswer.current_url,#当前的url即登录后的url
                                        body=spider.broswer.page_source,#Gets the source of the current page.
                                            encoding="utf-8")
            else:
                # requests请求登录
                session=requests.session()#请求session
                #cookie一个字典
                for cookie in spider.cookies:
                    session.cookies.set(cookie['name',cookie['value']])
                    session.headers.clear()#清除头
                    newpage=session.get(request.url,verify=False).content.decode()
                    return HtmlResponse(url=request.url,body=newpage,encoding='urf-8')
'''

class Cqmmgo0815SpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Cqmmgo0815SpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
