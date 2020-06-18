# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    region = scrapy.Field()  # 行政区域
    community = scrapy.Field()  # 房源名称
    deal_time = scrapy.Field()  # 房源名称
    total_price = scrapy.Field()  # 总价
    unit_price = scrapy.Field()  # 每平米单价
    style = scrapy.Field()  # 房屋户型
    floor = scrapy.Field()  # 楼层高度
    size = scrapy.Field()  # 建筑面积
    orientation = scrapy.Field()  # 朝向
    build_year = scrapy.Field()  # 建造时间
    decoration = scrapy.Field()  # 装修
    property_time = scrapy.Field()  # 产权年限
    elevator = scrapy.Field()  # 电梯
    info = scrapy.Field()  # 周边学校
    number = scrapy.Field()  # 链家编号（主键去重）
    create_time = scrapy.Field()  # 爬取时间

