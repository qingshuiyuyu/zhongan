# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhonganItem(scrapy.Item):

    type = scrapy.Field()#保险类型
    link =scrapy.Field()#产品连接
    title = scrapy.Field()#保险名称
    #planName = scrapy.Field()#保险计划
    payfor = scrapy.Field()#支付金额

    detail = scrapy.Field()#赔付详情
    #onment = scrapy.Field()#赔付项目
    # compensate = scrapy.Field() # 赔付金额
    # timelimite = scrapy.Field()#赔付期限
    # forpeople = scrapy.Field()#赔付人群



