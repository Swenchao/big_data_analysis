# -*- coding: utf-8 -*-
import scrapy

from lianjia_spider.items import LianjiaSpiderItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = []
    #  爬取城市（广州 东莞 湛江）
    city_region = ['gz', 'dg', 'zhanjiang']
    # city_region = ['gz']

    def start_requests(self):
        # start_urls.append('https://gz.lianjia.com/chengjiao/' + region + '/pg' + str(i) + "ddo41/")
        url_ori = 'https://%s.lianjia.com/chengjiao'
        for str_temp in self.city_region:
            url = url_ori % str_temp
            # print("+++++++++++++++++++++")
            # print(url_ori)
            yield scrapy.Request(url=url, callback=self.parse_main)

    def parse_main(self,response):
        url = response.url
        county_region = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        for region in county_region:
            region = str(region).replace("/chengjiao/","")
            # 可修改页数,可能会有没有的
            for i in range(1, 25):
                url_temp = url
                # https://gz.lianjia.com/chengjiao/huangpugz/pg3ddo41/
                # self.start_urls.append(url_temp + region + 'pg' + str(i) + "ddo41/")
                url_new = url_temp + region + 'pg' + str(i) + "ddo41/"
                yield scrapy.Request(url=url_new,callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            li_item = response.xpath('//ul[@class="listContent"]')
            for li in li_item:
                hrefs = li.xpath('//a[@class="img"]/@href').extract()
                for href in hrefs:
                    yield scrapy.Request(url=href, callback=self.more, dont_filter=True)

    def more(self, response):
        # 根据url来判断是哪个城市
        if response.url.find('//gz.') != -1:
            city = '广州'
        elif response.url.find('//dg.') != -1:
            city = '东莞'
        else:
            city = '湛江'
        item = LianjiaSpiderItem()
        info1 = ''
        # 地区
        area = response.xpath('//section[1]/div[1]/a[3]/text()').extract()[0]
        item['region'] = city + "-" + area.replace("二手房成交", "")
        # print(item['region'])
        # 小区名
        community = response.xpath('//title/text()').extract()[0]
        item['community'] = community[:community.find(" ", 1, len(community))]
        # 成交时间
        deal_time = response.xpath('//div[@class="wrapper"]/span/text()').extract()[0]
        item['deal_time'] = deal_time.replace("成交", "").strip()
        # print("================================")
        # print(deal_time)
        # 总价
        item['total_price'] = response.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()[
                                  0] + '万'
        # 单价
        item['unit_price'] = response.xpath('//div[@class="price"]/b/text()').extract()[0] + '元/平'

        # 户型
        introContent = response.xpath('//div[@class="content"]/ul/li/text()').extract()
        # print("================================")
        # print(introContent)
        item['style'] = introContent[0].strip()
        # 楼层
        item['floor'] = introContent[1].strip()
        # 大小
        item['size'] = introContent[2].strip()
        # 朝向
        item['orientation'] = introContent[6].strip()
        # 建成年代
        item['build_year'] = introContent[7].strip()
        # 装修情况
        item['decoration'] = introContent[8].strip()
        # 产权年限
        item['property_time'] = introContent[17].strip()
        # 电梯配备
        item['elevator'] = introContent[12].strip()
        # 编号（主键）
        item['number'] = introContent[13].strip()
        # 其他周边等信息
        infos = response.xpath('//div[@class="content"]/text()').extract()
        if len(infos) != 0:
            for info in infos:
                info = "".join(info.split())
                info1 += info
            item['info'] = info1
        else:
            item['info'] = '暂无信息'
        return item
