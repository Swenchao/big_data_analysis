# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lianjia_spider.model import house_info


class LianjiaSpiderPipeline(object):
    def process_item(self, item, spider):
        # 新增数据
        house_info.create(region=item['region'], community=item['community'], number=item['number'],
                          deal_time=item['deal_time'],
                          total_price=item['total_price'], unit_price=item['unit_price'], style=item['style'],
                          floor=item['floor'], size=item['size'], orientation=item['orientation'],
                          build_year=item['build_year'], decoration=item['decoration'],
                          property_time=item['property_time'],
                          elevator=item['elevator'], info=item['info'], create_time=item['create_time'])
        return item