# -*- coding: utf-8 -*-
import random
from urllib.request import urlopen
import csv
import datetime
from io import StringIO
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SmartphoneSpiderSpider(CrawlSpider):
    name = 'smartphone_spider'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/mobile/mobilnye-telefony-i-smartfony/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//li[@class="product-item"]/div[@class="item-info"]/p[@class="h4"]/a'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="pages"]'), follow=True),
    )

    def parse_item(self, response):
        product = {}
        features = {}
        product['features'] = features
        product['card_title'] = str(response.xpath('//h1[@datatype="card-title"]/text()').get()).strip()
        product['card_id'] = str(response.css('span[data-card-id]::attr(data-card-id)').get()).strip()
        product['image'] = str(response.css('.zg-canvas-img::attr(src)').get()).strip()
        for index, feature in enumerate(response.xpath('//table[@class="seo-table"]/tr')):
            key = feature.xpath('td/text()').get()
            value = feature.xpath('td/span/a/text()').get() or feature.xpath('td/p/text()').get()
            if key and value:
                features[key.strip().replace(':', '')] = value.strip()
        product['time_series'] = SmartphoneSpiderSpider.load_csv(product['card_id'])
        yield product

    @staticmethod
    def load_csv(card_id):
        card_id_str = str(card_id)
        rnd = random.uniform(0, 1)
        csv_url = f'https://hotline.ua/temp/charts/{card_id_str[:-2]}/{card_id_str[-2:]}complex.csv?rnd={rnd}'
        data = urlopen(csv_url).read().decode('ascii', 'ignore')
        datafile = StringIO(data)
        csv_reader = csv.reader(datafile, delimiter=';')
        data = []
        for row in csv_reader:
            date, price, quant, popul = row
            data.append({  
                'date': datetime.datetime.strptime(date, '%d.%m.%Y'),
                'price': float(price),
                'quant': float(quant),
                'popul': float(popul),
            })
        return data
