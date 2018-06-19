# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogscrapyItem(scrapy.Item):
    title = scrapy.Field()
    links = scrapy.Field()
    pass



class BikaeItem(scrapy.Item):
    title = scrapy.Field()
    links = scrapy.Field()
    thumbnail = scrapy.Field()
    description = scrapy.Field()
    pass