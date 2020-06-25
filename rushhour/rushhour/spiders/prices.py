# -*- coding: utf-8 -*-
import scrapy
import csv
import json
from scrapy.utils.response import open_in_browser
from scrapy.http.request import Request

class PricesSpider(scrapy.Spider):
    name = 'prices'


    def chunks(self, list, n):
        for i in range(0, len(list), n):
            yield list[i:i + n]


    def start_requests(self):
        with open('test.csv') as csv_file:
            ids=[]
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                ids.append(row[2] + '+')
        chunked = list(self.chunks(ids, 400))
        for chunk in chunked:
            string = ''.join(chunk).replace("+id+", "")
            url = 'https://www.rushhour.nl/index.php?q=rushhour/record/multiple/add-to-cart&nids=' + string
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        raw = response.body
        info = json.loads(raw)
        yield info

