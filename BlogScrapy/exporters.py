#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.contrib.exporter import JsonLinesItemExporter


class NonEscapeJsonLinesItemExporter(JsonLinesItemExporter):

    def __init__(self, filepath, **kwargs):
        super(NonEscapeJsonLinesItemExporter, self).__init__(
            filepath,
            ensure_ascii=False
        )