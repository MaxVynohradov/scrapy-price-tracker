# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SmartphoneSpiderSpider(CrawlSpider):
    name = 'smartphone_spider'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/mobile/mobilnye-telefony-i-smartfony/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[@class="product-item"]/div[@class="item-info"]/p[@class="h4"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        product = {}
        features = {}
        product['card_title'] = str(response.xpath('//h1[@datatype="card-title"]/text()').get()).strip()
        for index, feature in enumerate(response.xpath('//table[@class="seo-table"]/tr')):
            key = feature.xpath('td/text()').get()
            value = feature.xpath('td/span/a/text()').get() or feature.xpath('td/p/text()').get()
            if (key and value):
                features[key.strip().replace(':', '')] = value.strip()
        yield product
