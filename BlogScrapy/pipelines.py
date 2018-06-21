# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
import os
from BlogScrapy import settings
import shutil


class MyImagesPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # DL できたファイルのパス
        file_paths = [x['path'] for ok, x in results if ok]

        # ドメインごとのフォルダに move
        for file_path in file_paths:
            img_home = settings.IMAGES_STORE
            full_path = img_home + "/" + file_path
            domain_home = img_home + "/" + item['domain']

            os.makedirs(domain_home, exist_ok=True)
            # DL した結果同じファイルのことがある
            if os.path.exists(domain_home + '/' + os.path.basename(full_path)):
                continue
            shutil.move(full_path, domain_home)

        # parse() の続きに戻る
        return item



class BlogscrapyPipeline(object):
    def process_item(self, item, spider):
        return item
