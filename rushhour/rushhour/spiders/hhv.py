# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser

class HhvSpider(scrapy.Spider):
    pages = int(input('How many pages do you want to scrape: '))
    name = 'hhv'
    allowed_domains = ['www.hhv.de']
    start_urls = ['https://www.hhv.de/shop/en/vinyl/p:125B9G?&page={}'.format(i + 1) for i in range(pages)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'rushhour.pipelines.HhvPipeline': 300,
        }
    }

    def parse(self, response):
        vinyls = response.css('div.items')
        for vinyl in vinyls:
            for v in vinyl.css('div.item_list_entry'):
                yield {
                    'artist': v.css('div.artist::text').getall(),
                    'title': v.css('div.title::text').getall(),
                    'price': v.css('div.price::text').getall(),
                    'label': v.css('div.format_label::text').getall(),
                    'release': v.css('div.release>span.value::text').getall()
                }
