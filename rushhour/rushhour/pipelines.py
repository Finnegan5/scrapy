# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import re
from datetime import datetime

class HhvPipeline:
    def process_item(self, item, spider):
        if item['label']:
            label_search = re.search('\((.*?)\)', str(item['label']), re.IGNORECASE)
            item['label'] = label_search.group(1)
        if item['release']:
            release_search = re.search('\d{4}', str(item['release']), re.IGNORECASE)
            item['release'] = release_search.group(0)
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()
        if item['price']:
            price_search = re.search('\d*\,\d\d', str(item['price']), re.IGNORECASE)
            item['price'] = price_search.group(0).replace(',', '.')

        return item

class RushhourPipeline:
    def process_item(self, item, spider):
        if not item['artist']:
            raise DropItem("Missing artist in %s" % item)
        if item['release']:
            release_search = re.search('\d{4}', str(item['release']), re.IGNORECASE)
            item['release'] = release_search.group(0)
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()
        return item
