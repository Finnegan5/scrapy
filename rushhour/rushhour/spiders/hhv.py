# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
import re

class HhvSpider(scrapy.Spider):
    name = 'hhv'
    allowed_domains = ['www.hhv.de']
    start_urls = ['https://www.hhv.de/shop/en/vinyl/p:125B9G']
    custom_settings = {
        'ITEM_PIPELINES': {
            'rushhour.pipelines.HhvPipeline': 300,
        }
    }

    def parse(self, response):
        vinyls = response.css('div.items')
        for vinyl in vinyls:
            for v in vinyl.css('div.item_list_entry'):
                if not v.css('div.sale'):
                    yield {
                        'artist': v.css('div.artist::text').getall(),
                        'title': v.css('div.title::text').getall(),
                        'price': v.css('div.price::text').getall(),
                        'label': v.css('div.format_label::text').getall(),
                        'release': v.css('div.release>span.value::text').getall()
                    }
                else:
                    yield {
                        'artist': v.css('div.artist::text').getall(),
                        'title': v.css('div.title::text').getall(),
                        'price': v.css('div.price>span.new::text').getall(),
                        'label': v.css('div.format_label::text').getall(),
                        'release': v.css('div.release>span.value::text').getall()
                    }

        max_pages = re.search(r'\d{3}$', response.css('div.status::text').get(), re.IGNORECASE)
        max_pages = int(max_pages.group(0))
        current_page = re.search(r'\ \d*\ ', response.css('div.status::text').get(), re.IGNORECASE)
        current_page = int(current_page.group(0))

        next_page = 'https://www.hhv.de/shop/en/vinyl/p:125B9G' + '?&page=' + str(current_page + 1)
        if not (current_page + 1) > max_pages:
            yield scrapy.Request(next_page, callback=self.parse)

