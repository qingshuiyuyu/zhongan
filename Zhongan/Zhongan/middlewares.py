# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from scrapy.http import HtmlResponse


class ZhonganSpiderMiddleware(object):
    def process_request(self, request, spider):
        """ selenium 处理没有数据的代码"""
        if request.meta.has_key('selenium'):
            driver = webdriver.PhantomJS()

            print request.url
            # driver = webdriver.PhantomJS()
            driver.get(request.url)
            # driver.get("http://www.baidu.com/")
            # print driver.page_source
            time.sleep(2)

            body = driver.page_source
            url = driver.current_url
            driver.quit()


            return HtmlResponse(url, body=body, encoding='utf-8', request=request)

