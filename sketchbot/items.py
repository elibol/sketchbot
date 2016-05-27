# -*- coding: utf-8 -*-
"""
Project items
"""

import scrapy

class EmailItem(scrapy.Item):
    """
    Item yielded by EmailSpider.
    """
    email = scrapy.Field()
    url = scrapy.Field()
