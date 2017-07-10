# -*- coding: utf-8 -*-
import scrapy

from Zhongan.items import ZhonganItem
import json
import re


class ZhonganSpider(scrapy.Spider):
    name = 'zhongan'
    allowed_domains = ['zhongan.com']
    start_urls = ['https://www.zhongan.com/index']
    baseURL = "https://www.zhongan.com/dm/open/aggregation/productAggregation.vm?channelEnName="

    #匹配type链接
    def parse(self, response):
        result = response.body
        urls = re.compile(r'vm\?channelEnName=(\w+)').findall(result)
        for url in urls:

            yield scrapy.Request(self.baseURL+url, callback=self.parse_links)

    #匹配每一个产品链接
    def parse_links(self, response):
        result = response.text
        #print ("===")*20
        url1 = re.compile(r'(/p/\d+\?channelEnName\=\w+)').findall(result)
        print len(url1)
        urls = []
        for url in url1:
            url = 'https://www.zhongan.com'+url
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_item)

    #处理信息
    def parse_item(self, response):
        item = ZhonganItem()
        item['type'] = re.compile(r'channelEnName=(\w+)').findall(response.url)[0]
        item['link'] = response.url
        #获取数据
        result = re.compile(r'content : formatServerData\((\[.*\])\)').findall(response.text)[0]

        result = json.loads(result)
        items = []
        for each in result:
            item_info = {}
            item_info['title'] = each['dmGoodsPackage']['campaignName']#保险名
            item_info['plan'] = each['dmGoodsPackage']['planName']#版本
            item_info['payfor'] = each['dmGoodsPackage']['startingPrice']#花费
            #保险期限
            if each['dmGoodsPackage']['premiumFactorList']:
                item_info['timelimite '] =each['dmGoodsPackage']['premiumFactorList'][0]['valueList']
            else:
                item_info['timelimite '] = '1y'
            item_info['forpeople'] = each['dmGoodsPackage']['suitableCrowd']#适合人群

            #理赔详情
            conments = []
            conment_list = each["liabilityDetailData"]
            for li in conment_list:
                conment = {}
                #赔付名
                conment['liabilityName'] = li["liabilityName"] or 'Null'
                #赔付额
                conment['paymentAmount'] = li['paymentAmount'] or 'Null'
                conments.append(conment)
            item_info['conment'] = conments

            items.append(item_info)

        item['detail'] = items

        yield item
