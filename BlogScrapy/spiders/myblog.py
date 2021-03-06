# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from urllib import parse
from BlogScrapy.items import BlogscrapyItem

class MyblogSpider(scrapy.Spider):
    name = 'myblog'
    allowed_domains = ['momijiame.tumblr.com']
    start_urls = ['http://momijiame.tumblr.com/']

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        # 各ブログポストの <div> を取得する
        posts = soup.find_all('div', {'class': 'title'})
        for post in posts:
            post_url = post.a['href']
            parse_result = parse.urlparse(post_url)  # URL から記事の ID を取得する
            path_segments = parse_result.path.split('/')

            try:
                post_id = path_segments[2]
                print("####Request####: {}")
                spider = BlogscrapyItem(post_id) # 記事の ID を指定して個別のポストを処理する Spider を生成する
                req = scrapy.Request(url=post_url, callback=spider.parse) # リクエストを処理するコールバックに上記の Spider のメソッドを指定する
                yield req
            except:
                print(path_segments)
                yield

        next_page = soup.find('li', {'class': 'next'}) # 次のページへのリンクが入った <li> を取得する
        next_page_link = next_page.a # <li> の中に入った <a> を取り出す

        if 'href' in next_page_link.attrs: # 次のページがあるか確認する
            baseurl = 'http://momijiame.tumblr.com'
            path = next_page_link['href']
            url = '{baseurl}{path}'.format(baseurl=baseurl, path=path)

            # scrapy.Request を返すと次にクロールするページの指定になる
            next_crawl_page = scrapy.Request(url)
            yield next_crawl_page
        else:
            yield




    class MyblogPostSpider(scrapy.Spider):
        name = 'myblogpost'
        allowed_domains = ['momijiame.tumblr.com']

        def __init__(self, post_id, *args, **kwargs):
            super(BlogscrapyItem, self).__init__(*args, **kwargs)

            self.post_id = post_id
            url = 'http://momijiame.tumblr.com/post/{post_id}'.format(
                post_id=self.post_id,
            )
            self.start_urls = [url]

        def parse(self, response):
            soup = BeautifulSoup(response.body, "lxml")

            content = soup.find('div', {'class': 'body'})

            links = content.find_all('a')
            if len(links) < 1:
                # 記事にハイパーリンクが含まれていないので終了
                return

            # ハイパーリンクがあったらタイトルと共にアイテムを返す
            title_div = soup.find('div', {'class': 'title'})
            title = title_div.a.text
            link_urls = [link['href'] for link in links]
            item = BlogscrapyItem(title=title, links=link_urls)
            return item