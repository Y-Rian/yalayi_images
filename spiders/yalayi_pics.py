# -*- coding: utf-8 -*-
import scrapy
from items import YalayiImagesItem
import copy

class YalayiPicsSpider(scrapy.Spider):
    name = 'yalayi_pics'
    # allowed_domains = ['www.yalayi.com/gallery']
    start_urls = ['https://www.yalayi.com/gallery/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'yalayi_images.pipelines.ImagePipeline': 300,
            'yalayi_images.pipelines.MongoPipeline': 301,
        }
    }

    def parse(self, response):
        # print(response.status)
        item = YalayiImagesItem()
        img_list = response.css('.img-box')
        # print(img_list)
        for img in img_list:
            item['model_name'] = img.xpath('.//div[@class="album"]/span[1]/a/text()').extract_first()
            item['album_name'] = img.xpath('.//div[@class="album"]/span[2]/a/text()').extract_first()
            item['album_url'] = img.xpath('.//div[@class="album"]/span[2]/a/@href').extract_first()
            item['album_update'] = img.xpath('.//div[@class="info"]/div[2]/text()').extract_first()
            item['album_num'] = img.xpath('.//div[@class="info"]/div[1]/text()').extract_first()
            yield scrapy.Request(item['album_url'], callback=self.parse_album_url, meta={'item': copy.deepcopy(item)})            # break

        is_next_page = response.xpath('//div[@class="pages"]/a[last()-1]/text()').extract_first()
        next_page = response.xpath('//div[@class="pages"]/a[last()-1]/@href').extract()
        if next_page is not None and '下一页' in is_next_page:
            next_page = next_page[0]
            yield response.follow(next_page, callback=self.parse)
            print('下一页 url为：{}'.format(next_page))
        else:
            print('已经到图集的最后一页了')

    def parse_album_url(self, response):
        item = response.meta['item']
        image_list = response.css('.bigimg img')
        for image in image_list:
            item["image_urls"] = image.css('img::attr(data-src)').extract_first()
            item['image_name'] = image.css('img::attr(alt)').extract_first()
            yield item



