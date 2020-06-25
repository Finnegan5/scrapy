# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.utils.response import open_in_browser

class RushSpider(scrapy.Spider):
    pages = int(input('How many pages do you want to scrapeeeeee: '))
    name = 'rush'
    download_delay = 10.0
    allowed_domains = ['rushhour.nl']
    start_urls = ['https://www.rushhour.nl/search?instock=&page={}'.format(i) for i in range(pages)]
    custom_settings = {
        'ITEM_PIPELINES': {
            'rushhour.pipelines.RushhourPipeline': 400,
        }
    }

    def parse(self, response):
        vinyls= response.css('div.main-wrapper')
        for vinyl in vinyls:
            for v in vinyl.css('div.node'):
                yield {
                    "artist": v.css('div.field-name-field-artist::text').getall(),
                    "title": v.css('div.field-name-title::text').getall(),
                    "id": v.css('div.add-to-cart::attr(data-nid)').getall(),
                    "label": v.css('div.field-name-field-label::text').getall(),
                    "release": v.css('div.field-name-field-release-week::text').getall()
                }
