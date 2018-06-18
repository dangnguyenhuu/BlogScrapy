# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup



class MyblogSpider(scrapy.Spider):
    name = 'myblog'
    allowed_domains = ['momijiame.tumblr.com']
    start_urls = ['http://momijiame.tumblr.com/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        # 次のページへのリンクが入った <li> を取得する
        next_page = soup.find('li', {'class': 'next'})
        # <li> の中に入った <a> を取り出す
        next_page_link = next_page.a
        # 次のページがあるか確認する
        if 'href' not in next_page_link.attrs:
            # 次のページが見つからなかったので終了
            yield

        # 次のページがあるときは URL を組み立てる
        baseurl = 'http://momijiame.tumblr.com'
        path = next_page_link['href']
        url = '{baseurl}{path}'.format(baseurl=baseurl, path=path)
        print(url)

        # scrapy.Request を返すと次にクロールするページの指定になる
        next_crawl_page = scrapy.Request(url)
        yield next_crawl_page