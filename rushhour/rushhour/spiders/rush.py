# -*- coding: utf-8 -*-
import scrapy
import json

class RushSpider(scrapy.Spider):
    name = 'rush'
    allowed_domains = ['rushhour.nl']
    start_urls = ['https://www.rushhour.nl/search?instock']
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
        next_page = response.css('a[title="Go to next page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
