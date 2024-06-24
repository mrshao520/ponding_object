# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals

# useful for handling different item types with a single interface
from scrapy.http import HtmlResponse

from src.pachong.utils import  create_chrome_driver

class SouhuSpiderMiddleware:
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
        spider.logger.info("Spider opened: %s" % spider.name)


import time
from scrapy.http import HtmlResponse
from scrapy import signals


class SouhuDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def __init__(self):
        self.browser = create_chrome_driver()

    def process_request(self, request, spider):
        meta_data = request.meta.get('href')
        if meta_data:
            self.browser.get(request.url)
            time.sleep(2)
            print(meta_data)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8')


    def process_response(self, request, response, spider):
        # 处理响应，如果需要的话
        return response

    def process_exception(self, request, exception, spider):
        # 处理异常情况，可以根据需要返回响应、请求或者抛出 IgnoreRequest
        pass


class SouhuDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def __init__(self):
        self.browser = create_chrome_driver()

    def process_request(self, request, spider):
        if 'middleware' in request.meta and request.meta['middleware'] == 'souhu.middlewares.SouhuDownloaderMiddleware':
            self.browser.get(request.url)
            time.sleep(2)
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8')
        return None


    def process_response(self, request, response, spider):
        # 处理响应，如果需要的话
        return response

    def process_exception(self, request, exception, spider):
        # 处理异常情况，可以根据需要返回响应、请求或者抛出 IgnoreRequest
        pass



class SecondeDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

    def process_request(self, request, spider):
        if 'middleware' in request.meta and request.meta['middleware'] == 'souhu.middlewares.SecondeDownloaderMiddleware':
            print(2341)
            return request
        return None

    def process_response(self, request, response, spider):
        # 处理响应，如果需要的话
        return response

    def process_exception(self, request, exception, spider):
        # 处理异常情况，可以根据需要返回响应、请求或者抛出 IgnoreRequest
        pass