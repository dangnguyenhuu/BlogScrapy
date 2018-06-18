# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BlogScrapy.items import BikaeItem
from bs4 import BeautifulSoup
from urllib import parse



class BikaeSpider(scrapy.Spider):
    name = 'bikae'
    allowed_domains = ['bikae.net']
    start_urls = ['http://bikae.net/']

    rules = [Rule(LinkExtractor(), callback='parse', follow=True)]


    def parse(self, response):

        soup = BeautifulSoup(response.body, "lxml")

        item = BikaeItem()
        item['links'] = response.url
        # ページのどの部分をスクレイプするかを指定
        # xPath形式での指定に加え、CSS形式での指定も可能
        item['title'] = soup.head.title.string
        return item