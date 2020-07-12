# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import re
import json
import os
import psycopg2
from scrapy.exceptions import DropItem
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()


class HhvPipeline:

    def open_spider(self, spider):
        token = os.environ.get("TOKEN")

        url = 'http://127.0.0.1:3000/api/v1/db_url'
        headers = {'token': token}
        r = requests.get(url, headers=headers)
        url = json.loads(r.text)['database_url']

        result = urlparse(url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname

        self.connection = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname
        )
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        if item['artist']:
            artist_search = re.search(r'[a-zA-Z0-9- ]+', str(item['artist']), re.IGNORECASE)
            item['artist'] = artist_search.group(0)
        if item['title']:
            title_search = re.search(r'[a-zA-Z0-9- ]+', str(item['title']), re.IGNORECASE)
            item['title'] = title_search.group(0)
        if item['label']:
            label_search = re.search(r'\((.*?)\)', str(item['label']), re.IGNORECASE)
            item['label'] = label_search.group(1)
        if item['release']:
            release_search = re.search(r'\d{4}', str(item['release']), re.IGNORECASE)
            item['release'] = release_search.group(0)
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()
        if item['price']:
            price_search = re.search(r'\d*\,\d\d', str(item['price']), re.IGNORECASE)
            item['price'] = price_search.group(0).replace(',', '.')
        sql = '''
            INSERT INTO hhv_records ("artist", "title", "price", "label", "release", "created_at", "updated_at")
            VALUES(%s, %s, %s, %s, %s, %s, %s)
        '''
        self.cursor.execute(sql, (item["artist"], item["title"], item["price"], item["label"], item["release"], item["created_at"], item["updated_at"]))
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

class RushhourPipeline:
    def process_item(self, item, spider):
        if not item['artist']:
            raise DropItem("Missing artist in %s" % item)
        if item['release']:
            release_search = re.search(r'\d{4}', str(item['release']), re.IGNORECASE)
            item['release'] = release_search.group(0)
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()
        return item
