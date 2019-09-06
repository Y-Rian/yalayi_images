# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem

class YalayiImagesPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        print('----正在下载大图{0}--{1}'.format(item['album_name'], item['image_name']))
        image_url = item['image_urls']
        image_name = item['image_name']
        album_name = item['album_name']
        yield Request(image_url, meta={"image_name": image_name,
                                        "album_name": album_name})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloader Failed')
        print('======{0}----{1} 已经保存'.format(item['album_name'], item['image_name']))
        return item


    def file_path(self, request, response=None, info=None):
        album_name = request.meta['album_name']
        image_name = request.meta['image_name']
        filename = './yalayi/{0}/{1}.jpg'.format(album_name, image_name)
        return filename


import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db, mongo_port, collection_name):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        self.collection_name = collection_name
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB'),
            mongo_port = crawler.settings.get('MONGO_PORT'),
            collection_name = crawler.settings.get("MONGO_COLLECTION_NAME")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_url, port=self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        print('   {}  已保存到MongoDB'.format(item['album_name']))
        return item