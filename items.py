# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YalayiImagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    album_name = scrapy.Field()
    model_name = scrapy.Field()
    album_num = scrapy.Field()
    album_update = scrapy.Field()
    album_url = scrapy.Field()
    image_urls = scrapy.Field()
    image_name = scrapy.Field()