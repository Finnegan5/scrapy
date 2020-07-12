# -*- coding: utf-8 -*-
import scrapy
import json
import re

class RushSpider(scrapy.Spider):
    name = 'rush'
    allowed_domains = ['rushhour.nl']
    start_urls = ['https://www.rushhour.nl/search?instock']
    custom_settings = {
        'ITEM_PIPELINES': {
            'rushhour.pipelines.RushhourPipeline': 400,
        },
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    def parse(self, response):
        vinyls= response.css('div.main-wrapper')
        records=[]
        nids=[]
        for vinyl in vinyls:
            for v in vinyl.css('div.node'):

                records.append({
                    "artist": v.css('div.field-name-field-artist::text').get(),
                    "title": v.css('div.field-name-title::text').get(),
                    "nid": v.css('div.add-to-cart::attr(data-nid)').get(),
                    "label": v.css('div.field-name-field-label::text').get(),
                    "release": v.css('div.field-name-field-release-week::text').get()
                })

                if v.css('div.add-to-cart::attr(data-nid)').get() is not None:
                    nids.append(v.css('div.add-to-cart::attr(data-nid)').get())
        string = '+'.join(nids)
        url = 'https://www.rushhour.nl/index.php?q=rushhour/record/multiple/add-to-cart&nids=' + string
        next_page = response.css('a[title="Go to next page"]::attr(href)').get()
        yield response.follow(url=url, callback=self.parse_prices, meta={'records': records, 'next': next_page})

    def parse_prices(self, response):
        records = response.request.meta['records']
        for record in records:
            artist = record['artist']
            title = record['title']
            nid = record['nid']
            label = record['label']
            release = record['release']
            raw = response.body
            info = json.loads(raw)
            if nid in info:
                price = re.search(r'\d+,\d\d', info[nid])
                price = price.group(0)

                yield {
                    "artist": artist,
                    "title": title,
                    "price": price,
                    "label": label,
                    "release": release
                }

        next_page = response.request.meta['next']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

