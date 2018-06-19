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

        categories = soup.select("li.swipe-menu-item > a.title")
        for category in categories:
            url = category.get("href")
            parse_result = parse.urlparse(url).path.split('/')
            if len(parse_result) > 2:
                spider = MyblogPostSpider(url)
                req = scrapy.Request(url=url, callback=spider.parse)
                yield req
            else:
                yield


class MyblogPostSpider(scrapy.Spider):
    name = 'bikaepost'
    allowed_domains = ['bikae.net']

    def __init__(self, url, *args, **kwargs):
        super(MyblogPostSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        for a in soup.find_all('article'):
            try:
                item = BikaeItem()
                item['links'] = a.select("div.entry-header > h1 > a")[0].get('href')
                item['title'] = a.select("div.entry-header > h1 > a")[0].string
                item['thumbnail'] = a.select("div.entry-summary > div.toppage-post-feature-img > a > img")[0].get('src')
                yield item
            except:
                yield

            # print(a.select("div.entry-header > h1 > a")[0].string)  # Title
            # print(a.select("div.entry-header > h1 > a")[0].get('href'))  # Url
            # print(a.select("div.entry-summary > div.toppage-post-feature-img > a > img")[0].get('src'))  # Thumbnail
            # print(a.select("div.entry-summary > div.toppage-post-excerpt > div")[0].string)  # Des